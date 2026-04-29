use tokio::time::{sleep, Duration};
use tracing::debug;

/// Trigger the ejector for a detected NG bottle.
///
/// In mockup mode (eject_delay_ms > 0) this just simulates the pulse delay.
/// Production: replace with GPIO write or serial command to the ejector controller.
pub async fn trigger(delay_ms: u64) {
    if delay_ms == 0 {
        debug!("Ejector: dry-run (delay=0, not triggering)");
        return;
    }

    // TODO (production): assert GPIO pin / send serial frame here
    debug!("Ejector: pulse ON");
    sleep(Duration::from_millis(delay_ms)).await;
    debug!("Ejector: pulse OFF");
}
