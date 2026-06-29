#!/bin/sh
set -eu

# crawler-mcp installer
# Usage: curl -fsSL https://install.crawler.sh/install-mcp.sh | sh

BINARY="crawler-mcp"
BASE_URL="https://install.crawler.sh/mcp/latest"

# Reuse the CLI install location so a user who already has `crawler` finds
# `crawler-mcp` on the same PATH entry.
INSTALL_DIR="${CRAWLER_INSTALL_DIR:-$HOME/.crawler}"
BIN_DIR="$INSTALL_DIR/bin"

info() {
  printf "\033[1;34m%s\033[0m\n" "$1"
}

error() {
  printf "\033[1;31merror: %s\033[0m\n" "$1" >&2
  exit 1
}

detect_os() {
  case "$(uname -s)" in
    Darwin) echo "macos" ;;
    Linux)  echo "linux" ;;
    *)      error "Unsupported operating system: $(uname -s). Only macOS and Linux are supported." ;;
  esac
}

detect_arch() {
  case "$(uname -m)" in
    arm64 | aarch64) echo "arm64" ;;
    x86_64 | amd64)  echo "x64" ;;
    *)               error "Unsupported architecture: $(uname -m)" ;;
  esac
}

download() {
  url="$1"
  output="$2"

  case "$url" in
    https://*) ;;
    *) error "Refusing to download over insecure connection: $url" ;;
  esac

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL --proto '=https' "$url" -o "$output"
  elif command -v wget >/dev/null 2>&1; then
    wget --https-only -qO "$output" "$url"
  else
    error "curl or wget is required to download files"
  fi
}

add_to_path() {
  path_entry="export PATH=\"$BIN_DIR:\$PATH\""

  for rc in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"; do
    if [ -f "$rc" ]; then
      if ! grep -qF "$BIN_DIR" "$rc" 2>/dev/null; then
        printf '\n# crawler.sh\n%s\n' "$path_entry" >> "$rc"
      fi
    fi
  done

  fish_config="$HOME/.config/fish/config.fish"
  if [ -f "$fish_config" ]; then
    if ! grep -qF "$BIN_DIR" "$fish_config" 2>/dev/null; then
      printf '\n# crawler.sh\nset -gx PATH %s $PATH\n' "$BIN_DIR" >> "$fish_config"
    fi
  fi
}

main() {
  os="$(detect_os)"
  arch="$(detect_arch)"
  filename="${BINARY}-${os}-${arch}"
  url="${BASE_URL}/${filename}"

  info "Installing crawler-mcp..."
  printf "  OS:   %s\n" "$os"
  printf "  Arch: %s\n" "$arch"
  echo ""

  mkdir -p "$BIN_DIR"
  chmod 700 "$INSTALL_DIR"

  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' EXIT

  info "Downloading ${url}..."
  download "$url" "$tmp"

  mv "$tmp" "$BIN_DIR/$BINARY"
  chmod +x "$BIN_DIR/$BINARY"

  add_to_path

  echo ""
  info "crawler-mcp installed successfully!"
  echo ""
  echo "  Binary:  $BIN_DIR/$BINARY"
  echo ""
  echo "  Wire it into your agent (Claude Code example):"
  echo ""
  echo "    Add to ~/.claude/mcp.json:"
  echo "    {"
  echo "      \"mcpServers\": {"
  echo "        \"crawler-sh\": {"
  echo "          \"command\": \"$BIN_DIR/$BINARY\","
  echo "          \"args\": [],"
  echo "          \"env\": {}"
  echo "        }"
  echo "      }"
  echo "    }"
  echo ""
  echo "  Then restart your agent. Three tools become available:"
  echo "    crawl_site, fetch_page, discover_links"
  echo ""
  echo "  Docs: https://crawler.sh/docs/mcp/"
  echo ""
}

main
