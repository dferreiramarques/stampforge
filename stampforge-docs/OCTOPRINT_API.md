# StampForge OctoPrint Plugin — Documentação

**Plugin ID:** `stampforge`  
**Versão:** 3.0.0  
**Compatibilidade OctoPrint:** ≥ 1.8.0  
**Python:** ≥ 3.7  
**Licença:** MIT

---

## Arquitectura do Plugin

```
octoprint_stampforge/
├── __init__.py                     ← Plugin class + Blueprint routes
├── templates/
│   └── stampforge_tab.jinja2       ← Tab HTML (launcher + fullscreen overlay)
└── static/
    ├── js/stampforge.js            ← App JS completa
    └── css/stampforge.css          ← Estilos (tema claro)
```

O plugin regista-se no OctoPrint como:
- `SettingsPlugin` — configurações persistentes
- `AssetPlugin` — serve JS e CSS estáticos
- `TemplatePlugin` — adiciona tab à UI
- `BlueprintPlugin` — expõe endpoints REST próprios

---

## Interface na UI OctoPrint

A tab **StampForge** aparece na barra de navegação principal do OctoPrint ao lado de Temperature, Control, GCode Viewer, etc.

### Estado inicial (launcher)
```
┌────────────────────────────────┐
│  STAMPFORGE                    │
│  3D Stamp Designer · CDI       │
│                                │
│  [⊞ OPEN STAMPFORGE]          │
│                                │
│  v3.0.0 · CDI Portugal        │
└────────────────────────────────┘
```

### Modo fullscreen
- Overlay `position:fixed; inset:0; z-index:99999` cobre completamente o OctoPrint
- Botão **✕ CLOSE STAMPFORGE** no canto inferior direito (ou ESC)
- Canvas inicializa lazy — apenas quando o overlay abre pela primeira vez
- `fitCanvas()` é chamado nas aberturas seguintes

### Botão de impressão
O header da versão plugin tem **▶ PRINT** em vez dos botões USB e OctoPrint separados. Usa `octoPrintNative()` que envia via `OctoPrint.files.upload()`.

---

## Endpoints do Plugin

Base URL: `/api/plugin/stampforge/`

### POST /print
Recebe G-code e envia para a impressora via OctoPrint.

**Nota:** Implementado mas substituído pela abordagem `OctoPrint.files.upload()` no lado do cliente, que é mais robusta e não tem problemas de CSRF.

**Request:**
```json
{
  "filename": "meu-stamp_60x60mm.gcode",
  "gcode": "; G-code content...\nG28\n..."
}
```

**Response (200):**
```json
{
  "status": "ok",
  "filename": "meu-stamp-60x60mm.gcode",
  "lines": 1842
}
```

**Response (400):**
```json
{ "error": "Empty GCODE" }
```

**Response (500):**
```json
{ "error": "mensagem de erro" }
```

### CSRF
O plugin tem `is_blueprint_csrf_protected() = False` para permitir POST do JS sem token CSRF de sessão.

Para o upload de ficheiros, o JS usa `OctoPrint.files.upload()` que é o cliente nativo do OctoPrint e gere CSRF automaticamente.

---

## Configurações

Acessíveis via OctoPrint Settings → StampForge.

```python
{
  "auto_select": True,   # selecciona ficheiro após upload
  "auto_print": True,    # inicia impressão após selecção
}
```

Acesso em Python:
```python
self._settings.get(["auto_select"])
self._settings.get(["auto_print"])
```

---

## Template Variables

O template Jinja2 recebe:

```python
def get_template_vars(self):
    return dict(
        api_key=self._settings.global_get(["api", "key"])
    )
```

Usado no JS como:
```javascript
window.OCTOPRINT_APIKEY = "{{ api_key }}";
```

---

## Assets

```python
def get_assets(self):
    return dict(
        js=["js/stampforge.js"],
        css=["css/stampforge.css"],
    )
```

URL em templates:
```jinja2
{{ url_for('plugin.stampforge.static', filename='js/stampforge.js') }}
{{ url_for('plugin.stampforge.static', filename='css/stampforge.css') }}
```

---

## Função de Impressão (JS)

```javascript
async function octoPrintNative() {
  // Gera G-code usando o engine interno
  const gcode = await generateGcode(s, printer);

  // Cria File object
  const file = new File([gcode], filename, { type: 'text/plain' });

  // Upload via cliente nativo OctoPrint (trata CSRF automaticamente)
  OctoPrint.files.upload('local', file, { select: true, print: true })
    .done(() => showToast('✓ Printing: ' + filename))
    .fail(resp => showToast('ERROR: ' + resp.status));
}
```

O `OctoPrint.files.upload()` é o mesmo cliente usado pela UI nativa do OctoPrint — herda a sessão autenticada e o token CSRF, sem necessidade de API key explícita.

---

## Tema (CSS)

O plugin usa um **tema claro** (ao contrário da versão standalone que é escura) para melhor legibilidade dentro do OctoPrint.

Variáveis CSS scoped sob `#sf-app`:
```css
#sf-app {
  --bg:       #f0f0ec;
  --s1:       #e4e4de;
  --s2:       #ffffff;
  --s3:       #f8f8f5;
  --border:   #ccccc4;
  --acc:      #e06010;   /* laranja */
  --text:     #1a1a18;
  --dim:      #777770;
  --canvas-bg:#ffffff;
}
```

Todos os selectores são prefixados com `#sf-app` para não colidir com os estilos do OctoPrint.

---

## Desenvolvimento Local

Para desenvolver o plugin sem reinstalar:

```bash
# Activa o venv do OctoPrint
source ~/.local/share/OctoPrint/venv/bin/activate

# Instala em modo editable
pip install -e /caminho/para/octoprint_stampforge

# Reinicia OctoPrint
sudo systemctl restart octoprint
```

Para editar o JS/CSS sem reiniciar o OctoPrint, edita os ficheiros em `static/` directamente — são servidos sem cache em modo debug.

---

## Reinstalar / Actualizar

```bash
cd octoprint_stampforge
./install.sh   # Linux/macOS
install.bat    # Windows
```

O script detecta o Python do OctoPrint automaticamente nos locais mais comuns:
- `~/.local/share/OctoPrint/venv/bin/python`
- `~/OctoPrint/venv/bin/python`
- `/home/pi/oprint/bin/python`

---

## Limitações Conhecidas

- **Geometria complexa** — designs muito complexos com muitos holes podem falhar na triangulação dentro do OctoPrint (contexto de execução diferente do standalone). Para estes casos, usa o `stampforge.html` standalone com USB directo.
- **Sessão** — o overlay fullscreen partilha a sessão do OctoPrint. Se o OctoPrint fizer logout, o `▶ PRINT` para de funcionar.
- **Tamanho do G-code** — G-codes muito grandes (>5MB) podem ter timeout no upload via `OctoPrint.files.upload()`. Usa qualidade DRAFT ou STD para reduzir o tamanho.

---

*StampForge OctoPrint Plugin v3.0.0 — David Marques / CDI Portugal — MIT License — 2026*
