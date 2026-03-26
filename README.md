# StampForge v3

**Browser-based fabric stamp designer — draw, slice, and print in one tool.**

Design stamps directly in the browser, export SVG/STL/GCODE, or send directly to your 3D printer via USB. Single HTML file, zero dependencies, works fully offline.

![Version](https://img.shields.io/badge/version-3.0-orange) ![License](https://img.shields.io/badge/license-MIT-green) ![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)

---

## Builds

| File | Description |
|---|---|
| `stampforge.html` | Full local version — all features including USB print |
| `stampforge-free.html` | Cloud/Railway version — SVG + STL export only |
| `octoprint-plugin/stampforge-octoprint-plugin.zip` | Plugin for existing OctoPrint installs |
| `octoprint-plugin/stampforge-full-installer.zip` | Full installer — OctoPrint + StampForge from scratch |

---

## Quick start (local)

```bash
# Serve locally (required for USB printing via Web Serial API)
python3 -m http.server 7842
# Open http://localhost:7842/stampforge.html in Chrome or Edge
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
- Scale slider (5%–200%), X/Y offset, colour invert
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
| Resolution | 1200px | Canvas resolution |
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
- Line-by-line transmission with Marlin `ok` handshake (flow control)
- Live log with colour-coded responses
- Progress bar + ETA
- Emergency cancel (`M112`)
- Port released on close

### Save / Load project
- Saves complete state as `.stampforge` JSON
- Restores canvas, all settings, printer selection, project name

---

## Keyboard shortcuts

| Key | Action |
|---|---|
| `P` | Pencil |
| `L` | Line |
| `R` / `Shift+R` | Rectangle stroke / filled |
| `E` / `Shift+E` | Ellipse stroke / filled |
| `F` | Fill |
| `X` | Eraser |
| `T` | Text |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Delete` | Clear canvas |
| `Esc` | Close any modal |

---

## OctoPrint Plugin

For labs with OctoPrint already running:

```bash
unzip stampforge-octoprint-plugin.zip
cd octoprint_stampforge
chmod +x install.sh && ./install.sh
sudo systemctl restart octoprint
```

StampForge appears as a native tab in OctoPrint. The **▶ PRINT** button generates GCODE and sends it directly to the print queue — no API key, no CORS, no separate server.

### Full installer (OctoPrint + StampForge from scratch)

```bash
# Linux
unzip stampforge-full-installer.zip
chmod +x full_installer/install-linux.sh
./full_installer/install-linux.sh

# Windows — run as Administrator
powershell -ExecutionPolicy Bypass -File full_installer\install-windows.ps1

# macOS — double-click
full_installer/install-macos.command
```

---

## File structure

```
stampforge.html              ← entire app (~143KB, single file, offline)
stampforge-free.html         ← cloud build, SVG+STL only
octoprint-plugin/
  stampforge-octoprint-plugin.zip   ← plugin only
  stampforge-full-installer.zip     ← OctoPrint + plugin full install
README.md
```

No build step. No package.json. No node_modules.  
earcut 2.2.4 and bezier fitting are inlined — zero network requests.

---

## Recommended materials for fabric stamps

| Material | Notes |
|---|---|
| TPU 95A | Best ink transfer, flexible, durable |
| Flexible PLA | Good alternative, easier to print |
| Standard PLA | Works, less flexible — good for firm stamps |

Suggested: 100% infill on stamp face, print face-down for best surface quality.

---

## Known limitations (v3)

- Text tool does not follow symmetry axes
- USB print tested with Marlin firmware — Klipper via serial should work but is untested
- OctoPrint plugin geometry issues with complex designs (use standalone + USB instead)

---

## Changelog

### v3.0 (March 2026)
- Bezier curve fitting (Schneider algorithm) replaces Chaikin as default smoothing
- SVG import with scale/offset/invert controls + 4× high-res pipeline
- Layer-by-layer G-code preview with colour-coded move types
- Save/Load project state (.stampforge JSON)
- Multiple perimeter shells with inward offset
- Draggable vertical tool palette (Photoshop-style)
- Light theme for OctoPrint plugin
- Touch + stylus support (touchstart/touchmove/touchend + changedTouches)
- Eraser ghost dot fix
- Removed Google Fonts dependency — fully offline
- OctoPrint plugin with fullscreen overlay modal
- Cross-platform installers: Linux / Windows / macOS

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
- Cura profile import

---

## License

MIT — do whatever you want with it.

---

*Idealized & developed by vibe coding with claude.ai — Centro de Inovação Carlos Fiolhais / CDI Portugal — Março 2026*
