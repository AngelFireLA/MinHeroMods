from PIL import Image
import zlib
minion_dex_id_path = "source\scripts\States\MinionDexID.as"
all_minions_container_path = "source\scripts\Minions\AllMinionsContainer.as"
symbol_classes_path = "source\symbolClass\symbols.csv"
new_minion_image_path = r"C:\Dev\basard\Min Hero\MinHeroMods\eevee_minion.png"
images_folder_path = "source\images"

def add_dex_id(minion_code_name):
    with open(minion_dex_id_path, "r") as f:
        content = f.read()

        line_to_replace = next(line for line in content.splitlines() if "public static const DEX_ID_battleModMinion_1:int =" in line)
        first_num = int(line_to_replace.split("=")[1].strip().rstrip(";"))
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

        total_num_line = next(line for line in content.splitlines() if "public static const TOTAL_NUM_OF_MINIONS:int =" in line)
        minion_amount_line =  f"      public static const TOTAL_NUM_OF_MINIONS:int = {first_num+5};"
        new_minion_line = f"      public static const DEX_ID_{minion_code_name}:int = {first_num};"
        content = content.replace(total_num_line, f"{new_minion_line}\n\n{minion_amount_line}")
        
    with open(minion_dex_id_path, "w") as f:
        f.write(content)

def add_minion_container(minion_code_name:str, minion_name:str, icon_offset_x:int, icon_offset_y:int, exp_gain_rate:str, number_of_gems:int, starting_moves_ids:list, base_health:int, base_energy:int, base_attack:int, base_healing:int, base_speed:int, specialized_move_ids:list, minion_type1:str, minion_type2: str = None):
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
    if exp_gain_rate not in exp_gain_rates:
        raise ValueError(f"Exp Gain rate {exp_gain_rate} for minion {minion_code_name} isn't valid.")
    if minion_type1 not in minion_types:
        raise ValueError(f"Minion type {minion_type1} for minion {minion_code_name} isn't valid.")
    if minion_type2 and minion_type2 not in minion_types:
        raise ValueError(f"Minion type {minion_type2} for minion {minion_code_name} isn't valid.")
    if len(specialized_move_ids) != 3:
        raise ValueError(f"You must have exactly 3 specialized moves for minion {minion_code_name}. (Currently {len(specialized_move_ids)})")

    exp_gain_rate = exp_gain_rates[exp_gain_rate]
    starting_moves_line = "\n".join([f"         _loc1_.AddStartingMove({move_id}); " for move_id in starting_moves_ids])
    minion_type_str = f"MinionType.{minion_types[minion_type1]}" if not minion_type2 else f"MinionType.{minion_types[minion_type1]},MinionType.{minion_types[minion_type2]}"
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

    init_line = f"         this.{minion_code_name}();"
    with open(all_minions_container_path, "r") as f:
        content = f.read()
        all_lines = content.splitlines()

        # add codeblock before the last function in the file
        for i in range(len(all_lines)-1, -1, -1):
            if "_loc1_.SetTalentTree" in all_lines[i]:
                insert_index = i
                break   
        insert_index += 2
        all_lines.insert(insert_index, minion_code_block)

        # get the index of the line that contains "private function CM"
        cm_index = next(i for i, line in enumerate(all_lines) if "private function CM(" in line)
        # get the first line that contains } in the lines before the cm_index
        for i in range(cm_index-1, -1, -1):
            if "}" in all_lines[i]:
                last_closing_brace_index = i
                break
        # add the init line before the last closing brace
        all_lines.insert(last_closing_brace_index, init_line)
        content = "\n".join(all_lines)
    with open(all_minions_container_path, "w") as f:
        f.write(content)



    #private function CM(param1:int, param2:String, param3:String, param4:int, param5:int, param6:int, param7:int, param8:int, param9:int, param10:int = 0) : BaseMinion

