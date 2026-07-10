#Now you're able to automate the tedial process of adding images and scripts to the SWF, by emulating keyboard and mouse input.

"""
First, install the necessary libraries:
  pip install keyboard mouse pyperclip
Then, change the "DIR" variable to the directory of images you want to add. The images must be PNG files, and their name (without the .png) will be used as the name of the image and script.
Open FFDec is windowed mode, but fullscreen, and make sure that all folders are collapsed, and the search bar is not there.
  Search for the "SymbolClass (2)" file, and expand the "symbols" section. Find the largest UID, and set that to the "count" variable +1. This is to avoid conflicts in naming stuff (SUPA IMPORTANT)
Prepare FFDec by collapsing all folders.
Then, run the script. It'll auto-add the images and image script into the SWF.
  As it takes control of your keyboard and mouse, do not use your computer whilst it's running.
Once it's done, you'll be able to tell by a lack of motion of the mouse.
  It takes about 16 seconds per image, so calculate the rough time if you want. 
Locate the "SpriteHandlerAdditions.txt" file to get the code to add to SpriteHandler.as for the new images.
  This is essential if you want to use the images in-game.
"""

#IMPORTS
import keyboard #kb
import pyperclip #copying file
import mouse    #maus
import time #slow down
import os

#FUNCTIONS
def pause():
  """Just your standard time.sleep, but using the global BREAK_TIME variable for more concise typing"""
  time.sleep(BREAK_TIME) 

def clicky(x,y,mouseCode="left"):
  """Click at x,y. Use mouseCode parameter to change click type (i.e "right")"""
  mouse.move(x,y) #go to position
  pause() #give some time for interfaces to update
  #print("Clicking at ",x,y)
  mouse.click(mouseCode)
  pause()

def AddAClass(filename:str): #untested, should still work
  """Uses direct kbm control to add a class from a file"""
  print("Loading file..")  #1st stage: load file
  with open(os.path.join(DIR,filename),"r") as file:
    data = file.read()
  #2nd stage: create file in FFDec
  #there are lots of delays to make sure it actually clicks there on time
  #2.1: Naming
  clicky(51,231) #select scripts folder
  clicky(51,231,mouse.RIGHT) #open context menu
  clicky(105,378)  #select "create new class"
  name = filename.removesuffix(".as").replace("/",".")
  keyboard.write(+name) #adds the class name as needed: playerio.subfolder.name or playerio.name
  pause()
  clicky(917,552) # Select "Create New DoABC Tag" (yes this will get out of hand)
  clicky(914,579) #Confirm creation
  #2.2: Placing the DoABC tag
  clicky(459,253) #select frame 1
  clicky(569,382) #place above early entry, or last entry
  clicky(920,798) #confirm
  time.sleep(4) #wait for creation (I timed this)
  #2.3: Content
  clicky(1085,969)   #Enable editing
  pause()
  keyboard.send("ctrl+a")
  pause()
  keyboard.send("delete")
  pause()
  pyperclip.copy(data) #copy the data to clipboard
  pause()
  keyboard.send("ctrl+v") #paste
  #pyperclip.copy("") #reset clipboard
  pause()
  clicky(1248,972)  #Save
  time.sleep(2.5) #give time to save
  #2.4: Reset
  clicky(101,414) #select sidebar
  pause()
  for i in range(8):  #move to top pane -> test if "Home" works
    keyboard.send("page up")
    pause()

