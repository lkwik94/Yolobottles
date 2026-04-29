use std::path::Path;
use std::sync::Arc;
use std::time::Instant;

use parking_lot::Mutex;
use tracing::{info, warn};

use crate::inference::Model;
use crate::ejector;
use crate::Stats;

/// Process all images in `dir` (jpg/png), in alphabetical order.
/// Simulates a conveyor by processing one image at a time.
pub async fn run_image_bank(
    dir: &Path,
    model: Arc<Mutex<Model>>,
    stats: Arc<Mutex<Stats>>,
    eject_delay_ms: u64,
) -> anyhow::Result<()> {
    let pattern = format!("{}/**/*.{{jpg,jpeg,png,bmp}}", dir.display());
    let mut paths: Vec<_> = glob::glob(&pattern)?
        .filter_map(|e| e.ok())
        .collect();
    paths.sort();

    if paths.is_empty() {
        warn!("No images found in {}", dir.display());
        return Ok(());
    }

    info!("Found {} images. Starting inspection...", paths.len());

    for path in &paths {
        let t0 = Instant::now();

        let img = match image::open(path) {
            Ok(i) => i,
            Err(e) => {
                warn!("Cannot open {:?}: {}", path, e);
                continue;
            }
        };

        let detections = model.lock().infer(&img)?;
        let is_ng = !detections.is_empty();

        let elapsed_ms = t0.elapsed().as_millis();

        {
            let mut s = stats.lock();
            s.total += 1;
            if is_ng { s.ng += 1; } else { s.ok += 1; }
        }

        if is_ng {
            info!(
                "NG  [{:>4}ms] {:?}  — {} defect(s): {}",
                elapsed_ms,
                path.file_name().unwrap_or_default(),
                detections.len(),
                detections.iter()
                    .map(|d| format!("{} {:.0}%", d.class_name, d.confidence * 100.0))
                    .collect::<Vec<_>>()
                    .join(", ")
            );
            ejector::trigger(eject_delay_ms).await;
        } else {
            info!(
                "OK  [{:>4}ms] {:?}",
                elapsed_ms,
                path.file_name().unwrap_or_default()
            );
        }
    }

    let s = stats.lock();
    info!(
        "\nInspection complete — Total: {}  OK: {}  NG: {}  ({:.1}% reject rate)",
        s.total,
        s.ok,
        s.ng,
        if s.total > 0 { s.ng as f64 / s.total as f64 * 100.0 } else { 0.0 }
    );

    Ok(())
}
