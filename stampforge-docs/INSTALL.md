# StampForge — Guia de Instalação e Deploy

---

## Opções de Deploy

| Opção | Complexidade | USB Print | Requer servidor |
|-------|-------------|-----------|-----------------|
| Ficheiro local (file://) | ⭐ | ✗ | Não |
| Localhost Python | ⭐⭐ | ✓ | Não |
| Railway (cloud) | ⭐⭐ | ✓ (HTTPS) | Railway |
| OctoPrint plugin | ⭐⭐⭐ | ✓ | OctoPrint |

---

## Opção 1 — Ficheiro Local (mais simples)

Abre directamente no browser. USB print não disponível (Web Serial requer HTTPS ou localhost).

```bash
# Basta abrir o ficheiro
# macOS
open stampforge.html

# Linux
xdg-open stampforge.html

# Windows
start stampforge.html
```

SVG, STL e GCODE funcionam normalmente.

---

## Opção 2 — Localhost com Python (USB activo)

### Linux / macOS

```bash
# Pré-requisito: Python 3 (já incluído na maioria dos sistemas)
cd ~/Downloads/stampforge
python3 -m http.server 7842

# Abre no browser
# http://localhost:7842/stampforge.html
```

### Linux — Permissão USB (uma única vez)

```bash
sudo usermod -a -G dialout $USER
# Faz logout e login novamente
groups  # confirma que 'dialout' aparece na lista
```

### Windows

```cmd
cd %USERPROFILE%\Downloads\stampforge
python -m http.server 7842
```

Abre `http://localhost:7842/stampforge.html` no Chrome ou Edge.

### macOS

```bash
cd ~/Downloads/stampforge
python3 -m http.server 7842
```

Abre `http://localhost:7842/stampforge.html` no Chrome ou Edge.

> **Nota:** Safari não suporta Web Serial API. Usa Chrome ou Edge.

---

## Opção 3 — Instalador Completo (OctoPrint + StampForge)

O instalador instala o OctoPrint e o plugin StampForge de raiz.

### Linux (Mint, Ubuntu, Debian, Raspberry Pi OS)

```bash
unzip stampforge-full-installer.zip
cd full_installer
chmod +x install-linux.sh
./install-linux.sh
```

O instalador:
- Instala dependências do sistema (`python3-venv`, `build-essential`, etc.)
- Cria ambiente virtual em `~/.local/share/OctoPrint/venv`
- Instala OctoPrint ≥ 1.9.0
- Instala plugin StampForge
- Cria serviço systemd (auto-start no arranque)
- Cria atalho no menu de aplicações
- Adiciona alias `stampforge` ao bash/zsh
- Adiciona utilizador ao grupo `dialout`

Após instalação:
```bash
sudo systemctl start octoprint
# Abre http://localhost:5000
```

### Windows 10/11

Clique direito em `install-windows.ps1` → **Executar com PowerShell como Administrador**

Ou via terminal:
```powershell
powershell -ExecutionPolicy Bypass -File install-windows.ps1
```

O instalador:
- Descarrega Python 3.11 se necessário
- Cria ambiente virtual em `%LOCALAPPDATA%\OctoPrint\venv`
- Instala OctoPrint + plugin StampForge
- Cria atalho no Desktop e menu Iniciar
- Adiciona regra de firewall para porta 5000

### macOS (Monterey, Ventura, Sonoma — Intel + Apple Silicon)

Duplo clique em `install-macos.command`

Se bloqueado pelo Gatekeeper: clique direito → Abrir

O instalador:
- Instala Homebrew e Python 3.11 se necessário
- Cria ambiente virtual em `~/Library/Application Support/OctoPrint/venv`
- Instala OctoPrint + plugin StampForge
- Cria `~/Applications/StampForge.app`
- Cria serviço launchd
- Adiciona alias `stampforge` ao zsh/bash

---

## Opção 4 — Plugin OctoPrint (OctoPrint já instalado)

Se já tens OctoPrint instalado:

```bash
unzip stampforge-octoprint-plugin.zip
cd octoprint_stampforge

# Linux / macOS
chmod +x install.sh
./install.sh

# Windows
install.bat

# macOS (duplo clique)
install.command
```

Após instalação, reinicia o OctoPrint:
```bash
# Linux com systemd
sudo systemctl restart octoprint

# Via interface: OctoPrint → Settings → Server → Restart
```

O StampForge aparece como tab nativa no OctoPrint. Para usar, clica em **⊞ OPEN STAMPFORGE** para abrir em fullscreen.

---

## Opção 5 — Railway (deploy cloud)

### Pré-requisitos
- Conta Railway (railway.app)
- Git instalado

### Deploy

```bash
unzip stampforge-railway.zip
cd stampforge-railway

git init
git add .
git commit -m "StampForge v3 — Railway deploy"

# Via Railway CLI
railway login
railway new --name stampforge
railway up

# Ou via GitHub
# Push para o teu repo → liga ao Railway → deploy automático
```

### Estrutura do pacote Railway

```
stampforge-railway/
├── index.html          ← app completa (servida em /)
├── stampforge-free.html
├── serve.py            ← servidor Python (lê $PORT)
├── railway.toml        ← config Railway
├── nixpacks.toml       ← força Python provider
└── README.md
```

O Railway atribui HTTPS automático — Web Serial API (USB print) funciona sem configuração adicional no Windows e macOS.

---

## Verificar Instalação

### Funcionalidades base
1. Abre o StampForge
2. Desenha qualquer forma
3. Clica **STL** — deve descarregar um ficheiro `.stl`
4. Abre o STL no Cura ou PrusaSlicer — deve aparecer a forma

### USB Print
1. Liga a impressora via USB
2. Abre `http://localhost:PORT/stampforge.html` (não `file://`)
3. Clica **USB** → **🔌 CONNECT USB**
4. Selecciona a porta no diálogo do browser
5. Clica **▶ PRINT**

Se o botão CONNECT não aparecer ou der erro imediatamente:
- Confirma que estás a usar Chrome ou Edge (não Firefox)
- Confirma que o URL é `localhost` ou `https://` (não `file://`)
- Linux: confirma que estás no grupo `dialout` (`groups | grep dialout`)

---

## Desinstalar

### Linux (instalador completo)
```bash
sudo systemctl stop octoprint
sudo systemctl disable octoprint
rm -rf ~/.local/share/OctoPrint
rm ~/.local/share/applications/octoprint-stampforge.desktop
```

### Plugin OctoPrint
OctoPrint → Settings → Plugin Manager → StampForge → Uninstall

### Windows
Apaga `%LOCALAPPDATA%\OctoPrint` e o atalho do Desktop.

### macOS
```bash
rm -rf ~/Applications/StampForge.app
rm -rf ~/Library/Application\ Support/OctoPrint
launchctl unload ~/Library/LaunchAgents/com.cicf.stampforge.plist
```

---

*StampForge v3 — David Marques / CDI Portugal — MIT License — 2026*
