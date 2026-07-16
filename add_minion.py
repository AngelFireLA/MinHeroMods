import shutil
from pathlib import Path

import build_swf
# Need to have been extracted using the extract_from_swf.bat script.
minion_dex_id_path = r"source\scripts\States\MinionDexID.as"
all_minions_container_path = r"source\scripts\Minions\AllMinionsContainer.as"
symbol_classes_path = r"source\symbolClass\symbols.csv"
images_folder_path = r"source\images"

# Path to your minion's image
new_minion_image_path = r"C:\Dev\basard\Min Hero\MinHeroMods\eevee_minion.png"

def add_dex_id(minion_code_name):
    # We need to add the minion to the DEX IDs file, but it can't just be the last one, it needs to be before the 4 not-really-minions.
    with open(minion_dex_id_path, "r") as f:
        content = f.read()

        # We get the first line that contains the start of the not-really-minions
        line_to_replace = next(line for line in content.splitlines() if "public static const DEX_ID_battleModMinion_1:int =" in line)
        # We get the number from the line, and add 1 to it, because the original number will be the ID of our new minion
        first_num = int(line_to_replace.split("=")[1].strip().rstrip(";"))

        # We replace the 4 not-really-minions lines with their old numbers + 1
        new_line_to_replace =  f"      public static const DEX_ID_battleModMinion_1:int = {first_num+1};"
        content = content.replace(line_to_replace, new_line_to_replace)

        line_to_replace = next(line for line in content.splitlines() if "public static const DEX_ID_battleModMinion_2:int =" in line)
        new_line_to_replace =  f"      public static const DEX_ID_battleModMinion_2:int = {first_num+2};"
        content = content.replace(line_to_replace, new_line_to_replace)

        line_to_replace = next(line for line in content.splitlines() if "public static const DEX_ID_battleModMinion_3:int =" in line)
        new_line_to_replace =  f"      public static const DEX_ID_battleModMinion_3:int = {first_num+3};"
        content = content.replace(line_to_replace, new_line_to_replace)

        line_to_replace = next(line for line in content.splitlines() if "public static const DEX_ID_testing_minion:int =" in line)
        new_line_to_replace =  f"      public static const DEX_ID_testing_minion:int = {first_num+4};"
        content = content.replace(line_to_replace, new_line_to_replace)

        # We also edit the total number of minions
        total_num_line = next(line for line in content.splitlines() if "public static const TOTAL_NUM_OF_MINIONS:int =" in line)
        minion_amount_line =  f"      public static const TOTAL_NUM_OF_MINIONS:int = {first_num+5};"

        # We add our new minion line
        new_minion_line = f"      public static const DEX_ID_{minion_code_name}:int = {first_num};"
        content = content.replace(total_num_line, f"{new_minion_line}\n\n{minion_amount_line}")
        
    with open(minion_dex_id_path, "w") as f:
        f.write(content)


