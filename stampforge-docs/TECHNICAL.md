# StampForge — Documentação Técnica

**Versão:** 3.0  
**Autor:** David Marques  
**Organização:** Centro de Inovação Carlos Fiolhais / CDI Portugal  
**Licença:** MIT  
**Desenvolvimento:** Vibe coded with claude.ai — Março 2026

---

## Visão Geral

StampForge é uma aplicação web single-file (HTML/CSS/JS, ~145KB) para design de carimbos de tecido com exportação directa para impressão 3D. Não tem dependências externas, funciona offline, e corre em qualquer browser moderno.

```
stampforge.html   ← aplicação completa (USB + GCODE + STL + SVG)
stampforge-free.html ← versão cloud (SVG + STL apenas)
```

---

## Arquitectura

### Single-File Architecture

Toda a aplicação está contida num único ficheiro HTML. Não há build step, npm, ou bundler. As únicas dependências são inlined:

- **earcut 2.2.4** — triangulação de polígonos com holes (inlined, ~4KB)
- **Algoritmo de Schneider** — bezier fitting (implementado de raiz)

```
stampforge.html
├── <style>          CSS com variáveis de tema
├── <body>           HTML: header + canvas area + right panel + modals
└── <script>         ~3000 linhas JS:
    ├── Drawing engine    canvas, tools, symmetry
    ├── Bitmap pipeline   mask → contours → simplify → smooth
    ├── STL engine        earcut → watertight mesh
    ├── GCODE engine      printer profiles → toolpaths
    ├── USB Serial        Web Serial API (Marlin flow control)
    ├── Layer preview     canvas 2D visualiser
    └── UI helpers        toast, modals, save/load
```

### Layout

```
┌─────────────────────────────────────────────────────────┐
│ HEADER: logo · color · size · F/M/G · 💾 📂 · SVG STL PREV GCODE USB │
├──────┬──────────────────────────────────────────────────┤
│      │                                                   │
│ TOOL │           CANVAS AREA                            │ RIGHT
│ PAL  │   [projectTitle]                                 │ PANEL
│ 2col │                                                   │
│      │   [drawCanvas + overlayCanvas]                   │
│      │                                                   │
│      │   [floatPreview]        [zoomInfo]               │
├──────┴──────────────────────────────────────────────────┤
│ STATUS BAR: tool · pos · canvas · scale · credits        │
└─────────────────────────────────────────────────────────┘
```

---

## Pipeline de Exportação

### Bitmap → Geometria Vectorial

```
Canvas pixels (1200×1200px default)
    │
    ▼
getBinaryMask(s)
    ├── Mirror X transform (se mirrorX=true)
    ├── Brightness threshold < 220 → binary (0/1)
    └── Morphological closing R=1px
        ├── Dilate 1px  (fecha gaps de antialiasing)
        └── Erode 1px   (restaura dimensões originais)
    │
    ▼
extractContours(mask, W, H)
    ├── Boundary edge tracing (directed edges)
    ├── Edge map → chain into closed polygons
    └── Returns: array of pixel-coordinate rings
    │
    ▼
dpSimplify(contour, epsilon)
    └── Douglas-Peucker iterativo (stack-based, sem recursão)
    │
    ▼
bezierFitAndTessellate(pts, tolerance, tessN)
    ├── Chord-length parameterisation
    ├── Schneider cubic bezier fitting (recursive split on max error)
    └── Tessellation: N points per bezier segment
    │   (alternativa: chaikin(pts, passes))
    ▼
scaleContour(pts, W, H, physW, physH)
    └── pixels → milímetros
    │
    ▼
Classify outer / holes
    ├── Sort by |area| descending (largest = outermost)
    ├── Point-in-polygon test (ray casting)
    ├── Outers: CCW winding
    └── Holes:  CW winding
```

### STL Export