def add_image(image_path, minion_code_name):

    # open the symbols.csv file and get the last value of the first column
    with open(symbol_classes_path, "r") as f:
        lines = f.readlines()
        # remove any empty lines
        lines = [line for line in lines if line.strip()]
        last_value = lines[-1].split(";")[0] 
    new_index = int(last_value) + 1
    new_file_name = f"{new_index}_Utilities.SpriteHandler_{minion_code_name}.png"

    new_line = f"{new_index};Utilities.SpriteHandler_{minion_code_name}\n"
    with open(symbol_classes_path, "w") as f:
        f.writelines(lines)
        f.write(new_line)

    custom_sprite_handler_path = f"source/scripts/Utilities/SpriteHandler_{minion_code_name}.as"
    custom_sprite_handler_content = f"""
package Utilities
{{
   import mx.core.BitmapAsset;
   
   [Embed(source="/_assets/{new_file_name}")]
   public class SpriteHandler_{minion_code_name} extends BitmapAsset
   {{
       
      public function SpriteHandler_{minion_code_name}()
      {{
         super();
      }}
   }}
}}
"""
    with open(custom_sprite_handler_path, "w") as f:
        f.write(custom_sprite_handler_content)

    main_sprite_handler_path = f"source/scripts/Utilities/SpriteHandler.as"
    custom_minion_line = f"      private static var {minion_code_name}:Class = SpriteHandler_{minion_code_name};\n"

    with open(main_sprite_handler_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "public class SpriteHandler" in line:
                lines.insert(i + 2, custom_minion_line)
                break
    with open(main_sprite_handler_path, "w") as f:
        f.writelines(lines)

    # open dump.xml
    dump_xml_path = "dump.xml"
    with open(dump_xml_path, "r") as f:
        dump_lines = f.readlines()

    # find the first line containing '<item type="DefineBitsLossless2Tag" bitmapColorTableSize="0"'
    define_bits_index = None
    for idx, line in enumerate(dump_lines):
        if '<item type="DefineBitsLossless2Tag" bitmapColorTableSize="0"' in line:
            define_bits_index = idx
            break

    im = Image.open(image_path).convert("RGBA")
    w, h = im.size

    # 2) Split & re-merge, swapping R and B → now each pixel is B,G,R,A
    r, g, b, a = im.split()
    bgra = Image.merge("RGBA", (a, r, g, b))

    # 3) Get the raw bytes and compress them
    raw = bgra.tobytes()        # length = w*h*4
    comp = zlib.compress(raw)
    hexstr = comp.hex()
    image_string = f"""
    <item type="DefineBitsLossless2Tag" bitmapColorTableSize="0" bitmapFormat="5" bitmapHeight="{h}" bitmapWidth="{w}" characterID="{new_index}" forceWriteAsLong="true" zlibBitmapData="{hexstr}"/>
"""
    # insert the image_string on the line just before the define_bits_index
    dump_lines.insert(define_bits_index, image_string)

    # find all the indices where </tags> appears
    closing_tag_indices = [i for i, line in enumerate(dump_lines) if "</tags>" in line]
    # the 3rd occurrence is at index 2 in that list
    third_index = closing_tag_indices[2]
    # insert your new <item> line just above it
    dump_lines.insert(third_index, f"        <item>{new_index}</item>\n")

    # find all the indices where </names> appears
    name_tag_indices = [i for i, line in enumerate(dump_lines) if "</names>" in line]
    last_index = name_tag_indices[-1]
    # insert your new <item> line just above it
    dump_lines.insert(last_index, f"        <item>Utilities.SpriteHandler_{minion_code_name}</item>\n")


    with open(dump_xml_path, "w") as f:
        f.writelines(dump_lines)


def add_minion():
    add_dex_id("eeveeMinion")
    add_minion_container("eeveeMinion", "Eevee", 0, 0, "normal", 4, [1, 2, 3], 100, 100, 100, 100, 100, [4, 5, 6], "water")
    add_image(new_minion_image_path, "eeveeMinion")


if __name__ == "__main__":
    add_minion()
    print("Minion added successfully.")