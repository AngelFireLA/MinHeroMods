
# Hi there!

This is a compilation of the guides that you can read through to accomplish certain cool things!
Not all have been made yet, but gotta get a few down!

  
  

## Formatting "old" mod save file
So you want to clean your old save from mods? See "METHOD 1"
Or were using one of the "older" save files, and want to "upgrade"? See "METHOD 2". **only pick this method if you have owned modded minions and wish to save them**.


### METHOD 1
Firstly, make sure you unequip any Gems on your existing modded minions: **they will be deleted**. Then, release every single modded minion you have. It's much easier to do it in-game than through the save file editor.

Now, to remove the technical parts
* Open [.minerva](https://mariani.life/projects/minerva/) on a web browser.
* Select "Open" and then "Choose File". Navigate to your save file.
* Now we have the file open, it's time to select all the modded stuff and delete them
* Type in the search box `m_minionsseen`. For each one that has a number greater than 101 after it, right-click and select "Delete"
* Repeat this with `m_minionsowned` instead of `m_minionsseen`
* Done! Click "Save" and you now have a save file reset to vanilla! Test this by copying your newly-purged save into a vanilla save folder, and testing to load it!

Untested, but please do contact square_nine for any issues!

### METHOD 2

* Open [.minerva](https://mariani.life/projects/minerva/) on a web browser.
* Select "Open" and then "Choose File". Navigate to your save file.
* Now we have the file open, it's time to select all the modded stuff and reformat them into the "new" format, starting with the obsolete stuff.
* Type in the search box `m_minionsseen`. For each one that has a number greater than 101 after it, right-click and select "Delete"
* Repeat this with `m_minionsowned` instead of `m_minionsseen`
* Now time to save your modded minions!
* Repeat the below for numbers 102-109:
	* Search for the number (i.e `102` in the search box):
	* Then, look through all the results. If there is a result that contains "DexID", click on it. If the number that appears in the "Integer" window matches the number you are looking for, you've found the minion! Record the number down for now, and the number you found it at (102-109)
* Now, repeat for each minion number you found:
	* Search for `minion` + the number you noted down
	* Right click on the `minion`+ your number+`dexID` and select "Delete"
	* Then right click on the `TCrpgSaveSlot` row at the top of the results, and select "Create"
	* Set the "Key" value to `minion`+your number + `ModName`, and the "Value" to the "codename" of that minion. Use the handy table below:
		* 102 -> "waterRay1" 
		103 -> "waterRay2"
		104 -> "holyEye1"	
		105 -> "holyEye2"	
		106 -> "holyEye3"	
		107 -> "holyBirb1"
		108 -> "holyBirb2"
		109 -> "dirtFish"	
* For each one of these codenames you use:
	* Right click on the `TCrpgSaveSlot` row at the top of the results, and select "Create"
	* Set the "Key" value to `m_isMod_` + the codename, and the value to `true`

Now, I hope it was easy to follow, but _theoretically_ when you copy this to the modded save folder, it should work as if nothing changed! Not tested, but please let square_nine know if it does!
  

## Adding Mods to Save Manually

So you want to add mods into an already-created save file? Sure you can! This will only work for "vanilla" save files from the base game. See the guide to formatting your save file if it's from the old mod

* Open [.minerva](https://mariani.life/projects/minerva/) on a web browser.
* Select "Open" and then "Choose File". Navigate to your save file.
* Now we have the file open, it's time to add our mod toggles
* Right click on the `TCrpgSaveSlot` row at the top of the results, and select "Create"
* Set the "Key" value to `m_isMod_` + the codename, and the value to `true`. Get the codename from the table below. 
	* You may need to repeat this whole process from Step 4 for multiple variants (specified as numbers after the codename). Just add the number to the end, and repeat for each case
	* Zanyu -> "dirtFish"
	* Ophan -> "holyEye" 1/2/3
	* Arkvian -> "holyBirb" 1/2
	* Stingaray -> "waterRay" 1/2
* 	Now, click "Save", and you have the formatted file! _Theoretically_ you can copy over to the modded save folder and it'll work!
Let square_nine know if this works, or if it doesn't