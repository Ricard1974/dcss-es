#!/usr/bin/env python3
"""
Corrige traducciones de calidad baja en los archivos UI de DCSS.
Usa reemplazos exactos para no dañar contenido correcto.
"""

import os
import re

BASE = os.path.expanduser("~/proyectos/dcss-es/translations/ui/es")

# Mapa de correcciones: (archivo, English original, Spanish actual → Spanish correcto)
# Solo se corrige si el match es EXACTO
FIXES = [
    # ═══ ability.txt ═══
    ("ability.txt", "Brand Self", "atributo Self", "Marca Personal"),
    ("ability.txt", "Confirm evoke", "Confirme evocar", "Confirmar evocación"),
    ("ability.txt", "Damage: dice", "Daño: dados", "Daño: dados de daño"),
    ("ability.txt", "Dismiss Apostle", "el apóstol despido", "Despedir Apóstol"),
    (
        "ability.txt",
        "Makhleb denies you. Endure the Crucible first!",
        "Makhleb te niega. Endure el Crucible primero!",
        "¡Makhleb te rechaza! Supera el Crisol primero.",
    ),
    (
        "ability.txt",
        "Night has already fallen.",
        "la noche ya ha caído.",
        "La noche ya ha caído.",
    ),
    (
        "ability.txt",
        "No description found.\\n",
        "No Hay descripción encontrada",
        "No hay descripción disponible.\\n",
    ),
    ("ability.txt", "Really use ", "Uso real", "¿Usar de verdad? "),
    (
        "ability.txt",
        "Sacrifices cannot be taken back.\\n",
        "los sacrificios no se pueden recuperar",
        "Los sacrificios no se pueden recuperar.\\n",
    ),
    (
        "ability.txt",
        "Select an artefact weapon to imprint upon your Paragon.",
        "Seleccione un arma de artefacto para imprimir en tu Paragon.",
        "Selecciona un arma de artefacto para imprimir en tu Parangón.",
    ),
    (
        "ability.txt",
        "That deck is empty!",
        "¡la cubierta está vacía!",
        "¡Esa baraja está vacía!",
    ),
    (
        "ability.txt",
        "There is no water in range!",
        "¡no hay agua en rango!",
        "¡No hay agua en el rango!",
    ),
    (
        "ability.txt",
        "There isn't enough space to grow briars here.",
        "No Hay suficiente espacio para cultivar briares aquí.",
        "No hay suficiente espacio para cultivar zarzas aquí.",
    ),
    (
        "ability.txt",
        "There's no appreciative audience!",
        "¡no hay audiencia apreciativa!",
        "¡No hay público que lo aprecie!",
    ),
    (
        "ability.txt",
        "Use which ability? (? or * to list) ",
        "¿Utilizar qué habilidad? (? o * a lista)",
        "¿Usar qué habilidad? (? o * para listar) ",
    ),
    (
        "ability.txt",
        "Weird ability return type",
        "Tipo de retorno de habilidad rara",
        "Tipo de retorno de habilidad extraño",
    ),
    (
        "ability.txt",
        "You already have the maximum number of followers. Dismiss one first.",
        "Ya tienes el número máximo de seguidores. Descargue uno primero.",
        "Ya tienes el número máximo de seguidores. Despide a uno primero.",
    ),
    (
        "ability.txt",
        "You are too exhausted to lash out.",
        "Estás demasiado agotada para lavarte.",
        "Estás demasiado agotado para atacar.",
    ),
    (
        "ability.txt",
        "You are not zealous enough to affect this audience!",
        "¡no eres lo suficientemente celoso como para afectar a este público!",
        "¡No eres lo bastante fervoroso para influir en este público!",
    ),
    (
        "ability.txt",
        "You aren't in the Abyss!",
        "¡no estás en el Abyss!",
        "¡No estás en el Abismo!",
    ),
    (
        "ability.txt",
        "You call down Yredelemnul's inexorable grip.",
        "Derriba el inexorable agarre de Yredelemnul.",
        "Invocas el agarre inexorable de Yredelemnul.",
    ),
    (
        "ability.txt",
        "You can't do that.",
        "No Puedes hacer eso.",
        "No puedes hacer eso.",
    ),
    (
        "ability.txt",
        "You can't heal while in death's door.",
        "No Puedes curarte mientras estás en la puerta de la muerte.",
        "No puedes curarte mientras estás en la puerta de la muerte.",
    ),
    (
        "ability.txt",
        "You can't rise from this level!",
        "¡no puedes subir de este nivel!",
        "¡No puedes subir de este nivel!",
    ),
    (
        "ability.txt",
        "You can't see any clouds you can empower.",
        "No Puedes ver ninguna nube que puedas empoderar.",
        "No puedes ver ninguna nube que puedas potenciar.",
    ),
    (
        "ability.txt",
        "You can't see any nearby targets.",
        "No Puedes ver objetivos cercanos.",
        "No puedes ver objetivos cercanos.",
    ),
    (
        "ability.txt",
        "You cannot banish yourself!",
        "¡no puedes desterrarte!",
        "¡No puedes desterrarte!",
    ),
    (
        "ability.txt",
        "You don't have any memories left to burn.",
        "No Te quedan recuerdos para quemar.",
        "No te quedan recuerdos para quemar.",
    ),
    (
        "ability.txt",
        "You don't have enough experience to sacrifice.",
        "No Tienes suficiente experiencia para sacrificarte.",
        "No tienes suficiente experiencia para sacrificar.",
    ),
    (
        "ability.txt",
        "You don't have enough innate magic capacity.",
        "No Tienes suficiente capacidad mágica innata.",
        "No tienes suficiente capacidad mágica innata.",
    ),
    (
        "ability.txt",
        "You exhale a blast of poison gas.",
        "Exhala una explosión de gas venenoso.",
        "Exhalas una ráfaga de gas venenoso.",
    ),
    (
        "ability.txt",
        "You extend your mandibles.",
        "Extendes tus mandíbulas.",
        "Extiendes tus mandíbulas.",
    ),
    (
        "ability.txt",
        "You fail to use your ability.",
        "No Puedes usar tu habilidad.",
        "No puedes usar tu habilidad.",
    ),
    (
        "ability.txt",
        "You feel stolen life flooding into you from an unseen source!",
        "¡Te sientes robada de una fuente invisible!",
        "¡Sientes cómo la vida robada entra en ti desde una fuente invisible!",
    ),
    (
        "ability.txt",
        "You feel stolen life flooding into you!",
        "¡Te sientes robada la vida inundada en ti!",
        "¡Sientes cómo la vida robada entra en ti!",
    ),
    (
        "ability.txt",
        "You feel the orb feeding on your energy!",
        "¡Sientes el orbe alimentando tu energía!",
        "¡Sientes el orbe alimentándose de tu energía!",
    ),
    (
        "ability.txt",
        "You have no need to draw out power.",
        "No Tienes que sacar el poder.",
        "No tienes necesidad de extraer poder.",
    ),
    (
        "ability.txt",
        "You have nothing to donate!",
        "¡no tienes nada que donar!",
        "¡No tienes nada que donar!",
    ),
    (
        "ability.txt",
        "You must stoke the torch's fire more first.",
        "Debe aturdir el fuego de la antorcha más primero.",
        "Debes avivar más el fuego de la antorcha primero.",
    ),
    (
        "ability.txt",
        "You're already rising!",
        "¡Ya estás subiendo!",
        "¡Ya estás ascendiendo!",
    ),
    (
        "ability.txt",
        "You're too exhausted to draw out your power.",
        "Estás demasiado agotada para sacar tu poder.",
        "Estás demasiado agotado para extraer tu poder.",
    ),
    (
        "ability.txt",
        "You're too exhausted to power leap.",
        "Estás demasiado agotada para saltar el poder.",
        "Estás demasiado agotado para dar un salto poderoso.",
    ),
    (
        "ability.txt",
        "You're too exhausted to unleash your apocalyptic power.",
        "Estás demasiado agotada para liberar tu poder apocalíptico.",
        "Estás demasiado agotado para liberar tu poder apocalíptico.",
    ),
    (
        "ability.txt",
        "Your [hand(s)] get{s} new energy.",
        "Tu nueva energía.",
        "Tus [mano(s)] reciben nueva energía.",
    ),
    # ═══ religion.txt ═══
    (
        "religion.txt",
        "The service fee for joining is currently %d gold; you have",
        "la cuota de servicio para unirse es actualmente oro %d; Tú tiene",
        "La cuota de servicio para unirse es actualmente %d de oro; tienes",
    ),
    (
        "religion.txt",
        "You drain nearby creatures when transferring your ancestor.",
        "Tú drena criaturas cercanas al transferir tu antepasado.",
        "Drenas criaturas cercanas al transferir a tu ancestro.",
    ),
    (
        "religion.txt",
        "You feel the divine notice you fully once more.",
        "Tú siente el aviso divino Tú completamente una vez más.",
        "Sientes que lo divino te nota por completo una vez más.",
    ),
    (
        "religion.txt",
        "You pay a service fee of %d gold.",
        "Tú atraviesa una cuota de servicio de oro %d.",
        "Pagas una cuota de servicio de %d de oro.",
    ),
    (
        "religion.txt",
        "You will suffer for embracing such %s",
        "Tú sufrirá por abrazar tales porcentajes",
        "Sufrirás por abrazar tal %s",
    ),
    (
        "religion.txt",
        "Your access to %s's decks is revoked.",
        "Tu acceso a cubiertas de %s es revocado.",
        "Tu acceso a las barajas de %s queda revocado.",
    ),
    (
        "religion.txt",
        "Your apostles are sometimes healed when you deal damage.",
        "Sus apóstoles a veces son curados cuando Tú hace daño.",
        "Tus apóstoles a veces se curan cuando causas daño.",
    ),
    (
        "religion.txt",
        "recall your ancestor",
        "recuerde tu antepasado",
        "recuerda a tu ancestro",
    ),
    (
        "religion.txt",
        "says: You must forswear the aid of any and all",
        "dice: Tú debe forzar la ayuda de cualquiera y todos",
        "dice: Debes renunciar a la ayuda de cualquier otro dios",
    ),
    (
        "religion.txt",
        "You and your allies can gain power from killing the unholy and evil.",
        "Tú y tus aliados pueden ganar el poder de matar al impío y al mal.",
        "Tú y tus aliados podéis ganar poder matando a los impíos y malvados.",
    ),
    (
        "religion.txt",
        "You and your allies can no longer gain power from killing the unholy and evil.",
        "Vosotros y vuestros aliados ya no podéis ganar el poder de matar al impío y al mal.",
        "Vosotros y vuestros aliados ya no podéis ganar poder matando a los impíos y malvados.",
    ),
    (
        "religion.txt",
        "You and your allies can now gain power from killing the unholy and evil.",
        "Tú y tus aliados ahora pueden ganar el poder de matar a los impíos y al mal.",
        "Tú y tus aliados ahora podéis ganar poder matando a los impíos y malvados.",
    ),
    (
        "religion.txt",
        "You no longer exude an aura of power that intimidates your foes.",
        "Ya no exudes un aura de poder que intimida a tus enemigos.",
        "Ya no exudas un aura de poder que intimide a tus enemigos.",
    ),
    (
        "religion.txt",
        "You now exude an aura of power that intimidates your foes.",
        "Ahora exudes un aura de poder que intimida a tus enemigos.",
        "Ahora exudas un aura de poder que intimida a tus enemigos.",
    ),
    # ═══ inventory.txt ═══
    ("inventory.txt", "dragon hide", "dragón", "piel de dragón"),
    ("inventory.txt", "dragon scales", "básculas de dragón", "escamas de dragón"),
    (
        "inventory.txt",
        "BUG WARNING: Item didn't seem to be linked at all.",
        "el artículo no parecía estar relacionado en absoluto.",
        "AVISO DE ERROR: El artículo no parecía estar vinculado.",
    ),
    ("inventory.txt", "malachite amulet", "malachite amuleto", "amuleto de malaquita"),
    ("inventory.txt", "old blowgun", "vieja escopeta", "vieja cerbatana"),
    ("inventory.txt", "old great sword", "vieja espada", "vieja espada grande"),
    ("inventory.txt", "old scythe", "viejo cigarro", "vieja guadaña"),
    ("inventory.txt", "old spiked flail", "viejo caracola", "viejo mayal con púas"),
    ("inventory.txt", "removed troll hide", "oculto de Trol", "piel de trol eliminada"),
    ("inventory.txt", "old cutlass", "viejo cutlas", "viejo alfanje"),
    ("inventory.txt", "old falchion", "viejo alfanje", "viejo falcado"),
    ("inventory.txt", "old fustibalus", "viejo fustibalus", "viejo fustíbalo"),
]


