---
title: ort 2.0.0-rc.12 — API Reference & Known Quirks
type: concept
created: 2026-04-28
source: empirical — discovered during Yolobottles inspector build
tags: [ort, onnxruntime, rust, inference]
---

# ort 2.0.0-rc.12 — API Reference & Known Quirks

`ort` is the Rust binding to ONNX Runtime. Version 2.0.0-rc.12 introduced a
completely rewritten API that breaks compatibility with the 1.x series.
This page documents the patterns that work in rc.12 and the traps to avoid.

---

## Cargo.toml

```toml
ort = { version = "2.0.0-rc.12", features = ["download-binaries"] }
```

The `download-binaries` feature auto-downloads the ONNX Runtime prebuilt
binary (~80 MB) on first `cargo build`. Requires internet. No manual DLL
installation needed.

The `ndarray` feature is **not enabled by default**. Without it, ndarray
arrays cannot be passed directly to the `inputs!` macro.

---

## Loading a session

```rust
use ort::session::Session;

let session = Session::builder()
    .map_err(|e| anyhow::anyhow!("{e}"))?
    .with_optimization_level(ort::session::builder::GraphOptimizationLevel::All)
    .map_err(|e| anyhow::anyhow!("{e}"))?
    .with_intra_threads(4)
    .map_err(|e| anyhow::anyhow!("{e}"))?
    .commit_from_file(model_path)
    .map_err(|e| anyhow::anyhow!("{e}"))?;
```

**Trap:** each builder method returns `Result<SessionBuilder, ort::Error<SessionBuilder>>`.
`ort::Error<SessionBuilder>` is **not `Send + Sync`** (it contains raw pointers),
so `?` cannot convert it to `anyhow::Error` via `From`.
Fix: `.map_err(|e| anyhow::anyhow!("{e}"))` on each builder call.

---

## Creating a tensor input

```rust
use ort::value::Tensor;

// (shape_as_i64_array, owned_vec)
let shape = [1i64, 3, 640, 640];
let value = Tensor::from_array((shape, data_vec))
    .map_err(|e| anyhow::anyhow!("{e}"))?;
```

**Trap:** without the `ndarray` feature, passing an `ArrayView4<f32>` to
`inputs!` fails at compile time:
```
the trait `From<ArrayBase<ViewRepr<&f32>, Dim<[usize; 4]>>>` is not implemented
for `SessionInputValue<'_>`
```
Fix: use `Tensor::from_array((shape_i64, vec))` — no ndarray needed.

The shape array must contain `i64` values (or `usize`; both implement `ToShape`).

---

## Running inference

```rust
use ort::inputs;

// session.run() requires &mut self
let outputs = self.session.run(inputs!["images" => value])?;
```

**Trap 1:** `session.run()` requires `&mut self` in rc.12. If the model is
behind `Arc`, use `Arc<parking_lot::Mutex<Model>>` and lock before calling.

**Trap 2:** the `inputs!` macro returns a `Vec` / array directly (not a
`Result`). Do **not** put `?` after `inputs![...]`.

---

## Extracting tensor output

```rust
let output = outputs["output0"].try_extract_tensor::<f32>()?;
let (shape, raw_slice) = output;
// raw_slice: &[f32], borrows from outputs/session

// Copy before dropping outputs, otherwise decode_output (which needs &self)
// cannot borrow self while session is still mutably borrowed
let raw: Vec<f32> = raw_slice.to_vec();
drop(outputs);

let detections = self.decode_output(&raw, orig_w, orig_h);
```

**Trap:** `try_extract_tensor` returns `(&Shape, &[T])` — both slices borrow
from `SessionOutputs`, which in turn borrows `self.session` mutably. Calling
any `&self` method while `outputs` is alive fails to compile.
Fix: `.to_vec()` the slice and `drop(outputs)` explicitly.

---

## Full infer() skeleton

```rust
pub fn infer(&mut self, img: &DynamicImage) -> anyhow::Result<Vec<Detection>> {
    // 1. Preprocess
    let resized = img.resize_exact(640, 640, FilterType::Lanczos3);
    let data = image_to_tensor(&resized.into_rgb8()); // Vec<f32>, BCHW

    // 2. Build ort tensor
    let shape = [1i64, 3, 640, 640];
    let value = Tensor::from_array((shape, data))
        .map_err(|e| anyhow::anyhow!("{e}"))?;

    // 3. Run
    let outputs = self.session.run(inputs!["images" => value])?;

    // 4. Extract
    let (_, raw_slice) = outputs["output0"].try_extract_tensor::<f32>()?;
    let raw = raw_slice.to_vec();
    drop(outputs);

    // 5. Decode
    Ok(self.decode_output(&raw, img.width(), img.height()))
}
```

---

## YOLOv8 output layout

For a model exported with `dynamic=False`, `opset=17`, `batch=1`:

- Output name: `output0`
- Shape: `[1, 4 + nc, 8400]`
- Layout (row-major, column = anchor):
  - `raw[0 * 8400 + i]` → cx (normalized to input size, not [0,1])
  - `raw[1 * 8400 + i]` → cy
  - `raw[2 * 8400 + i]` → w
  - `raw[3 * 8400 + i]` → h
  - `raw[(4 + c) * 8400 + i]` → score for class c
- **No objectness score** — YOLOv8 removed it vs YOLOv5.
- Coordinates are in input-image pixels (0–640). Scale back to original size.

---

## See also

- [[YOLOv8]] — model architecture and training
- [ort crate docs](https://docs.rs/ort/2.0.0-rc.12/ort/) (external)
- [ort GitHub](https://github.com/pykeio/ort) (external)