```
Contours (outers + holes)
    │
    ▼
earcut triangulation
    ├── Flatten to [x,y] array with hole indices
    ├── Returns triangle indices
    └── Handles complex holes correctly (even-odd rule)
    │
    ▼
buildSTL(s)
    ├── Top face    (z = topZ)      — triangles CCW
    ├── Bottom face (z = midZ/0)    — triangles CW (reversed)
    └── Side walls  per contour ring
        ├── 2 triangles per edge segment
        └── Normal vectors computed from edge direction
    │
    ▼
writeBinarySTL(tris)
    └── Binary STL: 80B header + 4B count + 50B/triangle
```

### GCODE Export

```
Contours (vectorial, mm)
    │
    ▼
Multiple perimeters
    ├── Shell 0: original contour
    ├── Shell 1..N: offsetRingBy(ring, n * extW)
    │              centroid-pull inward offset
    └── coalesceRing(ring, 0.25mm) — merge micro-segments
    │
    ▼
Boustrophedon infill
    ├── Scanline ray-casting à pitch = extW / density
    ├── Build all scanlines first
    ├── Connect adjacent lines without retraction (pitch × 2.5 threshold)
    └── Travel only when gap too large
    │
    ▼
Extrusion calculation
    └── E = (length × layerH × extW) / (π × (filDia/2)²)
    │
    ▼
G-code emission
    ├── Start G-code (printer profile, with {nozzle_temp} placeholders)
    ├── Layer loop: Z lift → perimeters → infill
    ├── Fan control at configured layer
    └── End G-code
```

---

## Qualidade de Impressão

Três presets que ajustam simultaneamente múltiplos parâmetros:

| Preset | simplifyEps | Smooth | Perimeters | Speed | ~Tempo |
|--------|-------------|--------|------------|-------|--------|
| DRAFT  | 3.0px | Chaikin 2p | 1 | 100mm/s | ~8min |
| STD    | 1.5px | Bezier tol=1.5 | 2 | 70mm/s | ~15min |
| FINE   | 0.8px | Bezier tol=1.0 | 3 | 40mm/s | ~50min |

---

## Perfis de Impressora

18 perfis embebidos em `PRINTER_PROFILES[]`. Cada perfil contém:

```javascript
{
  id, name,
  bed_x, bed_y,          // dimensões da mesa (mm)
  firmware,              // 'marlin' | 'klipper' | 'bambu' | 'reprap'
  filament,              // diâmetro (mm)
  temp_nozzle, temp_bed,
  speed_print, speed_travel, speed_first,
  retract_len, retract_speed,
  fan_speed, fan_layer,
  start_gcode,           // com placeholders {nozzle_temp} {bed_temp} {z_max}
  end_gcode
}
```

Impressoras incluídas: Prusa MK3S/MK4/MINI, Creality Ender-3/S1/CR-10, Bambu P1P/X1/A1, Artillery Sidewinder/Genius, Voron 2.4/Trident, Anycubic Kobra, Elegoo Neptune, Longer LK4 Pro, Generic RepRap.

---

## Web Serial API (USB Print)

Flow control Marlin linha-a-linha:

```
usbConnect()
    └── navigator.serial.requestPort()
        └── port.open({ baudRate: 115200 })
            └── _readLoop() — background TextDecoderStream reader

usbStartPrint()
    ├── generateGcode() → _gcodeLines[]
    └── loop:
        ├── _sendLine(line)     → port.writable writer
        ├── _waitForOk()        → Promise resolved by _onSerialLine()
        └── _onSerialLine():    parses 'ok', errors, temps

usbPurge()
    └── navigator.serial.getPorts() → close all known ports
```

**Requisitos:** Chrome ou Edge. HTTPS ou localhost. Linux: grupo `dialout`.

---

## SVG Import Pipeline

Quando um SVG é importado e confirmado, `_svgActive = true`.

Nos exports subsequentes, `buildContours()` detecta o flag e usa `getSVGMask()` em vez de `getBinaryMask()`:

