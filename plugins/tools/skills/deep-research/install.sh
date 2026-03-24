#!/bin/bash
# Deep Research Skill - One-Click Installer
# Installs all dependencies for automated YouTube + Web research with NotebookLM

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Get the directory where this script is located
SKILL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SKILL_DIR"

# Welcome banner
clear
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           🔬 Deep Research Skill - Installation               ║
║                                                               ║
║   Automated research combining 50+ YouTube videos            ║
║   and 20+ web articles into comprehensive summaries          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

log_info "This installer will set up everything you need:"
echo "  • Python dependencies (yt-dlp, notebooklm-py, beautifulsoup4, etc.)"
echo "  • Node.js/Deno (required by yt-dlp for YouTube)"
echo "  • Playwright browser automation"
echo "  • NotebookLM authentication"
echo "  • Vault directory for research outputs"
echo ""
read -p "Press Enter to begin installation..."

# ============================================================
section "1/6: System Check"
# ============================================================

log_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 not found"
    echo ""
    echo "Please install Python 3.8 or later:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
log_success "Python 3 found: v${PYTHON_VERSION}"

log_info "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    log_error "pip3 not found"
    echo ""
    echo "Please install pip3:"
    echo "  macOS: python3 -m ensurepip --upgrade"
    echo "  Ubuntu: sudo apt install python3-pip"
    echo ""
    exit 1
fi
log_success "pip3 found"

# ============================================================
section "2/6: Python Dependencies"
# ============================================================

log_info "Installing Python packages from requirements.txt..."
echo ""

if pip3 install -r scripts/requirements.txt; then
    log_success "All Python dependencies installed successfully"
else
    log_error "Failed to install Python dependencies"
    echo ""
    echo "Try running manually:"
    echo "  pip3 install -r scripts/requirements.txt"
    echo ""
    exit 1
fi

# ============================================================
section "3/6: YouTube Extractor (yt-dlp)"
# ============================================================

log_info "Checking yt-dlp installation..."
if ! command -v yt-dlp &> /dev/null; then
    log_info "Installing yt-dlp..."
    if pip3 install -U yt-dlp; then
        log_success "yt-dlp installed successfully"
    else
        log_error "Failed to install yt-dlp"
        exit 1
    fi
else
    YT_DLP_VERSION=$(yt-dlp --version)
    log_success "yt-dlp already installed: v${YT_DLP_VERSION}"
fi

# Check for Node.js or Deno (required by yt-dlp for YouTube)
log_info "Checking for Node.js or Deno (required by yt-dlp)..."
HAS_JS_RUNTIME=false

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    log_success "Node.js found: ${NODE_VERSION}"
    HAS_JS_RUNTIME=true
elif command -v deno &> /dev/null; then
    DENO_VERSION=$(deno --version | head -1)
    log_success "Deno found: ${DENO_VERSION}"
    HAS_JS_RUNTIME=true
fi

if [ "$HAS_JS_RUNTIME" = false ]; then
    log_warning "Neither Node.js nor Deno found"
    echo ""
    echo "yt-dlp requires Node.js or Deno to download from YouTube."
    echo ""
    echo "Install options:"
    echo "  macOS:  brew install node"
    echo "  Ubuntu: sudo apt install nodejs"
    echo "  Alternative: brew install deno"
    echo ""
    read -p "Do you want to continue without it? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_error "Installation cancelled"
        exit 1
    fi
    log_warning "Continuing without JS runtime - YouTube downloads may fail"
fi

# ============================================================
section "4/6: Playwright Browser Automation"
# ============================================================

log_info "Installing Playwright browsers (required for NotebookLM)..."
echo ""
echo "This will download Chromium browser (~300MB)..."
echo ""

if playwright install chromium; then
    log_success "Playwright Chromium installed successfully"
else
    log_error "Failed to install Playwright browsers"
    echo ""
    echo "Try running manually:"
    echo "  playwright install chromium"
    echo ""
    exit 1
fi

# ============================================================
section "5/6: NotebookLM Authentication"
# ============================================================

log_info "Setting up NotebookLM authentication..."
echo ""
echo "NotebookLM will open a browser window for Google authentication."
echo "Please sign in with your Google account."
echo ""
read -p "Press Enter to open authentication browser..."

if notebooklm login; then
    log_success "NotebookLM authentication successful!"
else
    log_error "NotebookLM authentication failed"
    echo ""
    echo "You can retry later by running:"
    echo "  notebooklm login"
    echo ""
    read -p "Continue with installation? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# ============================================================
section "6/6: Vault Directory & Configuration"
# ============================================================

# Determine user's home directory
USER_HOME="$HOME"
VAULT_DIR="${USER_HOME}/Documents/Work related/Claude code/Vault"

log_info "Creating Vault directory for research outputs..."
mkdir -p "$VAULT_DIR"
log_success "Vault created at: $VAULT_DIR"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    log_info "Creating .env configuration file..."
    if [ -f .env.example ]; then
        cp .env.example .env
        log_success ".env created (you can edit to customize settings)"
    else
        log_warning ".env.example not found, skipping .env creation"
    fi
else
    log_info ".env already exists, skipping"
fi

# ============================================================
section "✅ Installation Complete!"
# ============================================================

log_success "All components installed successfully!"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "🎉 You're ready to start deep research!"
echo ""
echo "Usage:"
echo "  1. Ask Claude Code: 'Research API design best practices'"
echo "  2. Wait 10-30 minutes for analysis"
echo "  3. Find output in: $VAULT_DIR/{topic}/summary-{date}.md"
echo ""
echo "Output includes:"
echo "  • 10-section comprehensive summary"
echo "  • NotebookLM notebook with all sources"
echo "  • Citations and references"
echo ""
echo "Configuration:"
echo "  • Edit .env to adjust YouTube/web search limits"
echo "  • Run './verify.sh' to test installation"
echo "  • See QUICKSTART.md for detailed usage"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run verification if available
if [ -f verify.sh ]; then
    log_info "Running installation verification..."
    echo ""
    chmod +x verify.sh
    ./verify.sh
fi

echo ""
log_success "Setup complete! Happy researching! 🚀"
echo ""
