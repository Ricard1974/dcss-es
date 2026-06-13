#!/bin/bash
# Actualiza las traducciones en el juego instalado
# Ejecutar después de traducir nuevos archivos

GAME_DIR="$HOME/proyectos/dcss-squashfs/squashfs-root"
PROJECT="$HOME/proyectos/dcss-es"

if [ ! -d "$GAME_DIR/usr/dat/descript/es" ]; then
    echo "❌ No se encuentra el juego instalado"
    echo "Ejecuta primero el script de instalación"
    exit 1
fi

echo "📦 Actualizando traducciones..."
cp "$PROJECT/translations/descript/es/"*.txt "$GAME_DIR/usr/dat/descript/es/"
echo "✅ Copiadas $(ls $PROJECT/translations/descript/es/*.txt | wc -l) traducciones"

# También actualizar database si existe
if [ -d "$PROJECT/translations/database/es" ] && [ "$(ls $PROJECT/translations/database/es/ 2>/dev/null | wc -l)" -gt 0 ]; then
    mkdir -p "$GAME_DIR/usr/dat/database/es"
    cp "$PROJECT/translations/database/es/"*.txt "$GAME_DIR/usr/dat/database/es/"
    echo "✅ Copiadas $(ls $PROJECT/translations/database/es/*.txt | wc -l) traducciones de database"
fi

# Actualizar UI translations (Fase 2)
if [ -d "$PROJECT/translations/ui/es" ] && [ "$(ls $PROJECT/translations/ui/es/ 2>/dev/null | wc -l)" -gt 0 ]; then
    mkdir -p "$GAME_DIR/usr/dat/ui/es"
    cp "$PROJECT/translations/ui/es/"*.txt "$GAME_DIR/usr/dat/ui/es/"
    echo "✅ Copiadas $(ls $PROJECT/translations/ui/es/*.txt | wc -l) traducciones de UI"
fi

echo "🎮 Listo. Ejecuta: ./jugar.sh"
