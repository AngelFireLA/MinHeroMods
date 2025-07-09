"""
This Python script (maintained by square_nine) is used to provide Python-ized versions of scripts used within the game, as well as utilities to create game-ready code!
These can then be used to streamline the mod creation process, by turning laborious calculations and hand-typing into a few modifications to a template.

The functions can then be used in the following applications/ideas:
* A Mod application tool, calling these functions to provide the inserting text which can then be inserted using FFDec
* Data extraction within SWF, calling these functions in reverse to extract data, for usage as cached data in an application or for the remaster

There are some utilities in here too:
* AutoIndent -> automatically indents a string block X times, which is useful when needing to match an indent level

See the "init" dictionaries for the format that is required, happy modding!
"""


#Compilation of functions that can be used to covert max-level game health to coded value for it. Use the "Calc" version to take a coded value into the actual value, and the "Reverse" to put a maximum health and covert it into the game value.
#i.e use the "Reverse" to get the value you need in init_minion, and "Calc" to verify (in the case of rounding)
def CalcMinionHealthSimple(baseHealth):       return baseHealth * 6 + 5
def ReverseMinionHealthSimple(finalHealth):   return (finalHealth-5)/6
def CalcMinionEnergySimple(baseEnergy):       return ((baseEnergy * 3)+5)*1.5
def ReverseMinionEnergySimple(finalEnergy):   return ((finalEnergy/1.5) - 5)/3
def CalcMinionAttackSimple(baseEnergy):       return ((baseEnergy * 3)+5)
def ReverseMinionAttackSimple(finalEnergy):   return ((finalEnergy) - 5)/3
def CalcMinionHealingSimple(baseEnergy):      return ((baseEnergy * 3)+5)
def ReverseMinionHealingSimple(finalEnergy):  return ((finalEnergy) - 5)/3
def CalcMinionSpeedSimple(baseEnergy):        return ((baseEnergy * 3)+5)
def ReverseMinionSpeedSimple(finalEnergy):    return ((finalEnergy) - 5)/3



#-> options for EXP_Gain_Rate option, ordered by the increase
EXP_GAIN_RATES = ["VERY_EASY","EASY","NORMAL","HARD","VERY_HARD"] 

# The MoveTuple is an intuitive way to store move data. 
# The first param is the name of the move, and the second is the level, from 1-5. 
# For unique names at level 5, instead use the name of the less powerful version, and put the level as 5
MOVE_TUPLE_EXAMPLE = ("ExampleMoveName",2) 

#MINION DICT -> PUT YOUR DATA HERE!
init_minion = {"codename": "dirtFish", #the codename that was used in-game for the image as well as for the species
              "name": "Zanyu",        #the name that is used for displaying
              "health": 485,          #the following stats are the MAXIMUM values. These will be converted by the above functions
              "energy": 277,
              "speed": 170,
              "attack":260,
              "healing": 50,
              "numGems": 3,           #number of available gem sockets that arrive unlocked
              "numLockedGems": 1,     #number of locked gem sockets. Must be greater than zero, less than 4 - existing sockets
              "evoLevel": 1,          #The evolutionary level. 1 is the first minion, 2 is the second etc... (yes this can theoretically extend beyond 3)
              "EXP_Gain_Rate": "HARD",#How easy it is to gain EXP. Make this harder for more "powerful" minions
              "StartingMoves": [("Pound",2)], #starting moves as List[MoveTuple]
              "SkillTree1": "GroundAttacker_Ground", #Each Skill Tree must have an equivalent in the BaseTalentTreeContainer. Create one if you need one!
              "SkillTree2": "DirtFish_Flying",
              "SkillTree3": "HummingBird_Normal",
              "SpecialisationMoves": [("Stone Fall",1),("Flurry",1),("Mirror Skin",1)], #The 3 moves that preface each branch. All 3 MUST be present
              "Types": ["Flying", "Earth"], #Minion Types -> Keep in the list. At least 1, no more than 2 is recommended
              "IconPosX": 0, #modify if your thing needs displacement when in the game, or in the preview
              "IconPoxY": 0, 
              #"evolvesTo",: level it evolves at #uncomment if it evolves at that level. The name of the thing it evolves to need not be present as that is automatically calculated
              }

