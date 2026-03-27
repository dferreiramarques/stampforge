# StampForge — Guia de Utilizador

**Versão 3.0 · CDI Portugal · 2026**

---

## O que é o StampForge?

StampForge é uma aplicação web para desenhar carimbos de tecido e enviá-los directamente para impressão 3D. Abre no browser, não precisa de instalação, e funciona offline.

**Fluxo típico:**
```
Desenha → Ajusta parâmetros → Export STL/GCODE → Imprime via USB
```

---

## Interface

### Header (topo)
- **COLOR** — cor do pincel
- **SIZE** — espessura em pixels
- **F · M · G** — presets de espessura: Fino (2px), Médio (6px), Grosso (16px)
- **💾 📂** — guardar / carregar projecto (.stampforge)
- **SVG** — exportar SVG vectorial
- **STL** — exportar modelo 3D
- **PREV** — preview das layers de impressão
- **GCODE** — exportar G-code para o slicer
- **USB** — imprimir directamente via USB

### Paleta de ferramentas (esquerda, arrastável)

| Ícone | Tecla | Função |
|-------|-------|--------|
| ✏ | P | Lápis — traço livre |
| ⬜ | X | Borracha |
| ╱ | L | Linha recta |
| ◪ | F | Preenchimento (flood fill) |
| ▭ | R | Rectângulo (contorno) |
| ▬ | Shift+R | Rectângulo (preenchido) |
| ◯ | E | Elipse (contorno) |
| ⬤ | Shift+E | Elipse (preenchida) |
| A | T | Texto |
| ↩ | Ctrl+Z | Desfazer |
| ↪ | Ctrl+Y | Refazer |
| ✕ | Delete | Limpar canvas |
| ⬆ | — | Importar imagem / SVG |
| SVG | — | Importar SVG |
| ⇔ | — | Simetria esquerda/direita |
| ⇕ | — | Simetria cima/baixo |

**A paleta é arrastável** — agarra pelo handle `· · ·` no topo e move para qualquer posição.

### Canvas
- **Nome do projecto** — clica em "untitled" para renomear (usado nos ficheiros exportados)
- **Zoom** — scroll do rato ou pinch no touchpad
- **Stamp Preview** — miniatura no canto inferior esquerdo, mostra simulação de impressão em tecido

### Painel direito

#### Physical Size
- Width / Height (mm) — dimensões físicas do carimbo
- Resolution — resolução do canvas (1200px recomendado)

#### Print Settings
- **DRAFT / STD / FINE** — qualidade de impressão (afecta velocidade, perimetros e suavização)
- Layer Height, Nozzle Size, Base Thickness, Design layers
- Mirror for stamp — espelha para a impressão ficar correcta no tecido
- Include base plate — adiciona base sólida ao modelo
- Perimeters — número de shells do perimetro
- Simplify (px) — simplificação dos contornos
- Curve smooth — Bezier fit ou Chaikin, com tolerância e tessellation

#### Printer Profile
- Selecciona a impressora (18 perfis incluídos)
- Temperaturas, velocidades, retracção e diâmetro de filamento
- Actualizam automaticamente ao mudar de impressora

---

## Fluxo de Trabalho

### 1. Desenhar

Usa as ferramentas da paleta. O canvas tem fundo branco — o preto é o que vai ser impresso.

**Dicas:**
- Usa **simetria** (⇔ ⇕) para formas simétricas — desenha metade e a outra aparece automaticamente
- O **Grosso (G)** é bom para formas orgânicas rápidas
- O **Médio (M)** para detalhes
- O **Fino (F)** para texto e linhas finas

### 2. Importar SVG ou imagem

Clica em ⬆ ou SVG na paleta. Para SVGs, o StampForge rasteriza a 4× resolução para traçar contornos limpos.

**Atenção:** após importar SVG, os exports usam o SVG original em alta resolução — não o canvas. Para voltar ao modo normal, clica em Clear (✕).

### 3. Ajustar parâmetros

- **Dimensões físicas** — define o tamanho real do carimbo (ex: 60×60mm)
- **Qualidade** — DRAFT para testes rápidos (~8min), FINE para produção (~50min)
- **Impressora** — selecciona o perfil correcto para o teu hardware

### 4. Preview de layers

Clica em **PREV** para ver o G-code layer a layer antes de imprimir:
- 🟠 Laranja = perimetros
- 🟢 Verde = infill
- 🔴 Vermelho tracejado = travels (moveimentos sem extrusão)

### 5. Exportar

| Botão | Ficheiro | Para quê |
|-------|----------|----------|
| SVG | .svg | Corte a laser / vinyl |
| STL | .stl | Abrir no Cura, PrusaSlicer |
| GCODE | .gcode | Copiar para SD card ou enviar por rede |
| USB | — | Imprimir directamente (ver secção USB) |

### 6. Imprimir via USB

1. Liga a impressora ao computador via USB
2. Clica **USB** no header
3. Clica **🔌 CONNECT USB** → selecciona a porta no browser
4. Clica **▶ PRINT**

Se der erro de porta ocupada, clica **↺ PURGE** para libertar a porta e tenta de novo.

**Requisitos:** Chrome ou Edge (não Firefox). Linux: adicionar ao grupo `dialout` (ver guia de instalação).

---

## Qualidade de Impressão

### DRAFT (~8 min)
- Simplificação agressiva — formas mais suaves
- 1 perimetro, velocidade 100mm/s
- Para testes e protótipos

### STD (~15 min)
- Qualidade equilibrada
- 2 perimetros, velocidade 70mm/s
- Para maioria dos casos

### FINE (~50 min)
- Máximo detalhe
- 3 perimetros, velocidade 40mm/s
- Para designs complexos e produção final

---

## Guardar e Carregar Projectos

**Guardar (💾):** cria um ficheiro `.stampforge` com o estado completo — canvas, todas as definições, impressora seleccionada e nome do projecto.

**Carregar (📂):** restaura exactamente o estado guardado, incluindo o canvas.

O ficheiro é JSON legível — podes partilhar projectos entre dispositivos.

---

## Materiais Recomendados

| Material | Notas |
|----------|-------|
| **TPU 95A** | Melhor transferência de tinta, flexível, durável |
| **PLA Flexível** | Boa alternativa, mais fácil de imprimir |
| **PLA Standard** | Funciona, menos flexível — bom para carimbos firmes |

**Configurações sugeridas:**
- 100% infill na face do carimbo
- Imprimir com a face para baixo (melhor acabamento)
- Layer height 0.2mm

---

## Atalhos de Teclado

| Tecla | Acção |
|-------|-------|
| P | Lápis |
| L | Linha |
| R / Shift+R | Rectângulo contorno / preenchido |
| E / Shift+E | Elipse contorno / preenchida |
| F | Fill |
| X | Borracha |
| T | Texto |
| Ctrl+Z | Desfazer |
| Ctrl+Y | Refazer |
| Delete | Limpar canvas |
| Esc | Fechar modal |

> Os atalhos são desactivados quando o nome do projecto está em edição.

---

*StampForge v3 — David Marques / CDI Portugal — MIT License — 2026*
