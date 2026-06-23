#!/usr/bin/env python3
"""
Bot QA v6 - Rastrea estado en lugar de detectar pantalla.
"""

import subprocess, re, time, os, random

TMUX = "dcss-bot"
CAP_DIR = "capturas"
os.makedirs(CAP_DIR, exist_ok=True)

STATE = "init"  # init → menu → name → species → game → death
_menuidx = 0
_english = set()


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
        if re.search(r"[áéíóúñ]", s):
            score -= 2
        if score >= 1:
            r.add(s)
    return r


MENUS = [
    ("?", "ayuda_principal", 2),
    ("e", "ayuda_explore", 1),
    ("1", "ayuda_especies", 1),
    ("2", "ayuda_clases", 1),
    ("3", "ayuda_habilidades", 1),
    ("4", "ayuda_teclas", 1),
    ("Escape", None, 0),
    ("m", "skills", 2),
    ("Escape", None, 0),
    ("i", "inventario", 2),
    ("Escape", None, 0),
    ("%", "aptitudes", 2),
    ("Escape", None, 0),
    ("@", "status", 2),
    ("Escape", None, 0),
    ("A", "habilidades", 2),
    ("Escape", None, 0),
    ("z", "hechizos", 2),
    ("Escape", None, 0),
    ("M", "biblioteca", 2),
    ("Escape", None, 0),
    ("^", "religion", 2),
    ("Escape", None, 0),
    ("\\\\", "conocimiento", 2),
    ("Escape", None, 0),
    ("}", "runas", 2),
    ("Escape", None, 0),
    ("[", "armadura", 2),
    ("Escape", None, 0),
    ('"', "joyas", 2),
    ("Escape", None, 0),
    ("$", "oro", 2),
    ("Escape", None, 0),
    ("E", "experiencia", 2),
    ("Escape", None, 0),
]


def do(action, delay=0.3):
    if action.startswith("delay:"):
        time.sleep(int(action.split(":")[1]))
    elif action == "escape":
        send("Escape")
    elif action in (
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
    ):
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
            }[action]
        )
    else:
        send(action)
    time.sleep(delay)


def cycle_menus():
    global _menuidx, _english
    if _menuidx >= len(MENUS):
        _menuidx = 0
        for _ in range(15):
            do(random.choice(["h", "j", "k", "l", "o"]), 0.3)
        do(">", 1)
        return

    action = MENUS[_menuidx]
    key, name, delay = action
    _menuidx += 1

    if name:
        do(key, delay)
        t = cap()
        save(t, name)
        _english |= find_english(t)
    elif key == "Escape":
        do("escape", 0.3)
    else:
        do(key, 0.5)


def main():
    global STATE, _menuidx, _english

    print("=" * 50)
    print("BOT QA v6")
    print("=" * 50)

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
    print("🔄 Iniciando...")
    time.sleep(3)

    paso = 0
    stuck = 0
    last = ""

    while paso < 500:
        paso += 1
        t = cap()

        if not t or t.strip() == last.strip():
            stuck += 1
        else:
            stuck = 0
        last = t

        if paso % 3 == 0:
            save(t)
            _english |= find_english(t)

        if paso % 5 == 1:
            print(f"\n[{paso}] {STATE} en={len(_english)} stuck={stuck}")
            for l in t.split("\n")[-3:]:
                if l.strip():
                    print(f"  {l.strip()[:100]}")

        # State machine
        if STATE == "init":
            STATE = "name"

        elif STATE == "name":
            do("Bot" + str(random.randint(100, 999)), 0.3)
            do("enter", 0.5)
            STATE = "menu"

        elif STATE == "menu":
            do("enter", 0.5)
            STATE = "species"

        elif STATE == "species":
            do(random.choice("abcdefghijklmnopqrstuvwxyz"), 0.5)
            STATE = "game"

        elif STATE == "game":
            # Check if dead
            if "You die" in t or "Has muerto" in t:
                STATE = "death"
                continue

            # Check for enemy messages to fight
            if re.search(r"(hits|misses|bites|wounded|is nearby|está cerca)", t, re.I):
                do("fight", 0.3)
                continue

            cycle_menus()

        elif STATE == "death":
            do("enter", 1)
            do("enter", 2)
            STATE = "menu"
            _menuidx = 0

        if stuck > 50:
            print("⚠️ Reinicio...")
            do("Q", 1)
            do("y", 2)
            STATE = "menu"
            stuck = 0
            _menuidx = 0

    print(f"\n✅ {len(_english)} strings en inglés.")
    rpt = os.path.join(CAP_DIR, "english_report.txt")
    with open(rpt, "w") as f:
        for s in sorted(_english):
            f.write(s + "\n")
    print(f"Reporte: {rpt}")


if __name__ == "__main__":
    main()
