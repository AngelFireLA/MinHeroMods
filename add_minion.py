minion_dex_id_path = "source\scripts\States\MinionDexID.as"
all_minions_container_path = "source\scripts\Minions\AllMinionsContainer.as"

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

def add_minion():
    add_dex_id("testMinion")
    add_minion_container("testMinion", "Eevee", 0, 0, "normal", 4, [1, 2, 3], 100, 100, 100, 100, 100, [4, 5, 6], "normal")


if __name__ == "__main__":
    add_minion()
    print("Minion added successfully.")