#SKILL TREE DICT -> Put your data here!
init_skill_tree = {"name": "DirtFish_Flying", #The codename for the skill tree, as welll as the actual name (after the underscore)
                   #Each branch needs to be created, using a list for each branch, and a list for each MoveSlot, and a tuple for each move. Add an extra "True" to the MoveTuple if it is dependent on the previous move slot. Add items from left to right as it appears from top to bottom.
                   "LeftBranch": [[("Focus",1),("Focus",2),("Focus",3)],[("Agility",1),("Agility",3)],[("Agility",4,True)]], 
                   "MiddleBranch": [[("Volley",1),("Volley",2)],[("Flurry",2),("Flurry",3),("Flurry",4)],[("Flurry",5,True)]],
                   "RightBranch":[[("Wind Lance",1),("Wind Lance",2),("Wind Lance",3)],[("Hurricane",2),("Hurricane",3)],[("Titan Slam",2),("Titan Slam",4)],[("Titan Slam",5,True)]]
                   }

def MoveToGameName(name:str,level:int):
  """Converts a name with a level to the in-game representation of it.
  So parameters of 'Steel Spike', 1 would yield 'steel_spike_t1'
  """
  return name.lower().replace(" ","_")+ f"_t{level}" #all that's needed. If a particular move tries a different name it can change

def AutoIndent(in_str:str,amount:int=2):
  """Indents the input string by the amount. Defaults to the one required for Talent Trees and Minions.
  Change amount to 3 for moves
  """
  for i in range(amount):
    out = in_str.replace("\n","\n\t")
  return out

def BuildSkillTreeLog(inp_talent_tree_file):
  """Finds all of the available skill trees, to verify if one exists. Could be used to create an internal log..."""
  try:
    with open(inp_talent_tree_file,"r") as file:
      data = file.readlines()
  except:
    raise ValueError("Path is not correct!")
  names = []
  for line in data:
    if "      public function " in line and "BaseTalentTreeContainer" not in line: #if it's the function name
      names.append(line.split("function")[1].split("()")[0]) #process
  return names

def AutoSkillTree(init_dict):
  """Takes in an initialising dict to create the necessary string for a skill tree. 
     Just copy and paste into the code!
     
     DICT FORMAT:

     "name" -> The codename for the skill tree. Can be as a tuple ("MinionName", "SkillTreeName") or the codename to use. If it's the codename, it must end in "_[TreeDisplayName]", where TreeDisplayName is the thing to show to the player

     "[Left/Middle/Right]Branch" -> The 3 different branches, the leftwards, middle and right ones respectively. These must contain a list of "move slots", where a "move slot" is itself a list of the moves within that slot
     The moves are of the form ("MoveName",Level,isDependentOnPriorSlot), where the final variable is an optional "True" boolean to specify if it's dependent on the move slot before it (not the move before it within the slot). DO NOT DO FOR THE FIRST ONE!!!!
     """
  #NAME -> Must be a full string name, or can be a length 2 tuple of ("MinionName", "SkillTreeName")
  if type(init_dict["name"]) != str:
    if type(init_dict["name"]) == tuple and len(init_dict["name"])==2:
      func_name = init_dict["name"][0]+"_"+init_dict["name"][1].lower()
      name = init_dict["name"][1]
    else:  raise ValueError("Name must be a string")
  else:
    func_name = init_dict["name"]
    name = init_dict["name"].split("_")[1]
  
  output = f"public function {func_name}() : MinionTalentTree\n" + "{\n\t"+f'var _loc1_:MinionTalentTree = new MinionTalentTree("{name}");'

  branches = [init_dict["LeftBranch"],init_dict["MiddleBranch"],init_dict["RightBranch"]]
  branch_id = 0 #current branch
  for branch in branches: #for each branch
    moveSlot_id = 0 #current move slot
    for moveSlot in branch: #for each of the slots along the branch
      for move in moveSlot: #for each move within a slot -> make sure it's in order!
        currMove = MoveToGameName(move[0],move[1])
        try: #might contain extra bool to show dependency on previous move slit
          if move[2]: #if it exists
            output += f'\n\t_loc1_.AddMoveToTree({branch_id},{moveSlot_id},MinionMoveID.{currMove},true);'
        except: #fails if it doesn't exist
          output += f'\n\t_loc1_.AddMoveToTree({branch_id},{moveSlot_id},MinionMoveID.{currMove});'
      moveSlot_id += 1
    branch_id += 1
  output += "\n\treturn _loc1_;\n}\n" #closing part
  return output