```
getSVGMask(s, scale=4)
    ├── Blob URL do SVG original
    ├── Renderiza em canvas 4× resolução (ex: 4800×4800px)
    ├── Morphological closing R=4px (proporcional ao scale)
    └── Retorna { mask, W, H, scale: 4 }

buildContours(s)
    └── dpSimplify epsilon × scale (compensa resolução extra)
```

O flag é limpo em `clearCanvas()` e `importImage()`.

---

## Layer Preview

`buildLayerData(s, printer)` replica o engine do GCODE mas em vez de emitir texto, acumula geometria por layer:

```javascript
layer = {
  z,          // altura Z (mm)
  isBase,     // true = base plate layer
  perimeters, // array de rings [[{x,y}, ...], ...]
  infill,     // array de segmentos [[{x,y},{x,y}], ...]
  travels,    // array de segmentos (para visualização)
  filament,   // mm extrudidos neste layer
  time,       // segundos estimados
  settings,   // s (para escalar no render)
  allRings    // outers + holes para fill even-odd
}
```

O render usa `Canvas 2D` com even-odd fill para mostrar holes correctamente.

---

## Estrutura de Ficheiros

```
stampforge/
├── stampforge.html              # app completa
├── stampforge-free.html         # versão cloud (sem USB/GCODE)
├── README.md
├── .gitignore
└── octoprint-plugin/
    ├── stampforge-octoprint-plugin.zip
    │   ├── octoprint_stampforge/__init__.py
    │   ├── static/js/stampforge.js
    │   ├── static/css/stampforge.css
    │   ├── templates/stampforge_tab.jinja2
    │   ├── setup.py
    │   ├── install.sh / install.bat / install.command
    │   └── README.md
    └── stampforge-full-installer.zip
        ├── install-linux.sh
        ├── install-windows.ps1
        ├── install-macos.command
        └── plugin/ (mesmo conteúdo acima)
```

---

## Variáveis de Estado Globais

```javascript
let tool = 'pencil'          // ferramenta activa
let color = '#000000'        // cor actual
let brushSize = 6            // px
let isDrawing = false
let startX, startY           // início do shape actual
let lastX, lastY             // ponto anterior (pencil/eraser)
let symH = false, symV = false  // eixos de simetria
let undoStack = [], redoStack = []
let _svgDoc, _svgImg, _svgSrc, _svgActive  // SVG import state
let _layerData = null        // layer preview cache
let _port, _reader           // Web Serial
let _printing, _cancelled    // USB print state
let _drawMode = 'stroke'     // comportamento da máscara
let _infillDensity = 0.25    // controlado pelo quality preset
let _printQuality = 'standard'
```

---

## Notas de Implementação

### Douglas-Peucker Iterativo
A implementação usa stack explícita em vez de recursão para evitar stack overflow em contornos com muitos pontos (canvas 1200px pode ter 5000+ pontos por contorno).

### Bezier Fitting (Schneider)
Implementação simplificada do algoritmo An Algorithm for Automatically Fitting Digitized Curves (Schneider 1990). Usa chord-length parameterisation e splitting recursivo no ponto de maior erro. Profundidade máxima: 8 níveis.

### Coalescência de Segmentos
Antes de emitir G-code, `coalesceRing(ring, 0.25)` remove pontos consecutivos a menos de 0.25mm. O Cura tem segmentos médios de ~5mm; sem coalescência o StampForge gerava segmentos médios de 0.08mm (98% abaixo de 0.5mm), tornando a impressão muito lenta.

### Boustrophedon sem Travel
O infill conecta linhas adjacentes com um move sub-extrudido (30% da extrusão normal) em vez de retracção + travel, quando a distância ao próximo ponto de partida é inferior a `pitch × 2.5`. Reduz drasticamente o número de retrações e o tempo de impressão.

---

*StampForge v3 — David Marques / CDI Portugal — MIT License — 2026*
