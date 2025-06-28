from PIL import Image
import zlib
import subprocess
# Need to have been extracted using the extract_from_swf.bat script.
minion_dex_id_path = "source\scripts\States\MinionDexID.as"
all_minions_container_path = "source\scripts\Minions\AllMinionsContainer.as"
symbol_classes_path = "source\symbolClass\symbols.csv"
images_folder_path = "source\images"

# Path to your minion's image
new_minion_image_path = r"C:\Dev\basard\Min Hero\MinHeroMods\eevee_minion.png"

# Unmodified SWF 
base_swf_path = "original.swf"

# Final SWF after modifications
final_swf_path = "default.swf"

intermediary_xml_path = "dump.xml"

# Path to the modified file detector script so we don't recompile every script every time
modified_file_detector_script_path = "modified_detector.py"

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
    print("Starting swf2xml...")
    subprocess.run(fr'"jpexs\ffdec-cli.exe" -swf2xml {base_swf_path} {intermediary_xml_path}', shell=True)
    print("SWF to XML conversion completed.")
    # open dump.xml

    with open(intermediary_xml_path, "r") as f:
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

    closing_tag_indices = [i for i, line in enumerate(dump_lines) if "</tags>" in line]
    third_index = closing_tag_indices[2]
    dump_lines.insert(third_index, f"        <item>{new_index}</item>\n")
    name_tag_indices = [i for i, line in enumerate(dump_lines) if "</names>" in line]
    last_index = name_tag_indices[-1]
    dump_lines.insert(last_index, f"        <item>Utilities.SpriteHandler_{minion_code_name}</item>\n")

    string_to_add = f"""
    <item type="DoABC2Tag" flags="0" forceWriteAsLong="false" name="Utilities.SpriteHandler_{minion_code_name}">
      <abc type="ABC">
        <version type="ABCVersion" major="46" minor="16"/>
        <constants type="AVM2ConstantPool">
          <constant_int/>
          <constant_uint/>
          <constant_double/>
          <constant_decimal/>
          <constant_float/>
          <constant_float4/>
          <constant_string>
            <item isNull="true"/>
            <item>http://adobe.com/AS3/2006/builtin</item>
            <item>Utilities</item>
            <item>SpriteHandler_{minion_code_name}</item>
            <item>Object</item>
            <item/>
            <item>Utilities:SpriteHandler_{minion_code_name}</item>
          </constant_string>
          <constant_namespace>
            <item isNull="true"/>
            <item type="Namespace" kind="8" name_index="1"/>
            <item type="Namespace" kind="22" name_index="2"/>
            <item type="Namespace" kind="22" name_index="5"/>
            <item type="Namespace" kind="5" name_index="6"/>
            <item type="Namespace" kind="24" name_index="6"/>
          </constant_namespace>
          <constant_namespace_set>
            <item isNull="true"/>
            <item type="NamespaceSet">
              <namespaces>
                <item>2</item>
              </namespaces>
            </item>
          </constant_namespace_set>
          <constant_multiname>
            <item isNull="true"/>
            <item type="Multiname" kind="7" name_index="3" namespace_index="2" namespace_set_index="0" qname_index="0"/>
            <item type="Multiname" kind="7" name_index="4" namespace_index="3" namespace_set_index="0" qname_index="0"/>
            <item type="Multiname" kind="9" name_index="3" namespace_index="0" namespace_set_index="1" qname_index="0"/>
          </constant_multiname>
        </constants>
        <method_info>
          <item type="MethodInfo" flags="0" name_index="5" ret_type="0">
            <param_types/>
            <optional/>
            <paramNames/>
          </item>
          <item type="MethodInfo" flags="0" name_index="0" ret_type="0">
            <param_types/>
            <optional/>
            <paramNames/>
          </item>
          <item type="MethodInfo" flags="0" name_index="5" ret_type="0">
            <param_types/>
            <optional/>
            <paramNames/>
          </item>
        </method_info>
        <metadata_info/>
        <instance_info>
          <item type="InstanceInfo" flags="9" iinit_index="1" name_index="1" protectedNS="5" super_index="2">
            <interfaces/>
            <instance_traits type="Traits">
              <traits/>
            </instance_traits>
          </item>
        </instance_info>
        <class_info>
          <item type="ClassInfo" cinit_index="2">
            <static_traits type="Traits">
              <traits/>
            </static_traits>
          </item>
        </class_info>
        <script_info>
          <item type="ScriptInfo" init_index="0">
            <traits type="Traits">
              <traits>
                <item type="TraitClass" class_info="0" deleted="false" fileOffset="0" kindFlags="0" kindType="4" name_index="1" slot_id="1">
                  <metadata/>
                </item>
              </traits>
            </traits>
          </item>
        </script_info>
        <bodies>
          <item type="MethodBody" init_scope_depth="1" max_regs="1" max_scope_depth="3" max_stack="2" method_info="0">
            <exceptions/>
            <traits type="Traits">
              <traits/>
            </traits>
          </item>
          <item type="MethodBody" init_scope_depth="4" max_regs="1" max_scope_depth="5" max_stack="1" method_info="1">
            <exceptions/>
            <traits type="Traits">
              <traits/>
            </traits>
          </item>
          <item type="MethodBody" init_scope_depth="3" max_regs="1" max_scope_depth="4" max_stack="1" method_info="2">
            <exceptions/>
            <traits type="Traits">
              <traits/>
            </traits>
          </item>
        </bodies>
      </abc>
    </item>
"""
    idk = [i for i, line in enumerate(dump_lines) if '<item type="ExportAssetsTag" forceWriteAsLong="true">' in line]
    last_index = idk[0]
    # add the string_to_add before the last index
    dump_lines.insert(last_index, string_to_add)


    with open(intermediary_xml_path, "w") as f:
        f.writelines(dump_lines)

    print("Starting xml2swf...")
    subprocess.run(fr'"jpexs\ffdec-cli.exe" -xml2swf {intermediary_xml_path} {final_swf_path}', shell=True)
    print("SWF to XML conversion completed.")

    print("Starting modified file detector script...")
    subprocess.run(fr'python {modified_file_detector_script_path}', shell=True)
    print("Modified file detector script completed.")

    # swf2swf
    print("Starting importing scripts into swf file...")
    subprocess.run(fr'"jpexs\ffdec-cli.exe" -importScript {final_swf_path} {final_swf_path} modified', shell=True)
    print("Scripts imported successfully.")



def add_minion():
    add_dex_id("eeveeMinion")
    add_minion_container("eeveeMinion", "Eevee", 0, 0, "normal", 4, [1, 4, 7], 100, 100, 100, 100, 100, [8, 5, 6], "water")
    add_image(new_minion_image_path, "eeveeMinion")
    print("Minion added successfully. Please check the output for any errors.")


if __name__ == "__main__":
    add_minion()