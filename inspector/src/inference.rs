use std::path::Path;

use image::{DynamicImage, RgbImage};
use ort::{inputs, session::Session, value::Tensor};
use tracing::debug;

const INPUT_SIZE: u32 = 640;
const NUM_CLASSES: usize = 5;

pub const CLASS_NAMES: [&str; NUM_CLASSES] = [
    "color_defect",
    "hole",
    "contamination",
    "whitening",
    "mold_defect",
];

#[derive(Debug, Clone)]
pub struct Detection {
    pub class_id:   usize,
    pub class_name: &'static str,
    pub confidence: f32,
    /// Bounding box in original image coordinates [x1, y1, x2, y2]
    pub bbox: [f32; 4],
}

pub struct Model {
    session:   Session,
    threshold: f32,
}

impl Model {
    pub fn load(model_path: &Path, threshold: f32) -> anyhow::Result<Self> {
        let session = Session::builder()
            .map_err(|e| anyhow::anyhow!("{e}"))?
            .with_optimization_level(ort::session::builder::GraphOptimizationLevel::All)
            .map_err(|e| anyhow::anyhow!("{e}"))?
            .with_intra_threads(4)
            .map_err(|e| anyhow::anyhow!("{e}"))?
            .commit_from_file(model_path)
            .map_err(|e| anyhow::anyhow!("{e}"))?;

        Ok(Self { session, threshold })
    }

    pub fn infer(&mut self, img: &DynamicImage) -> anyhow::Result<Vec<Detection>> {
        let (orig_w, orig_h) = (img.width(), img.height());

        // Resize + normalize to [0, 1] float32 in BCHW layout
        let resized = img.resize_exact(INPUT_SIZE, INPUT_SIZE, image::imageops::FilterType::Lanczos3);
        let rgb: RgbImage = resized.into_rgb8();
        let data = image_to_tensor(&rgb);

        // Shape: [1, 3, 640, 640] as i64 for ort
        let shape = [1i64, 3, INPUT_SIZE as i64, INPUT_SIZE as i64];
        let value = Tensor::from_array((shape, data))
            .map_err(|e| anyhow::anyhow!("{e}"))?;

        let outputs = self.session.run(inputs!["images" => value])?;

        // ort rc.12: try_extract_tensor returns (&Shape, &[T])
        let output = outputs["output0"].try_extract_tensor::<f32>()?;
        let (shape, raw_slice) = output;
        debug!("Model output shape: {:?}", shape);
        // Copy to owned Vec so we can drop outputs (releases session borrow) before calling decode_output
        let raw: Vec<f32> = raw_slice.to_vec();
        drop(outputs);
        let detections = self.decode_output(&raw, orig_w, orig_h);


        Ok(detections)
    }

    fn decode_output(&self, raw: &[f32], orig_w: u32, orig_h: u32) -> Vec<Detection> {
        // raw layout: [4 + nc, 8400] — row-major, no objectness (YOLOv8)
        let num_anchors = 8400_usize;

        let mut detections: Vec<Detection> = Vec::new();

        for i in 0..num_anchors {
            // Find best class
            let (class_id, score) = (0..NUM_CLASSES)
                .map(|c| (c, raw[(4 + c) * num_anchors + i]))
                .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
                .unwrap();

            if score < self.threshold {
                continue;
            }

            // Decode bbox (cx, cy, w, h) normalized → pixel coords on original image
            let cx = raw[0 * num_anchors + i];
            let cy = raw[1 * num_anchors + i];
            let bw = raw[2 * num_anchors + i];
            let bh = raw[3 * num_anchors + i];

            let scale_x = orig_w as f32 / INPUT_SIZE as f32;
            let scale_y = orig_h as f32 / INPUT_SIZE as f32;

            let x1 = (cx - bw / 2.0) * scale_x;
            let y1 = (cy - bh / 2.0) * scale_y;
            let x2 = (cx + bw / 2.0) * scale_x;
            let y2 = (cy + bh / 2.0) * scale_y;

            detections.push(Detection {
                class_id,
                class_name: CLASS_NAMES[class_id],
                confidence: score,
                bbox: [x1, y1, x2, y2],
            });
        }

        // Basic NMS (greedy IoU suppression)
        nms(detections, 0.45)
    }
}

fn image_to_tensor(img: &RgbImage) -> Vec<f32> {
    let (w, h) = (img.width() as usize, img.height() as usize);
    let mut tensor = vec![0f32; 3 * h * w];
    for (x, y, pixel) in img.enumerate_pixels() {
        let (x, y) = (x as usize, y as usize);
        tensor[0 * h * w + y * w + x] = pixel[0] as f32 / 255.0; // R
        tensor[1 * h * w + y * w + x] = pixel[1] as f32 / 255.0; // G
        tensor[2 * h * w + y * w + x] = pixel[2] as f32 / 255.0; // B
    }
    tensor
}

fn iou(a: &[f32; 4], b: &[f32; 4]) -> f32 {
    let ix1 = a[0].max(b[0]);
    let iy1 = a[1].max(b[1]);
    let ix2 = a[2].min(b[2]);
    let iy2 = a[3].min(b[3]);
    let inter = (ix2 - ix1).max(0.0) * (iy2 - iy1).max(0.0);
    let area_a = (a[2] - a[0]) * (a[3] - a[1]);
    let area_b = (b[2] - b[0]) * (b[3] - b[1]);
    inter / (area_a + area_b - inter + 1e-6)
}

fn nms(mut dets: Vec<Detection>, iou_thresh: f32) -> Vec<Detection> {
    dets.sort_by(|a, b| b.confidence.partial_cmp(&a.confidence).unwrap());
    let mut kept = Vec::new();
    let mut suppressed = vec![false; dets.len()];

    for i in 0..dets.len() {
        if suppressed[i] {
            continue;
        }
        for j in (i + 1)..dets.len() {
            if dets[i].class_id == dets[j].class_id && iou(&dets[i].bbox, &dets[j].bbox) > iou_thresh {
                suppressed[j] = true;
            }
        }
        kept.push(dets[i].clone());
    }
    kept
}
