#!/bin/bash
# Lanza DCSS con las traducciones al español
# Uso: ./jugar.sh [opciones]

GAME_DIR="$HOME/proyectos/dcss-squashfs/squashfs-root"
CRAWL_BIN="$GAME_DIR/usr/bin/crawl"

if [ ! -f "$CRAWL_BIN" ]; then
    echo "❌ No se encuentra el juego en $GAME_DIR"
    echo "Ejecuta primero: ./scripts/setup_game.sh"
    exit 1
fi

# Crear init file para español si no existe
INIT_DIR="$HOME/.crawl"
INIT_FILE="$INIT_DIR/init.txt"
mkdir -p "$INIT_DIR"
if ! grep -q "language" "$INIT_FILE" 2>/dev/null; then
    cat >> "$INIT_FILE" << 'EOF'

# Configuración de idioma (es = español)
language = es
EOF
echo "   Configurado idioma español en $INIT_FILE"
fi

# Lanzar juego
echo "🎮 Lanzando DCSS en español..."
echo "   (Ctrl+D para salir del juego)"
echo ""
CRAWL_LANG=es "$CRAWL_BIN" "$@"
