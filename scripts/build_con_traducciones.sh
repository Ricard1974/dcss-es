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

# ── 2b. Añadir names.txt a la lista de archivos cargados en translation.cc
echo ""
echo "🔧 Añadiendo names.txt a la lista de carga..."
sed -i '/"misc.txt"/a \    "names.txt",' translation.cc
echo "  ✓ names.txt añadido a s_ui_files"

# ── 3. Añadir translation.o a la lista de objetos ──
echo ""
echo "🔧 Añadiendo translation.o a Makefile.obj..."
if ! grep -q "translation.o" Makefile.obj; then
    sed -i '/^travel.o \\/i translation.o \\' Makefile.obj
    echo "  ✓ translation.o añadido"
else
    echo "  ✓ translation.o ya existe"
fi

# ── 4. Aplicar tr() calls a format.cc ──
echo ""
echo "🔧 Aplicando tr() calls a format.cc..."
sed -i '/^#include "viewchar.h"/a #include "translation.h"' format.cc
sed -i 's/ops.push_back(s);/ops.push_back(tr(s));/' format.cc
echo "  ✓ format.cc modificado"

# ── 5. Aplicar tr() calls a newgame.cc (vía Python, maneja multilínea) ──
echo ""
echo "🔧 Aplicando tr() calls a newgame.cc..."
git checkout -- newgame.cc 2>/dev/null || true
python3 "$PROJECT_DIR/scripts/fix_newgame.py" newgame.cc
echo "  ✓ newgame.cc modificado"

# ── 6. Aplicar tr() calls a menu.cc ──
echo ""
echo "🔧 Aplicando tr() calls a menu.cc..."
sed -i '/^#include "stringutil.h"/a #include "translation.h"' menu.cc
sed -i 's/"Select what (regex)?"/tr("Select what (regex)?").c_str()/' menu.cc
sed -i 's/newlines.push_back(formatted_string::parse_string(seg, colour));/newlines.push_back(formatted_string::parse_string(tr(seg), colour));/' menu.cc
echo "  ✓ menu.cc modificado (tr() línea por línea en add_formatted)"

# ── 7. Aplicar tr() calls a command.cc (carga archivos de ayuda localizados) ──
echo ""
echo "🔧 Aplicando carga de ayuda localizada a command.cc..."
git checkout -- command.cc 2>/dev/null || true
python3 "$PROJECT_DIR/scripts/fix_command.py" command.cc
echo "  ✓ command.cc modificado"

# ── 8. Aplicar tr() calls a message.cc (traducción de mensajes del juego) ──
echo ""
echo "🔧 Aplicando tr() calls a message.cc..."
sed -i '/^#include "stringutil.h"/a #include "translation.h"' message.cc
sed -i '/^static bool _doing_c_message_hook = false;/a \    text = tr(text);' message.cc
echo "  ✓ message.cc modificado (_mpr traduce todos los mensajes)"

# ── 8b. Aplicar tr() en do_message_print (traducir FORMATO antes de vsnprintf) ──
echo ""
echo "🔧 Aplicando tr() en do_message_print..."
python3 "$PROJECT_DIR/scripts/fix_message_mprf.py" message.cc
echo "  ✓ message.cc modificado (do_message_print traduce formato con %s)"

# ── 9. Aplicar tr() calls a cio.cc (wrapcprintf - panel derecho de stats) ──
echo ""
echo "🔧 Aplicando tr() calls a cio.cc..."
sed -i '1i #include "translation.h"' cio.cc
sed -i '/^string buf = vmake_stringf(s, args);$/a\    buf = tr(buf);' cio.cc
echo "  ✓ cio.cc modificado (wrapcprintf traduce panel derecho y otros)"

# ── 10. Aplicar tr() calls a libunix.cc (cprintf global - menús, etc.) ──
echo ""
echo "🔧 Aplicando tr() calls a libunix.cc..."
sed -i '1i #include "translation.h"' libunix.cc
python3 "$PROJECT_DIR/scripts/fix_libunix.py" libunix.cc
echo "  ✓ libunix.cc modificado (cprintf global traduce menús, etc.)"

# ── 11. Aplicar tr() a _add_command en command.cc (descripciones de teclas) ──
echo ""
echo "🔧 Aplicando tr() en _add_command..."
sed -i '/^#include "libutil.h"/a #include "translation.h"' command.cc
sed -i 's/line += ": " + untag_tiles_console(desc) + "\\n";/line += ": " + tr(untag_tiles_console(desc)) + "\\n";/' command.cc
echo "  ✓ command.cc modificado (_add_command traduce descripciones)"

# ── 12. Aplicar tr() calls a startup.cc (modos de juego del menú principal) ──
echo ""
echo "🔧 Aplicando tr() calls a startup.cc..."
sed -i 's/label->set_text(formatted_string(entry.label, WHITE));/label->set_text(formatted_string(tr(entry.label), WHITE));/' startup.cc
echo "  ✓ startup.cc modificado (menú principal traduce modos de juego)"

# ── 12. Copiar archivos de traducción ──
echo ""
echo "📝 Copiando traducciones UI..."
mkdir -p dat/ui/es/
cp "$PROJECT_DIR/translations/ui/es/"*.txt dat/ui/es/
echo "  ✓ $(ls dat/ui/es/*.txt | wc -l) archivos copiados"

# ── 14. Generar cabeceras ──
echo ""
echo "⚙️  Generando cabeceras..."
python3 util/gen-all.py 2>&1 | grep -v "Error:"

# ── 15. Compilar ──
echo ""
echo "🔨 Compilando (esto tarda unos minutos)..."
make -j$(nproc) 2>&1 | tail -10

# ── 16. Verificar ──
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
    echo "   cp dat/ui/es/*.txt ~/proyectos/dcss-squashfs/squashfs-root/usr/dat/ui/es/"
    echo "   cp crawl ~/proyectos/dcss-squashfs/squashfs-root/usr/bin/"
    echo ""
    echo "🔍 Ejecutando verificación post-build..."
    python3 "$PROJECT_DIR/scripts/verify.py"
else
    echo "❌ Compilación fallida. Revisa los errores arriba."
    exit 1
fi
