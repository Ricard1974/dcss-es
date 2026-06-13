#!/bin/bash
# Instala las traducciones de DCSS-es en un directorio de juego existente.
# Uso: bash scripts/instalar.sh --dir /ruta/al/squashfs-root
#
# Si no se especifica --dir, busca en ubicaciones comunes.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Directorios de traducción en el proyecto
TRANS_DESCRIPT="$PROJECT_DIR/translations/descript/es"
TRANS_DATABASE="$PROJECT_DIR/translations/database/es"

# Buscar directorio de instalación
if [ "$1" = "--dir" ] && [ -n "$2" ]; then
    GAME_DIR="$2"
elif [ -d "$HOME/proyectos/dcss-squashfs/squashfs-root" ]; then
    GAME_DIR="$HOME/proyectos/dcss-squashfs/squashfs-root"
elif [ -d "$HOME/squashfs-root" ]; then
    GAME_DIR="$HOME/squashfs-root"
elif [ -d "./squashfs-root" ]; then
    GAME_DIR="./squashfs-root"
else
    echo "❌ No se encuentra el directorio del juego."
    echo "   Usa: $0 --dir /ruta/al/squashfs-root"
    exit 1
fi

# Verificar estructura del juego
GAME_DESCRIPT="$GAME_DIR/usr/dat/descript"
GAME_DATABASE="$GAME_DIR/usr/dat/database"

if [ ! -d "$GAME_DESCRIPT" ]; then
    echo "❌ No se encuentra la estructura del juego en $GAME_DIR"
    echo "   Asegúrate de que es un DCSS extraído (AppImage o compilación)."
    exit 1
fi

# Copiar traducciones
echo "📦 Instalando traducciones en $GAME_DIR..."

# descript/
if [ -d "$TRANS_DESCRIPT" ]; then
    mkdir -p "$GAME_DESCRIPT/es"
    cp "$TRANS_DESCRIPT"/*.txt "$GAME_DESCRIPT/es/" 2>/dev/null
    count=$(ls "$TRANS_DESCRIPT"/*.txt 2>/dev/null | wc -l)
    echo "   ✅ $count archivos copiados en descript/es/"
else
    echo "   ⚠️  No se encuentran traducciones de descript/"
fi

# database/
if [ -d "$TRANS_DATABASE" ]; then
    mkdir -p "$GAME_DATABASE/es"
    cp "$TRANS_DATABASE"/*.txt "$GAME_DATABASE/es/" 2>/dev/null
    count=$(ls "$TRANS_DATABASE"/*.txt 2>/dev/null | wc -l)
    echo "   ✅ $count archivos copiados en database/es/"
else
    echo "   ⚠️  No se encuentran traducciones de database/"
fi

# Configurar init.txt
INIT_DIR="$HOME/.crawl"
INIT_FILE="$INIT_DIR/init.txt"
mkdir -p "$INIT_DIR"
if ! grep -q "^language" "$INIT_FILE" 2>/dev/null; then
    echo "" >> "$INIT_FILE"
    echo "# Configuración de idioma (es = español)" >> "$INIT_FILE"
    echo "language = es" >> "$INIT_FILE"
    echo "   ✅ Configurado language = es en $INIT_FILE"
else
    echo "   ℹ️  language ya configurado en $INIT_FILE"
fi

echo ""
echo "🎮 Instalación completa. Ejecuta:"
echo "   $GAME_DIR/usr/bin/crawl"
echo ""