def apply_fixes(filepath, fixes_for_file):
    """Aplica las correcciones a un archivo."""
    with open(filepath) as f:
        content = f.read()

    changes = 0
    for en, old_es, new_es in fixes_for_file:
        # Buscar la línea exacta: en|old_es
        old_line = f"{en}|{old_es}"
        new_line = f"{en}|{new_es}"

        if old_line in content:
            content = content.replace(old_line, new_line)
            changes += 1
        else:
            # Intentar con \n al final si la línea original lo tenía
            old_line_nl = old_line + "\n"
            new_line_nl = new_line + "\n"
            if old_line_nl in content:
                content = content.replace(old_line_nl, new_line_nl)
                changes += 1
            else:
                # Buscar variante: puede que tenga espacios extra
                found = False
                for line in content.split("\n"):
                    stripped = line.strip()
                    if "|" in stripped:
                        en_part, es_part = stripped.split("|", 1)
                        if en_part.strip() == en and es_part.strip() == old_es:
                            # Reemplazar esta línea específica
                            old_exact = line
                            # Preservar espacios/indentación original
                            indent = line[: len(line) - len(line.lstrip())]
                            new_exact = indent + new_line
                            content = content.replace(old_exact, new_exact)
                            changes += 1
                            found = True
                            break
                if not found:
                    print(f"  ⚠️  No se encontró: {en}|{old_es}")

    with open(filepath, "w") as f:
        f.write(content)

    return changes


def main():
    # Agrupar correcciones por archivo
    fixes_by_file = {}
    for fname, en, old, new in FIXES:
        fixes_by_file.setdefault(fname, []).append((en, old, new))

    total_changes = 0
    for fname, fixes in sorted(fixes_by_file.items()):
        fpath = os.path.join(BASE, fname)
        if not os.path.exists(fpath):
            print(f"⚠️  {fname} no existe")
            continue

        # Backup
        bak = fpath + ".bak2"
        with open(fpath) as f:
            original = f.read()
        with open(bak, "w") as f:
            f.write(original)

        changes = apply_fixes(fpath, fixes)
        total_changes += changes
        print(f"✅ {fname}: {changes} correcciones aplicadas (backup: .bak2)")

    print(f"\n📊 Total: {total_changes} correcciones aplicadas")
    print("   Para restaurar: mv <archivo>.bak2 <archivo>")


if __name__ == "__main__":
    main()
