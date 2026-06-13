# Instalación — DCSS-es

Guía para instalar y jugar a Dungeon Crawl Stone Soup con las traducciones al español.

---

## Requisitos

- **Sistema operativo**: Linux (x86_64)
- **DCSS**: v0.34.1 (AppImage recomendada)
- **Espacio**: ~500 MB

---

## Instalación rápida

### 1. Descargar DCSS

```bash
wget https://github.com/crawl/crawl/releases/download/0.34.1/crawl-0.34.1-linux-x86_64.AppImage
```

### 2. Extraer AppImage

```bash
chmod +x crawl-0.34.1-linux-x86_64.AppImage
./crawl-0.34.1-linux-x86_64.AppImage --appimage-extract
```

Se creará un directorio `squashfs-root/` con el juego.

### 3. Clonar las traducciones

```bash
git clone https://github.com/tu_usuario/dcss-es.git
cd dcss-es
```

### 4. Copiar traducciones al juego

```bash
bash scripts/instalar.sh --dir ../squashfs-root/
```

### 5. Configurar idioma

Crea o edita `~/.crawl/init.txt`:

```
language = es
```

O usa el lanzador incluido:

```bash
./jugar.sh
```

---

## Instalación con el lanzador

El script `jugar.sh` hace todo automáticamente:

```bash
./jugar.sh
```

Comprueba que el juego esté en `~/proyectos/dcss-squashfs/squashfs-root/` y
configura `language = es` si no existe.

### Personalizar ruta del juego

```bash
CRAWL_DIR=/ruta/al/juego ./jugar.sh
```

---

## Verificar instalación

```bash
# El juego debería mostrar la versión correcta
./jugar.sh -version

# Comprobar que los archivos de traducción están en su sitio
ls squashfs-root/usr/dat/descript/es/    # Deberían salir 23 archivos
ls squashfs-root/usr/dat/database/es/    # Deberían salir 23 archivos
```

---

## Actualizar traducciones

Cuando este repositorio se actualice:

```bash
git pull
bash scripts/actualizar_juego.sh
```

---

## LibreTranslate (opcional, para desarrollo)

Si quieres usar traducción automática para añadir nuevas entradas:

```bash
# Con Docker
docker run -d -p 5000:5000 libretranslate/libretranslate --load-only en,es

# Sin Docker (Python)
pip install libretranslate
libretranslate --port 5000
```

Luego:

```bash
python3 scripts/translate_batch.py --missing
```

---

## Solución de problemas

### "language = es" no funciona

Asegúrate de que `~/.crawl/init.txt` contenga exactamente:

```
language = es
```

(NO `lang = es` — la opción correcta es `language`)

### No aparecen las traducciones

Verifica que los archivos estén en el directorio correcto:

```bash
ls -la squashfs-root/usr/dat/descript/es/
ls -la squashfs-root/usr/dat/database/es/
```

Si faltan, ejecuta:

```bash
bash scripts/actualizar_juego.sh
```

### El juego se ve en inglés

Puede que el juego esté usando otro archivo init. Prueba:

```bash
CRAWL_LANG=es squashfs-root/usr/bin/crawl
```
