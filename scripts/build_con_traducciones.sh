#!/bin/bash
# ============================================================================
# Compila DCSS con las traducciones de UI (Fase 2)
# ============================================================================
# Uso: bash scripts/build_con_traducciones.sh
#
# Requisitos:
#   - git, g++, make, python3, pkg-config
#   - libsqlite3-dev, liblua5.4-dev, libpcre2-dev, libfreetype-dev, libpng-dev
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="/tmp/dcss-build-$$"

echo "📦 Compilando DCSS con traducciones UI..."
echo "   Proyecto: $PROJECT_DIR"
echo "   Build:    $BUILD_DIR"

# ── 1. Clonar fuente ──
echo ""
echo "📥 Clonando fuente (DCSS 0.34.1)..."
git clone --depth 1 --branch 0.34.1 https://github.com/crawl/crawl.git "$BUILD_DIR"

cd "$BUILD_DIR/crawl-ref/source"

# ── 2. Aplicar infraestructura de traducción ──
echo ""
echo "🔧 Aplicando infraestructura de UI translation..."
git apply "$PROJECT_DIR/patches/0001-ui-translation-infra-full.diff"

# ── 3. Aplicar tr() calls a newgame.cc y menu.cc ──
echo ""
echo "🔧 Aplicando tr() calls a newgame.cc..."
sed -i '/^#include "english.h"/a #include "translation.h"' newgame.cc
sed -i 's/"+ - Recommended species"/tr("+ - Recommended species")/' newgame.cc
sed -i 's/"+ - Recommended background"/tr("+ - Recommended background")/' newgame.cc
sed -i 's/"# - Recommended character"/tr("# - Recommended character")/' newgame.cc
sed -i 's/"Shuffles through random recommended character combinations /tr("Shuffles through random recommended character combinations /' newgame.cc
sed -i 's/"until you accept one.")/tr("until you accept one."))/' newgame.cc
sed -i 's/"Shuffles through random character combinations /tr("Shuffles through random character combinations /' newgame.cc
sed -i 's/"% - List aptitudes"/tr("% - List aptitudes")/' newgame.cc
sed -i 's/"Lists the numerical skill train aptitudes for all races."/tr("Lists the numerical skill train aptitudes for all races.")/' newgame.cc
sed -i 's/"? - Help"/tr("? - Help")/' newgame.cc
sed -i 's/"Opens the help screen."/tr("Opens the help screen.")/' newgame.cc
sed -i 's/"Esc - Quit"/tr("Esc - Quit")/' newgame.cc
sed -i 's/"\* - Random name"/tr("* - Random name")/' newgame.cc
sed -i 's/formatted_string("Enter - Begin!"/formatted_string(tr("Enter - Begin!")/' newgame.cc
sed -i 's/formatted_string("That'\''s a silly name!"/formatted_string(tr("That'\''s a silly name!")/' newgame.cc
sed -i 's/make_shared<Text>("Do you want to play this combination?/make_shared<Text>(tr("Do you want to play this combination?)/' newgame.cc
sed -i 's/prompt.cprintf("What is your name today? ")/prompt.cprintf("%s", tr("What is your name today? ").c_str())/' newgame.cc
sed -i 's/prompt.cprintf("You have an existing game under this name; really overwrite?/prompt.cprintf("%s", tr("You have an existing game under this name; really overwrite?)/' newgame.cc
sed -i 's/"Choose 0 for a random seed. /tr("Choose 0 for a random seed. /' newgame.cc
sed -i 's/cycle input focus.\\n"/cycle input focus.") + "\\n"/' newgame.cc
sed -i 's/"Seed: "/tr("Seed: ")/' newgame.cc
sed -i 's/set_child(make_shared<ui::Text>("Fully pregenerate the dungeon"))/set_child(make_shared<ui::Text>(tr("Fully pregenerate the dungeon")))/' newgame.cc

echo ""
echo "🔧 Aplicando tr() calls a menu.cc..."
sed -i '/^#include "stringutil.h"/a #include "translation.h"' menu.cc
sed -i 's/"Select what (regex)?"/tr("Select what (regex)?").c_str()/' menu.cc

# ── 4. Actualizar archivo de traducción ──
echo ""
echo "📝 Copiando traducciones UI..."
mkdir -p dat/ui/es/
cp "$PROJECT_DIR/translations/ui/es/menu.txt" dat/ui/es/

# ── 5. Generar cabeceras ──
echo ""
echo "⚙️  Generando cabeceras..."
python3 util/gen-all.py 2>&1 | grep -v "Error:"

# ── 6. Compilar ──
echo ""
echo "🔨 Compilando (esto tarda unos minutos)..."
make -j$(nproc) 2>&1 | tail -10

# ── 7. Verificar ──
if [ -f crawl ]; then
    echo ""
    echo "✅ Compilación exitosa!"
    echo "   Binario: $BUILD_DIR/crawl-ref/source/crawl"
    echo ""
    echo "🎮 Para jugar:"
    echo "   cd $BUILD_DIR/crawl-ref/source"
    echo "   LANGUAGE=es ./crawl"
    echo ""
    echo "   O instala las traducciones en tu juego existente:"
    echo "   cp dat/ui/es/menu.txt ~/proyectos/dcss-squashfs/squashfs-root/usr/dat/ui/es/"
else
    echo "❌ Compilación fallida. Revisa los errores arriba."
    exit 1
fi