def add_minion_container(minion_code_name:str, minion_name:str, icon_offset_x:int, icon_offset_y:int, exp_gain_rate:str, number_of_gems:int, starting_moves_ids:list, base_health:int, base_energy:int, base_attack:int, base_healing:int, base_speed:int, specialized_move_ids:list, minion_type1:str, minion_type2: str = None):
    
    # Constants so we don't have to remember the exact strings
    exp_gain_rates = {"very easy":"ExpGainRates.EXP_GAIN_RATE_VERY_EASY", "easy":"ExpGainRates.EXP_GAIN_RATE_EASY", "normal":"ExpGainRates.EXP_GAIN_RATE_NORMAL", "hard":"ExpGainRates.EXP_GAIN_RATE_HARD", "very hard":"ExpGainRates.EXP_GAIN_RATE_VERY_HARD"}
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
        "dino": "TYPE_DINO"
    }
    
    # We check that the arguments are mostly valid
    if exp_gain_rate not in exp_gain_rates:
        raise ValueError(f"Exp Gain rate {exp_gain_rate} for minion {minion_code_name} isn't valid.")
    if minion_type1 not in minion_types:
        raise ValueError(f"Minion type {minion_type1} for minion {minion_code_name} isn't valid.")
    if minion_type2 and minion_type2 not in minion_types:
        raise ValueError(f"Minion type {minion_type2} for minion {minion_code_name} isn't valid.")
    if len(specialized_move_ids) != 3:
        raise ValueError(f"You must have exactly 3 specialized moves for minion {minion_code_name}. (Currently {len(specialized_move_ids)})")

    # We replace the simple string with the code string
    exp_gain_rate = exp_gain_rates[exp_gain_rate]

    # We handle the cases where there are more than one starting move
    starting_moves_line = "\n".join([f"         _loc1_.AddStartingMove({move_id}); " for move_id in starting_moves_ids])
    
    # We have to handle the cases where the minions has either 1 or two types
    minion_type_str = f"MinionType.{minion_types[minion_type1]}" if not minion_type2 else f"MinionType.{minion_types[minion_type1]},MinionType.{minion_types[minion_type2]}"
    
    # The function for the minions container that includes information about the minion
    minion_code_block = f"""
      private function {minion_code_name}() : void
      {{
         var _loc2_:MinionTalentTree = null;
         var _loc1_:BaseMinion = this.CM(MinionDexID.DEX_ID_{minion_code_name},"{minion_name}","{minion_code_name}",{base_health},{base_energy},{base_attack},{base_healing},{base_speed},{minion_type_str});
         _loc1_.m_minionIconPositioningX = {icon_offset_x};
         _loc1_.m_minionIconPositioningY = {icon_offset_y};
         _loc1_.m_expGainRate = {exp_gain_rate};
         _loc1_.m_numberOfGems = {number_of_gems-1};
         _loc1_.m_numberOfLockedGems = {4-number_of_gems};
{starting_moves_line}
         _loc1_.SetSpeacilizaionMoves({specialized_move_ids[0]},{specialized_move_ids[1]},{specialized_move_ids[2]});
         _loc2_ = Singleton.staticData.m_baseTalentTreesList.Tortoise_Armor();
         _loc1_.SetTalentTree(0,_loc2_);
         _loc2_ = Singleton.staticData.m_baseTalentTreesList.Tortoise_Health();
         _loc1_.SetTalentTree(1,_loc2_);
         _loc2_ = Singleton.staticData.m_baseTalentTreesList.Tortoise_Buffs();
         _loc1_.SetTalentTree(2,_loc2_);
      }}
      """

    # the function needs to be initialized in the AllMinionsContainer.as file
    init_line = f"         this.{minion_code_name}();"

    with open(all_minions_container_path, "r") as f:
        content = f.read()
        all_lines = content.splitlines()

        # we find the last line that contains "_loc1_.SetTalentTree" because we know it will be the next-to-last line before the end of the functions
        # so we can just add our own function 2 lines below that
        for i in range(len(all_lines)-1, -1, -1):
            if "_loc1_.SetTalentTree" in all_lines[i]:
                insert_index = i
                break   
        insert_index += 2
        all_lines.insert(insert_index, minion_code_block)

        # we get the start of the function just before where we'll have to init our function
        cm_index = next(i for i, line in enumerate(all_lines) if "private function CM(" in line)
        
        # we get the first } before the cm_index because it will be the end of the function where we want to add the init line
        # so we can add our init line before the last closing brace
        for i in range(cm_index-1, -1, -1):
            if "}" in all_lines[i]:
                last_closing_brace_index = i
                break
        all_lines.insert(last_closing_brace_index, init_line)
        content = "\n".join(all_lines)

    with open(all_minions_container_path, "w") as f:
        f.write(content)




def add_image(image_path, minion_code_name):
    """Copy a new minion image into source using the exported JPEXS naming style."""
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Minion image does not exist: {image_path}")

    symbol_path = Path(symbol_classes_path)
    rows = []
    for line in symbol_path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        character_id_text, class_name = line.split(";", 1)
        rows.append((int(character_id_text), class_name))

    class_name = f"Utilities.SpriteHandler_{minion_code_name}"
    if any(existing_class == class_name for _, existing_class in rows):
        raise ValueError(f"SymbolClass already exists: {class_name}")

    new_index = max((character_id for character_id, _ in rows), default=0) + 1
    extension = image_path.suffix.lower() or ".png"
    new_file_name = f"{new_index}_{class_name}{extension}"
    destination = Path(images_folder_path) / new_file_name
    if destination.exists():
        raise FileExistsError(f"Image destination already exists: {destination}")

    shutil.copy2(image_path, destination)
    rows.append((new_index, class_name))
    symbol_path.write_text(
        "".join(f"{character_id};{symbol}\n" for character_id, symbol in rows),
        encoding="utf-8",
    )
    print(f"Prepared new image {destination} with character ID {new_index}.")
    return new_index


def add_minion():
    add_dex_id("eeveeMinion")
    add_minion_container("eeveeMinion", "Eevee", 0, 0, "normal", 4, [1, 4, 7], 100, 100, 100, 100, 100, [8, 5, 6], "water")
    add_image(new_minion_image_path, "eeveeMinion")
    build_swf.main()
    print("Minion added and default.swf built successfully.")


if __name__ == "__main__":
    add_minion()