def AutoMinionCreator(init_dict):
  """Creates the necessary minion code from an input dict to be able to add into the game!
  """
  #verification stuff
  try:
    if init_dict["evolvesFrom"]:
      evolvesFrom = init_dict["evolvesFrom"] 
  except:
    evolvesFrom = None
  try:
    if init_dict["evolvesTo"]:
      evolvesTo = init_dict["evolvesTo"]
  except:
    evolvesTo = None
  name = init_dict["name"]
  codename = init_dict["codename"]
  output = f"private function {codename}_stage{init_dict['evoLevel']}() : void\n" + "{\n\tvar _loc2_:MinionTalentTree = null;\n\t" #declaration

  #MAIN CONSTRUCTOR
  output += f'var _loc1_:BaseMinion = this.CM(MinionDexID.DEX_ID_{codename}_{init_dict["evoLevel"]},"{name}","{codename}",{round(ReverseMinionHealthSimple(init_dict["health"]))},{round(ReverseMinionEnergySimple(init_dict["energy"]))},{round(ReverseMinionAttackSimple(init_dict["attack"]))},{round(ReverseMinionHealingSimple(init_dict["healing"]))},{round(ReverseMinionSpeedSimple(init_dict["speed"]))}'
  
  #ADDING TYPES
  if len(init_dict["Types"]) == 2 and type(init_dict["Types"]) == list:
    output += f",MinionType.TYPE_{init_dict['Types'][0]},MinionType.{init_dict['Types'][1]});\n\t"
  elif len(init_dict["Types"]) == 2 and type(init_dict["Types"]) == list:
    output += f",MinionType.TYPE_{init_dict['Types'][0]});\n\t"
  else: #assume it's just the type itself instead of list
    if type(init_dict["Types"]) == str: 
      output += f",MinionType.TYPE_{init_dict['Types']});\n\t"
    else:  raise ValueError("Mismatched type length")

#gems + icon positioning
  output += f"_loc1_.m_minionIconPositioningX = 0;\n\t_loc1_.m_minionIconPositioningY = 0;\n\t_loc1_.m_expGainRate = ExpGainRates.EXP_GAIN_RATE_{init_dict['EXP_Gain_Rate']}\n\t_loc1_.m_numberOfGems = {init_dict['numGems']};\n\t_loc1_.m_numberOfLockedGems = {init_dict['numLockedGems']};\n\t"

  #if evolves into something else
  if evolvesTo:
    output += f"_loc1_.m_evolutionLevel = {evolvesTo[1]};\n\t" #level it evolves at

  #starting moves
  for item in init_dict['StartingMoves']: #add starting moves
    output += f'_loc1_.AddStartingMove(MinionMoveID.{MoveToGameName(item[0],item[1])});\n\t_loc1_.SetSpeacilizaionMoves('
  
  #specialising moves
  for item in init_dict['SpecialisationMoves']:
    output += f'MinionMoveID.{MoveToGameName(item[0],item[1])},'
  output += ');\n'

  #skill trees
  count = 0
  for item in [init_dict['SkillTree1'],init_dict['SkillTree2'],init_dict['SkillTree3']]:
    output += f'\t_loc2_ = Singleton.staticData.m_baseTalentTreesList.{item}();\n\t_loc1_.SetTalentTree({count},_loc2_);\n'
    count += 1
  output += "}"

  return output


#skill tree creation
#print(AutoSkillTree(init_skill_tree))


#Minion creation test
print("INTO 'All<inionsContainer.as': ")
print(AutoMinionCreator(init_minion)+"\n")

print("NOTE: The following extra modifications will be needed:")
print("* The skill tree (if not added already)")
print("* The DexID (added into MinionDexID.as)")
print("* Declarative stuff for the image (SpriteHandler, unique script for it, actual image, SymbolClass modification)")


