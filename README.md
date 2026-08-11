# StampForge — Beta

**Browser-based fabric stamp designer — draw a design, export a print-ready STL.**

Design stamps directly in the browser and export a watertight STL, ready to slice and print with any 3D printer / slicer. Single HTML file, zero dependencies, works fully offline.

> **⚠ This is a public beta.** Features are stable but still being refined. Feedback welcome.
>
> This release is intentionally simplified to the core design → STL workflow. In-app G-code generation, printer profiles, USB printing and OctoPrint integration are still in the codebase (commented out) and planned for a future release — see [Planned for a future release](#planned-for-a-future-release) below.

![Version](https://img.shields.io/badge/version-3.1--beta-orange) ![License](https://img.shields.io/badge/license-MIT-green) ![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)

---

## Author & Credits

**David Marques**  
MIT License — 2026

---

## Quick start (Railway / cloud)

The app runs as a single static HTML file served by a minimal Python server.  
Deploy to Railway and open the URL — no configuration needed.

```
railway up
```

---

## Quick start (local)

```bash
python3 -m http.server 7842
# Open http://localhost:7842 in any modern browser
```

---

## Features

### Drawing tools
- **Pencil** — freehand stroke (mouse + touch + stylus)
- **Line, Rectangle, Ellipse** — geometric shapes, stroke or filled
- **Fill** — flood fill
- **Eraser** — clean erase without ghost dots
- **Text** — place text with system fonts
- Undo / Redo / Clear / Import raster image / Import SVG
- **Symmetry axes** — ⇔ left/right, ⇕ top/bottom, or both simultaneously
- **Inline project name** — click "untitled" on canvas to rename
- **Draggable tool palette** — Photoshop-style vertical 2-column palette, drag anywhere

### SVG Import
- Load any SVG file as drawing layer
- Scale slider (5–200 %), X/Y offset, colour invert
- Preview before placing on canvas
- High-res pipeline: SVG rasterised at 4× resolution for clean contour tracing

### Export pipeline
```
Canvas pixels (or SVG at 4× resolution)
  → Binary mask  (morphological closing)
  → Boundary edge tracing
  → Douglas-Peucker simplification
  → Chaikin smoothing
  → Outer / hole classification (even-odd)
  → earcut triangulation (v2.2.4, inlined)
  → Watertight STL
```

### Model settings

| Parameter | Default | Description |
|---|---|---|
| Width / Height (mm) | 60 × 60 | Physical stamp dimensions |
| Resolution | 600 px | Canvas resolution |
| Layer Height (mm) | 0.20 | Relief step height, feeds mesh geometry |
| Base Thickness | 1.2 mm | Solid base plate |
| Design Layers | 2 | Raised stamp surface |
| Mirror for stamp | ☐ | Flip X for correct impression |
| Include base plate | ☐ | Add solid base to model |
| Simplify (px) | 0.8 | Contour simplification tolerance |
| Curve smooth | 3 passes | Chaikin smoothing passes |

### Save / Load project
- Saves complete state as .stampforge JSON
- Restores canvas, all settings, project name

---

## Planned for a future release

The following were part of the original beta and are still present in `index.html` (commented out, marked `FUTURE RELEASE`), but are disabled in this build to keep the product focused on the core design → STL workflow:

- **G-code engine** — perimeters, bezier-fitted contours, rectilinear infill, retraction, printer start/end G-code
- **18 printer profiles** — Prusa, Creality, Bambu Lab, Artillery, Voron, Anycubic, Elegoo, Longer, generic RepRap
- **Layer-by-layer print preview** — slider, perimeter/infill/travel visualisation, filament & time estimates
- **USB direct print** — Web Serial API connection straight to the printer (Marlin flow control)
- **OctoPrint integration** — upload + start print via the OctoPrint REST API
- **SVG export** and **print-quality presets** (draft/standard/fine)

Re-enabling any of these is a matter of un-commenting the relevant block and restoring its UI — nothing was deleted.

---

## Keyboard shortcuts

| Key | Action |
|---|---|
| P | Pencil |
| L | Line |
| R / Shift+R | Rectangle stroke / filled |
| E / Shift+E | Ellipse stroke / filled |
| F | Fill |
| X | Eraser |
| T | Text |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Delete | Clear canvas |
| Esc | Close any modal |

---

## Recommended materials for fabric stamps

| Material | Notes |
|---|---|
| TPU 95A | Best ink transfer, flexible, durable |
| Flexible PLA | Good alternative, easier to print |
| Standard PLA | Works, less flexible — good for firm stamps |

Suggested: 100% infill on stamp face, print face-down for best surface quality.

---

## File structure

```
index.html               <- the app — draw + export STL (print/G-code code kept, disabled — see "Planned for a future release")
stampforge-free.html     <- earlier free-tier draft, superseded by the above
serve.py                 <- minimal Python static server (Railway)
railway.toml             <- Railway deploy config
nixpacks.toml            <- Railway build config
README.md
INSTALL.md
USER_GUIDE.md
TECHNICAL.md
OCTOPRINT_API.md
```

No build step. No package.json. No node_modules.
earcut 2.2.4 and Bezier fitting are inlined — zero network requests at runtime.

---

## Known limitations (beta)

- Text tool does not follow symmetry axes
- G-code generation, printer profiles, USB printing and OctoPrint are disabled in this release (see [Planned for a future release](#planned-for-a-future-release))

---

## Roadmap

- [ ] Re-enable direct print (USB + OctoPrint) as an opt-in "Pro" workflow once G-code output has had more testing
- [ ] User accounts and saved projects

---

## Changelog

### v3.1 (August 2026)
- Simplified to a single focused workflow: draw → export STL
- Removed printing UI from the app (G-code export, printer profiles, USB print, OctoPrint, layer preview, SVG export) — code kept in place, commented out, for a future release
- Fixed a bug where the toast notification helper was never defined, which left the STL export button stuck disabled after use
- New colour palette aligned to the shared design system (Figtree/Fluent 2 tokens, Laranja accent)

### v3.0-beta (March 2026)
- Bezier curve fitting (Schneider algorithm) replaces Chaikin as default smoothing
- SVG import with scale/offset/invert controls + 4x high-res pipeline
- Layer-by-layer G-code preview with colour-coded move types
- Save/Load project state (.stampforge JSON)
- Multiple perimeter shells with inward offset
- Draggable vertical tool palette (Photoshop-style)
- Touch + stylus support
- Eraser ghost dot fix
- Removed Google Fonts dependency — fully offline
- OctoPrint modal with host + API key config
- Public beta release on Railway

### v2.0
- 18 printer profiles with auto-fill
- Native G-code engine (perimeters + infill + retraction)
- USB direct print via Web Serial API (Marlin flow control)
- OctoPrint REST API integration

### v1.0
- Canvas drawing tools (pencil, line, rect, ellipse, fill, eraser, text)
- Symmetry axes (H + V)
- Inline project name
- Watertight STL export (earcut triangulation)
- SVG export

---

## License

MIT — David Marques · 2026
