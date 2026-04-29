mod inference;
mod pipeline;
mod ejector;
mod hmi;

use std::collections::VecDeque;
use std::path::PathBuf;
use std::sync::Arc;

use clap::Parser;
use parking_lot::Mutex;
use tracing::info;

/// Yolobottles — PET bottle bottom inspection
#[derive(Parser, Debug)]
#[command(version)]
pub struct Args {
    /// Path to the ONNX model (e.g. ../models/exports/onnx/bottle_v1.onnx)
    #[arg(short, long)]
    pub model: PathBuf,

    /// Directory of images to inspect (image bank mode)
    #[arg(short, long)]
    pub images: PathBuf,

    /// Detection confidence threshold [0.0–1.0]
    #[arg(long, default_value_t = 0.5)]
    pub threshold: f32,

    /// HMI web server port
    #[arg(long, default_value_t = 8080)]
    pub port: u16,

    /// Simulate ejector delay in ms (0 = disabled / dry-run)
    #[arg(long, default_value_t = 50)]
    pub eject_delay_ms: u64,
}

pub const HISTORY_CAPACITY: usize = 50;

#[derive(Debug, Clone)]
pub struct DefectSummary {
    pub class_name:     String,
    pub confidence_pct: u32,
}

#[derive(Debug, Clone)]
pub struct InspectionRecord {
    pub filename:   String,
    pub is_ng:      bool,
    pub elapsed_ms: u64,
    pub defects:    Vec<DefectSummary>,
}

/// Shared counters visible to pipeline and HMI
#[derive(Debug, Default)]
pub struct Stats {
    pub total:         u64,
    pub ok:            u64,
    pub ng:            u64,
    /// Per-class NG detection counts (indexed by class_id)
    pub class_counts:  [u64; 5],
    /// Rolling history of the last HISTORY_CAPACITY inspections
    pub history:       VecDeque<InspectionRecord>,
    /// Set to true when the image bank has been fully processed
    pub pipeline_done: bool,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            std::env::var("RUST_LOG")
                .unwrap_or_else(|_| "inspector=info".into()),
        )
        .init();

    let args = Args::parse();
    let stats = Arc::new(Mutex::new(Stats::default()));

    info!("Loading model: {}", args.model.display());
    let model = Arc::new(Mutex::new(inference::Model::load(&args.model, args.threshold)?));

    // Start HMI server in background
    let hmi_stats = Arc::clone(&stats);
    let port = args.port;
    tokio::spawn(async move {
        hmi::serve(port, hmi_stats).await;
    });
    info!("HMI running on http://localhost:{}", port);

    // Run inspection pipeline (blocking)
    pipeline::run_image_bank(&args.images, model, stats, args.eject_delay_ms).await?;

    Ok(())
}
