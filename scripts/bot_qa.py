#!/usr/bin/env python3
"""
Bot QA - Abre TODOS los menús del juego para capturar texto.
"""

import subprocess, re, time, os, random

TMUX = "dcss-bot"
CAP_DIR = "capturas"
os.makedirs(CAP_DIR, exist_ok=True)


def cap():
    r = subprocess.run(
        ["tmux", "capture-pane", "-p", "-t", TMUX],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return r.stdout


def send(k):
    subprocess.run(["tmux", "send-keys", "-t", TMUX, k], capture_output=True)


def save(t, nombre=""):
    n = len(
        [
            f
            for f in os.listdir(CAP_DIR)
            if f.endswith(".txt") and not f.startswith("english")
        ]
    )
    p = os.path.join(CAP_DIR, f"{nombre}_{n:04d}.txt" if nombre else f"cap_{n:04d}.txt")
    with open(p, "w") as f:
        f.write(t)
    return p


def detect(text):
    if "Mazmorras de Piedra Sopa" in text or (
        "Choices:" in text and "Dungeon Crawl" in text
    ):
        return "menu"
    if (
        "seleccionar tu especie" in text.lower()
        or "select your species" in text.lower()
    ):
        return "species"
    if "Introduce tu nombre" in text or "Enter your name:" in text:
        return "name"
    if "@" in text and ("Health:" in text or "Salud:" in text or "HP:" in text):
        return "game"
    if "You die" in text or "Has muerto" in text:
        return "death"
    return "unknown"


def find_english(text):
    r = set()
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            continue
        score = 0
        if re.search(r"\b(The|You|Your)\s", s):
            score += 1
        if re.search(r"\bFound\b", s):
            score += 1
        if re.search(r"\bHealth:|Magic:|AC:|EV:|SH:|Str:|Int:|Dex:|XL:", s):
            score += 0.5
        if re.search(r"[áéíóúñ]", s):
            score -= 2
        if score >= 1:
            r.add(s)
    return r


# ============================================================
# SECUENCIA DE MENÚS PARA CAPTURAR
# ============================================================
# Cada entrada: (tecla, nombre_captura, delay, descripción)
MENUS = [
    # Ayuda y manual
    ("?", "ayuda_principal", 2, "Pantalla de ayuda (?)"),
    ("e", "ayuda_explore", 1, "Ayuda de movimiento/exploración"),
    ("1", "ayuda_especies", 1, "Lista de especies"),
    ("2", "ayuda_clases", 1, "Lista de clases/trasfondos"),
    ("3", "ayuda_habilidades", 1, "Lista de habilidades"),
    ("4", "ayuda_teclas", 1, "Lista de teclas y comandos"),
    ("Escape", None, 0, "Salir ayuda"),
    # Menús del personaje
    ("m", "skills_principal", 2, "Pantalla de habilidades"),
    ("Escape", None, 0, ""),
    ("i", "inventario", 2, "Inventario"),
    ("Escape", None, 0, ""),
    ("%", "aptitudes", 2, "Tabla de aptitudes"),
    ("Escape", None, 0, ""),
    ("@", "status", 2, "Estado del personaje"),
    ("Escape", None, 0, ""),
    ("A", "habilidades", 2, "Habilidades raciales/divinas"),
    ("Escape", None, 0, ""),
    ("z", "hechizos", 2, "Lanzar hechizo"),
    ("Escape", None, 0, ""),
    ("M", "biblioteca", 2, "Biblioteca de hechizos"),
    ("Escape", None, 0, ""),
    # Información
    ("^", "religion", 2, "Pantalla de religión (^)"),
    ("Escape", None, 0, ""),
    ("\\\\", "conocimiento", 2, "Conocimiento de objetos (\\)"),
    ("Escape", None, 0, ""),
    ("}", "runas", 2, "Runas recolectadas"),
    ("Escape", None, 0, ""),
    ("[", "armadura", 2, "Armadura equipada"),
    ("Escape", None, 0, ""),
    ('"', "joyas", 2, "Joyería equipada"),
    ("Escape", None, 0, ""),
    ("$", "oro", 2, "Oro en posesión"),
    ("Escape", None, 0, ""),
    ("E", "experiencia", 2, "Información de experiencia"),
    ("Escape", None, 0, ""),
    ("C", "mascotas", 2, "Compañeros/mascotas"),
    ("Escape", None, 0, ""),
]


def ejecutar_secuencia(text):
    """Ejecuta la secuencia de menús si estamos en juego."""
    global _menu_idx
    if not hasattr(ejecutar_secuencia, "_menu_idx"):
        ejecutar_secuencia._menu_idx = 0

    idx = ejecutar_secuencia._menu_idx

    # Si terminamos, salir
    if idx >= len(MENUS):
        return ["delay:5"]  # Esperar y luego repetir

    accion = MENUS[idx]
    tecla = accion[0]
    nombre = accion[1]
    delay = accion[2]
    desc = accion[3]

    ejecutar_secuencia._menu_idx += 1

    if nombre:
        print(f"  📋 Menú {idx + 1}/{len(MENUS)}: {desc}")

    if delay > 0 and nombre:
        return [tecla, f"guardar:{nombre}", f"delay:{delay}"]
    elif tecla == "Escape":
        return ["escape"]
    else:
        return [tecla]


def main():
    global _menu_idx
    print("=" * 60)
    print("BOT DCSS-es - CAPTURA DE MENÚS")
    print("=" * 60)
    print("Abriendo todos los menús del juego...")

    # Iniciar juego
    subprocess.run(["tmux", "kill-session", "-t", TMUX], capture_output=True)
    time.sleep(0.5)
    subprocess.run(
        ["tmux", "new-session", "-d", "-s", TMUX, "-x", "80", "-y", "30"],
        capture_output=True,
    )
    time.sleep(0.5)

    script = "/tmp/run_crawl.sh"
    with open(script, "w") as f:
        f.write("#!/bin/bash\ncd ~/proyectos/dcss-squashfs/squashfs-root/usr\n")
        f.write("exec env LANGUAGE=es ./bin/crawl\n")
    os.chmod(script, 0o755)

    send(f"bash {script}")
    send("Enter")
    print("🔄 Iniciando DCSS...")
    time.sleep(4)

    english = set()
    last = ""
    stuck = 0
    paso = 0
    dentro_del_juego = False

    try:
        while paso < 500:
            paso += 1
            t = cap()

            if not t or t.strip() == last.strip():
                stuck += 1
            else:
                stuck = 0
            last = t

            screen = detect(t)

            # Guardar captura de menús importantes
            if paso % 2 == 0:
                save(t)

            # Detectar inglés
            eng = find_english(t)
            english |= eng

            # Mostrar estado cada 5 pasos o en cambios de pantalla
            if paso % 5 == 1 or screen in ("menu", "game"):
                pos = "?"
                m = re.search(r"@\s*\(?\s*(\d+)", t)
                if not m:
                    m = re.search(r"@(?:\s|$)", t)
                print(f"\n[{paso}] {screen} | en={len(english)} stuck={stuck}")
                for l in t.split("\n")[-3:]:
                    if l.strip():
                        print(f"  {l.strip()[:100]}")

            # Si estamos en el menú principal, navegar al juego
            if screen == "menu" and not dentro_del_juego:
                # Seleccionar Dungeon Crawl y crear personaje
                actions = [
                    "enter",
                    "delay:1",
                    "Bot" + str(random.randint(100, 999)),
                    "enter",
                    "delay:1",
                    random.choice("abcdefghijklmnopqrstuvwxyz"),
                    "delay:1",
                    random.choice("abcdefghijklmnopqrstuvwxyz"),
                ]
                for a in actions:
                    exec_action(a)
                    time.sleep(0.3)
                dentro_del_juego = True
                ejecutar_secuencia._menu_idx = 0  # Reset menú sequence
                continue

            if screen == "death":
                print("💀 Personaje muerto, reiniciando...")
                exec_action("enter")
                time.sleep(1)
                exec_action("enter")
                time.sleep(2)
                dentro_del_juego = False
                continue

            # Si estamos en juego, ejecutar secuencia de menús
            if screen == "game" and dentro_del_juego:
                acciones = ejecutar_secuencia(t)
                for a in acciones:
                    exec_action(a)
                    time.sleep(0.5)

                # Si la secuencia terminó, explorar un poco y repetir
                if ejecutar_secuencia._menu_idx >= len(MENUS):
                    print("🔄 Secuencia completada, explorando...")
                    # Explorar y luego bajar escaleras
                    for _ in range(15):
                        exec_action(random.choice(["o", "h", "j", "k", "l"]))
                        time.sleep(0.4)
                    # Bajar escaleras e intentar de nuevo
                    exec_action(">")
                    time.sleep(1)
                    ejecutar_secuencia._menu_idx = 0
                continue

            # En pantallas desconocidas, cerrar con Escape
            if screen == "unknown":
                exec_action("escape")
                time.sleep(0.3)

            if stuck > 30:
                exec_action(random.choice(["h", "j", "k", "l"]))
            if stuck > 60:
                print("⚠️ Reinicio forzado...")
                exec_action("Q")
                time.sleep(1)
                exec_action("y")
                time.sleep(2)
                dentro_del_juego = False
                stuck = 0

    except KeyboardInterrupt:
        print("\n⏹️  Detenido")

    print(f"\n{'=' * 60}")
    print(
        f"CAPTURAS: {len([f for f in os.listdir(CAP_DIR) if f.endswith('.txt')])} archivos"
    )
    print(f"STRINGS INGLÉS: {len(english)}")

    rpt = os.path.join(CAP_DIR, "english_report.txt")
    with open(rpt, "w") as f:
        for s in sorted(english):
            f.write(s + "\n")
    print(f"Reporte: {rpt}")


def exec_action(a):
    if a.startswith("delay:"):
        time.sleep(int(a.split(":")[1]))
    elif a.startswith("guardar:"):
        t = cap()
        save(t, a.split(":")[1])
    elif a == "escape":
        send("Escape")
    elif a in {
        "enter",
        "explore",
        "fight",
        "help",
        "skills",
        "inventory",
        "aptitudes",
        "religion",
        "status",
        "abilities",
        "down",
        "wait",
    }:
        send(
            {
                "enter": "Enter",
                "explore": "o",
                "fight": "Tab",
                "help": "?",
                "skills": "m",
                "inventory": "i",
                "aptitudes": "%",
                "religion": "^",
                "status": "@",
                "abilities": "A",
                "down": ">",
                "wait": ".",
            }[a]
        )
    else:
        send(a)


if __name__ == "__main__":
    main()
