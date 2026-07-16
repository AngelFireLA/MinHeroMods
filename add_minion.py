"""Add one toggleable custom minion to the exported Min Hero source tree."""

import re
import shutil
from pathlib import Path

import build_swf


ROOT = Path(__file__).resolve().parent
ALL_MINIONS_CONTAINER = ROOT / "source" / "scripts" / "Minions" / "AllMinionsContainer.as"
STATIC_DATA = ROOT / "source" / "scripts" / "PresistentData" / "StaticData.as"
MOD_MENU = ROOT / "source" / "scripts" / "MainMenu" / "ModMenu.as"
SETTINGS_MENU = ROOT / "source" / "scripts" / "TopDown" / "Menus" / "SettingsMenu.as"
MAIN_MENU_SCREEN = ROOT / "source" / "scripts" / "MainMenu" / "MainMenuScreen.as"
SYMBOL_CLASSES = ROOT / "source" / "symbolClass" / "symbols.csv"
IMAGES_FOLDER = ROOT / "source" / "images"

# Set this to True while testing. A newly created save will receive the custom
# minion instead of Tiger. The minion's toggle must also be ON for that save.
DEBUG_REPLACE_STARTER = False

# Minion to add. The code name is also its persistent mod/save identifier, so do
# not rename it after players have made saves containing this minion.
MINION_CODE_NAME = "eeveeMinion"
MINION_NAME = "Eevee"
MINION_DESCRIPTION = "Enable Eevee as a custom minion."
NEW_MINION_IMAGE = ROOT / "eevee_minion.png"


def read_source(path):
    return path.read_text(encoding="utf-8-sig")


def write_source(path, content):
    path.write_text(content, encoding="utf-8")


def insert_once(content, marker, addition, description, *, before=True):
    """Insert an exact block once, raising if the expected source anchor moved."""
    if addition.strip() in content:
        return content
    if marker not in content:
        raise RuntimeError(f"Cannot find {description} anchor; the game source changed again.")
    replacement = addition + marker if before else marker + addition
    return content.replace(marker, replacement, 1)


def register_minion_mod(minion_code_name, menu_name, description):
    """Register the minion in Dex allocation and both mod-toggle menus."""
    content = read_source(STATIC_DATA)
    registration = f'         this.m_all_minion_mods.push("{minion_code_name}");\n'
    content = insert_once(
        content,
        '         trace("All known minion mods:");',
        registration,
        "StaticData minion-mod list",
    )
    write_source(STATIC_DATA, content)

    content = read_source(MOD_MENU)
    menu_order = f'         this.m_toggleTexts.push("{menu_name}");\n'
    content = insert_once(
        content,
        "         this.m_toggleDict = new Dictionary();\n",
        menu_order,
        "new-save mod-menu ordering",
    )
    menu_entry = (
        f'         this.m_toggleDict["{menu_name}"] = '
        f'["{description}", "{minion_code_name}"];\n'
    )
    content = insert_once(
        content,
        '         this.m_toggleDict["Example"]',
        menu_entry,
        "new-save mod-menu dictionary",
    )
    write_source(MOD_MENU, content)

    content = read_source(SETTINGS_MENU)
    settings_entry = (
        f'         this.m_modGroupNames.push("{menu_name}");\n'
        f'         this.m_modGroupMods.push(["{minion_code_name}"]);\n'
    )
    if settings_entry.strip() not in content:
        array_start = content.find("         this.m_modGroupMods = [")
        if array_start < 0:
            raise RuntimeError("Cannot find SettingsMenu mod-group array.")
        array_end = content.find("         ];", array_start)
        if array_end < 0:
            raise RuntimeError("Cannot find the end of SettingsMenu mod-group array.")
        array_end += len("         ];\n")
        content = content[:array_end] + settings_entry + content[array_end:]
    write_source(SETTINGS_MENU, content)


