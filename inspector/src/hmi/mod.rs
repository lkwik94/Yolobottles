use std::sync::Arc;

use axum::{
    extract::State,
    response::IntoResponse,
    routing::get,
    Json, Router,
};
use parking_lot::Mutex;
use serde::Serialize;
use tower_http::services::ServeDir;

use crate::inference::CLASS_NAMES;
use crate::Stats;

// ---------------------------------------------------------------------------
// Response types
// ---------------------------------------------------------------------------

#[derive(Serialize)]
struct ClassCount {
    name:  &'static str,
    count: u64,
}

#[derive(Serialize)]
struct StatsResponse {
    total:           u64,
    ok:              u64,
    ng:              u64,
    reject_rate_pct: f64,
    class_counts:    Vec<ClassCount>,
    pipeline_done:   bool,
}

#[derive(Serialize)]
struct DefectEntry {
    class_name:     String,
    confidence_pct: u32,
}

#[derive(Serialize)]
struct HistoryEntry {
    filename:   String,
    is_ng:      bool,
    elapsed_ms: u64,
    defects:    Vec<DefectEntry>,
}

// ---------------------------------------------------------------------------
// Handlers
// ---------------------------------------------------------------------------

async fn get_stats(State(stats): State<Arc<Mutex<Stats>>>) -> impl IntoResponse {
    let s = stats.lock();
    let rate = if s.total > 0 { s.ng as f64 / s.total as f64 * 100.0 } else { 0.0 };
    Json(StatsResponse {
        total: s.total,
        ok:    s.ok,
        ng:    s.ng,
        reject_rate_pct: rate,
        class_counts: CLASS_NAMES.iter().enumerate()
            .map(|(i, &name)| ClassCount { name, count: s.class_counts[i] })
            .collect(),
        pipeline_done: s.pipeline_done,
    })
}

async fn get_history(State(stats): State<Arc<Mutex<Stats>>>) -> impl IntoResponse {
    let s = stats.lock();
    let entries: Vec<HistoryEntry> = s.history.iter().rev().map(|r| HistoryEntry {
        filename:   r.filename.clone(),
        is_ng:      r.is_ng,
        elapsed_ms: r.elapsed_ms,
        defects:    r.defects.iter().map(|d| DefectEntry {
            class_name:     d.class_name.clone(),
            confidence_pct: d.confidence_pct,
        }).collect(),
    }).collect();
    Json(entries)
}

// ---------------------------------------------------------------------------
// Server
// ---------------------------------------------------------------------------

pub async fn serve(port: u16, stats: Arc<Mutex<Stats>>) {
    let static_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("src/hmi/static");

    let app = Router::new()
        .route("/api/stats",   get(get_stats))
        .route("/api/history", get(get_history))
        .nest_service("/", ServeDir::new(static_dir))
        .with_state(stats);

    let addr = format!("0.0.0.0:{port}");
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
