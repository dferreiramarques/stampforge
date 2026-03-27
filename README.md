# StampForge — Beta

**Browser-based fabric stamp designer — draw, slice, and print in one tool.**

Design stamps directly in the browser, export SVG / STL / GCODE, or send directly to your 3D printer via USB or OctoPrint. Single HTML file, zero dependencies, works fully offline.

> **⚠ This is a public beta.** Features are stable but still being refined. Feedback welcome.

![Version](https://img.shields.io/badge/version-3.0--beta-orange) ![License](https://img.shields.io/badge/license-MIT-green) ![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)

---

## Author & Credits

**David Marques**  
Centro de Inovação Carlos Fiolhais — CDI Portugal  
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
# Open http://localhost:7842 in Chrome or Edge
```

**USB printing on Linux** — add your user to the `dialout` group:
```bash
sudo usermod -a -G dialout $USER
# Log out and back in
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
  → Bezier curve fitting (Schneider algorithm) or Chaikin smoothing
  → Outer / hole classification (even-odd)
  → earcut triangulation (v2.2.4, inlined)
  → Watertight STL / GCODE / SVG
```

### Print settings

| Parameter | Default | Description |
|---|---|---|
| Width / Height (mm) | 60 × 60 | Physical stamp dimensions |
| Resolution | 1200 px | Canvas resolution |
| Layer Height | 0.20 mm | Slice thickness |
| Nozzle Size | 0.40 mm | Extrusion width reference |
| Base Thickness | 1.2 mm | Solid base plate |
| Design Layers | 2 | Raised stamp surface |
| Mirror for stamp | ☐ | Flip X for correct impression |
| Include base plate | ☐ | Add solid base to model |
| Perimeters | 2 | Number of perimeter shells |
| Smooth mode | Bezier fit | Bezier (Schneider) or Chaikin |
| Bezier tolerance | 1.5 | Curve fit precision |
| Bezier tessellation | 12 pts | Points per bezier segment |

### Printer profiles (18 included)

| Brand | Models |
|---|---|
| Prusa | i3 MK3S/MK3S+, MK4, MINI/MINI+ |
| Creality | Ender-3/V2, Ender-3 S1/Pro, CR-10, CR-10 V2/V3 |
| Bambu Lab | P1P, P1S, X1, X1C, A1, A1 Mini |
| Artillery | Sidewinder X1/X2, Genius Pro |
| Voron | 2.4, Trident |
| Anycubic | Kobra, Kobra 2 |
| Elegoo | Neptune 3, Neptune 4 |
| Longer | LK4 Pro (Klipper) |
| Generic | RepRap / Custom |

### G-code engine
- Perimeter paths from smooth bezier-fitted vector contours
- Multiple perimeter shells with inward offset
- Rectilinear infill via scanline ray-casting (alternating direction per layer)
- Correct extrusion: `E = (length × layerH × extW) / filArea`
- Retraction / unretraction between moves
- Auto-centred on printer bed
- Start / end G-code per printer profile

### Layer preview
- Interactive layer-by-layer visualisation before printing
- Slider to navigate layers
- Colour-coded: orange = perimeters, green = infill, red dashed = travels
- Ghost rendering of previous layers for depth context
- Stats: total layers, filament estimate, print time estimate

### USB direct print (Web Serial API)
- Connect directly to printer USB — no drivers, no software
- Line-by-line transmission with Marlin ok handshake (flow control)
- Live log with colour-coded responses
- Progress bar + ETA
- Emergency cancel (M112)
- Port released on close

### OctoPrint integration
- Send GCODE directly to OctoPrint REST API
- Configure host + API key in-app
- Starts print immediately after upload

### Save / Load project
- Saves complete state as .stampforge JSON
- Restores canvas, all settings, printer selection, project name

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
index.html               <- full app (beta) — all features including USB + OctoPrint
stampforge-free.html     <- future free tier — SVG + STL export only
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
- USB print tested with Marlin firmware — Klipper via serial should work but is untested
- USB print requires Chrome or Edge (Web Serial API) — Firefox not supported
- OctoPrint integration requires same-network access or a public OctoPrint URL

---

## Roadmap

- [ ] Free / Pro split — free tier: SVG + STL; Pro tier: direct print + OctoPrint
- [ ] Send directly to OctoPrint from the cloud (Pro)
- [ ] User accounts and saved projects

---

## Changelog

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

MIT — David Marques · Centro de Inovação Carlos Fiolhais · CDI Portugal · 2026