def AddAnImage(img_path,count): #WORKS
  """Adds a specified image to the SWF, using the filename as the name of the image. Also adds the necessary script for it, and then updates the SpriteHandler.as script"""
  name = img_path.removesuffix(".png") #all images are PNG
  fullName = f"Utilities.SpriteHandler_{name}" 

  #creating the data for the image script. Note the lack of indentation, this is because JPEXS auto-indents it when writing instead of pasting.
  data = 'package Utilities\n{\n   import mx.core.BitmapAsset;\n   \n   [Embed(source="/_assets/'
  data += f"{count}_{fullName}.png" # add image name
  data += '")]\n   public class '
  data += f"{fullName.removeprefix('Utilities.')}" #add class name
  data += ' extends BitmapAsset\n   {\n      \n      public function '
  data += f"{fullName.removeprefix('Utilities.')}" #add class name... again
  data += '()\n      {\n         super();\n      }\n   }\n}\n'  
  
  #1st stage: get to dialogue window
  clicky(64,199) #select "Images"
  clicky(13,199) #"expand"
  #clicky(152,655) # select random image
  keyboard.press_and_release("end") #move to bottom
  pause() #cooldown
  clicky(152,655,"right") #click to open context menu
  clicky(270,914) #open menu to add image
  clicky(598,913) #slide across to keep menu open
  clicky(591,863) #create tag
  clicky(1361,983) #click "Replace" -> already in target folder
  clicky(761,676) #click address bar
  #clicky(1047,461) #go to top bar
  keyboard.write(img_path) #write image name with PNG
  clicky(1192,745) #open image
  ##now, image is successfully added, time to update the symbolClass
  clicky(11,757) #expand "Scripts"
  clicky(121,758) #select "SymbolClass"
  clicky(827,196) #expand SymbolClass
  keyboard.press_and_release("end") #move to bottom
  pause() #cooldown
  clicky(1359,976) #enable editing
  clicky(1031,795,"right") #open context menu
  clicky(1074,893) #add new tag at end
  clicky(966,956) #select first text box
  keyboard.send("ctrl+a") #select all
  pause()
  keyboard.write(str(count)) # type ID
  pause()
  clicky(1197,956) #select second text box
  keyboard.write(fullName) # type name
  clicky(1315,976) #save

  ## now, create the image script

  clicky(206, 543) #select window
  keyboard.press_and_release("end") #move to bottom

  clicky(63, 759, mouse.RIGHT) #open context menu
  clicky(158, 925) #select Add Class
  clicky(809,488) #select class name box
  keyboard.write(fullName) #type file name
  pause()
  clicky(918, 575) #confirm
  clicky(1204, 512) #maximise tag menu
  clicky(944, 553) #select SpriteHandler tag
  clicky(929, 536) #confirm
  clicky(1113, 968) #edit actionscript
  pause()
  keyboard.send("ctrl+a")
  pause()
  keyboard.send("delete")
  pause()
  pyperclip.copy(data) #copy the data to clipboard
  pause()
  keyboard.send("ctrl+v") #paste
  #pyperclip.copy("") #reset clipboard
  pause()
  clicky(1324, 971) #save
  clicky(453, 619) #go back to main window
  keyboard.press_and_release("home") #press "Home"
  clicky(13,199) #minimise images
  clicky(11,285) #collapse other
  clicky(12,304) #collapse scripts

#get the directory
global DIR,BREAK_TIME
BREAK_TIME = 0.4 #number of seconds to pause each time. A smaller number will make it faster, but may cause misclicks if the computer is slow.
DIR = "" #change to the directory of files, their name being the thing to be written as
print(f"Working in : {DIR}")

all_files = os.listdir(DIR)
print(f"Found {len(all_files)} files to add")

print("Prepare yourselves!")
time.sleep(3) #time to alt tab

#READY TO RUN (play honks whilst it works, it takes a while xD)
#MAKE sure that all folders are collapsed, and the search bar is not there.
count = -100 #starting ID for SymbolClass. Check within FFDec before starting
new = ""
if count == -100: #idiot-proofing this
  print("Change it you idiot")
else:
  for item in all_files: 
    if ".png" in item:
      print(f"Adding image {item}")
      curr_str = f"      private static var {item}:Class = SpriteHandler_{item};"
      new += curr_str+"\n"
      AddAnImage(item,count)
      count += 1  
  print("All done!")
  with open("SpriteHandlerAdditions.txt", "w") as file: file.write(new) #writing the SpriteHandler extra thing to add.

