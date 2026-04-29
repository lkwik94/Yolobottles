# Wiki Log

Append-only chronological record of all operations.

Format: `## [YYYY-MM-DD] <operation> | <title>`

Parse recent entries: `grep "^## \[" wiki/log.md | tail -10`

---

## [2026-04-28] init | Wiki workspace initialized

## [2026-04-28] manual-concept | ort 2.0.0-rc.12 API — empirical findings during inspector build
- Created `wiki/concepts/ort-rc12-api.md`
- Documents: SessionBuilder error propagation, Tensor::from_array, inputs! macro, try_extract_tensor borrow trap, YOLOv8 output layout