def add_minion_container(
    minion_code_name,
    minion_name,
    icon_offset_x,
    icon_offset_y,
    exp_gain_rate,
    number_of_gems,
    starting_moves_ids,
    base_health,
    base_energy,
    base_attack,
    base_healing,
    base_speed,
    specialized_move_ids,
    minion_type1,
    minion_type2=None,
):
    """Add a dynamically indexed BaseMinion guarded by its saved toggle."""
    exp_gain_rates = {
        "very easy": "ExpGainRates.EXP_GAIN_RATE_VERY_EASY",
        "easy": "ExpGainRates.EXP_GAIN_RATE_EASY",
        "normal": "ExpGainRates.EXP_GAIN_RATE_NORMAL",
        "hard": "ExpGainRates.EXP_GAIN_RATE_HARD",
        "very hard": "ExpGainRates.EXP_GAIN_RATE_VERY_HARD",
    }
    minion_types = {
        "energy": "TYPE_ENERGY",
        "undead": "TYPE_UNDEAD",
        "robot": "TYPE_ROBOT",
        "fire": "TYPE_FIRE",
        "water": "TYPE_WATER",
        "ice": "TYPE_ICE",
        "demonic": "TYPE_DEMONIC",
        "holy": "TYPE_HOLY",
        "earth": "TYPE_EARTH",
        "plant": "TYPE_PLANT",
        "flying": "TYPE_FLYING",
        "titan": "TYPE_TITAN",
        "normal": "TYPE_NORMAL",
        "dino": "TYPE_DINO",
    }

    if not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", minion_code_name):
        raise ValueError(f"Invalid ActionScript/mod identifier: {minion_code_name}")
    if exp_gain_rate not in exp_gain_rates:
        raise ValueError(f"Invalid exp gain rate for {minion_code_name}: {exp_gain_rate}")
    if minion_type1 not in minion_types:
        raise ValueError(f"Invalid primary type for {minion_code_name}: {minion_type1}")
    if minion_type2 and minion_type2 not in minion_types:
        raise ValueError(f"Invalid secondary type for {minion_code_name}: {minion_type2}")
    if not 1 <= number_of_gems <= 4:
        raise ValueError("number_of_gems must be from 1 to 4")
    if len(specialized_move_ids) != 3:
        raise ValueError("Exactly three specialization moves are required")

    starting_moves = "\n".join(
        f"         _loc1_.AddStartingMove({move_id});" for move_id in starting_moves_ids
    )
    type_arguments = f"MinionType.{minion_types[minion_type1]}"
    if minion_type2:
        type_arguments += f",MinionType.{minion_types[minion_type2]}"

    method = f'''      private function {minion_code_name}() : void
      {{
         var _loc2_:MinionTalentTree = null;
         var _loc1_:BaseMinion = this.CM(Singleton.staticData.ModToDexID["{minion_code_name}"],"{minion_name}","{minion_code_name}",{base_health},{base_energy},{base_attack},{base_healing},{base_speed},{type_arguments});
         _loc1_.m_minionIconPositioningX = {icon_offset_x};
         _loc1_.m_minionIconPositioningY = {icon_offset_y};
         _loc1_.m_expGainRate = {exp_gain_rates[exp_gain_rate]};
         _loc1_.m_numberOfGems = {number_of_gems - 1};
         _loc1_.m_numberOfLockedGems = {4 - number_of_gems};
{starting_moves}
         _loc1_.SetSpeacilizaionMoves({specialized_move_ids[0]},{specialized_move_ids[1]},{specialized_move_ids[2]});
         _loc2_ = Singleton.staticData.m_baseTalentTreesList.Tortoise_Armor();
         _loc1_.SetTalentTree(0,_loc2_);
         _loc2_ = Singleton.staticData.m_baseTalentTreesList.Tortoise_Health();
         _loc1_.SetTalentTree(1,_loc2_);
         _loc2_ = Singleton.staticData.m_baseTalentTreesList.Tortoise_Buffs();
         _loc1_.SetTalentTree(2,_loc2_);
      }}

'''
    constructor_block = f'''         if(Singleton.dynamicData.m_isMod["{minion_code_name}"])
         {{
            this.{minion_code_name}();
         }}
'''

    content = read_source(ALL_MINIONS_CONTAINER)
    content = insert_once(
        content,
        "         this.BattleMod_stage1();",
        constructor_block,
        "AllMinionsContainer constructor",
    )
    content = insert_once(
        content,
        "      private function BattleMod_stage1() : void",
        method,
        "AllMinionsContainer custom-minion methods",
    )
    write_source(ALL_MINIONS_CONTAINER, content)


def configure_debug_starter(minion_code_name, enabled):
    """Optionally replace Tiger in a newly created save with the custom minion."""
    content = read_source(MAIN_MENU_SCREEN)
    vanilla = "new OwnedMinion(MinionDexID.DEX_ID_Tiger_1); //change to DexID of any adding test minion"
    custom = (
        f'new OwnedMinion(Singleton.staticData.ModToDexID["{minion_code_name}"]); '
        "// DEBUG custom starter"
    )
    if enabled:
        if custom not in content:
            if vanilla not in content:
                raise RuntimeError("Cannot find the Tiger starter line in MainMenuScreen.as.")
            content = content.replace(vanilla, custom, 1)
    elif custom in content:
        content = content.replace(custom, vanilla, 1)
    write_source(MAIN_MENU_SCREEN, content)


def add_image(image_path, minion_code_name):
    """Copy a new minion image into source using the exported JPEXS naming style."""
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Minion image does not exist: {image_path}")

    rows = []
    for line in read_source(SYMBOL_CLASSES).splitlines():
        if line.strip():
            character_id_text, class_name = line.split(";", 1)
            rows.append((int(character_id_text), class_name))

    class_name = f"Utilities.SpriteHandler_{minion_code_name}"
    existing = next(((item_id, name) for item_id, name in rows if name == class_name), None)
    if existing:
        matching_images = list(IMAGES_FOLDER.glob(f"{existing[0]}_{class_name}.*"))
        if not matching_images:
            raise RuntimeError(f"{class_name} is registered but its image is missing.")
        print(f"Image already registered: {matching_images[0]}")
        return existing[0]

    new_index = max((character_id for character_id, _ in rows), default=0) + 1
    extension = image_path.suffix.lower() or ".png"
    destination = IMAGES_FOLDER / f"{new_index}_{class_name}{extension}"
    if destination.exists():
        raise FileExistsError(f"Image destination already exists: {destination}")

    shutil.copy2(image_path, destination)
    rows.append((new_index, class_name))
    write_source(
        SYMBOL_CLASSES,
        "".join(f"{character_id};{symbol}\n" for character_id, symbol in rows),
    )
    print(f"Prepared new image {destination} with character ID {new_index}.")
    return new_index


def add_minion():
    register_minion_mod(MINION_CODE_NAME, MINION_NAME, MINION_DESCRIPTION)
    add_minion_container(
        MINION_CODE_NAME,
        MINION_NAME,
        0,
        0,
        "normal",
        4,
        [1, 4, 7],
        100,
        100,
        100,
        100,
        100,
        [8, 5, 6],
        "water",
    )
    configure_debug_starter(MINION_CODE_NAME, DEBUG_REPLACE_STARTER)
    add_image(NEW_MINION_IMAGE, MINION_CODE_NAME)
    build_swf.main()
    print("Minion added and default.swf built successfully.")


if __name__ == "__main__":
    add_minion()
