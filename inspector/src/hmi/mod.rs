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

use crate::Stats;

#[derive(Serialize)]
struct StatsResponse {
    total: u64,
    ok:    u64,
    ng:    u64,
    reject_rate_pct: f64,
}

async fn get_stats(State(stats): State<Arc<Mutex<Stats>>>) -> impl IntoResponse {
    let s = stats.lock();
    let rate = if s.total > 0 { s.ng as f64 / s.total as f64 * 100.0 } else { 0.0 };
    Json(StatsResponse {
        total: s.total,
        ok:    s.ok,
        ng:    s.ng,
        reject_rate_pct: rate,
    })
}

pub async fn serve(port: u16, stats: Arc<Mutex<Stats>>) {
    let static_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("src/hmi/static");

    let app = Router::new()
        .route("/api/stats", get(get_stats))
        .nest_service("/", ServeDir::new(static_dir))
        .with_state(stats);

    let addr = format!("0.0.0.0:{port}");
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
