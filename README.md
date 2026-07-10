All the mods for Min Hero: Tower of Sages are to be compiled here, in a single file with customizeable options.


## USAGE:
* Download the "default.swf" from here
* Run with FlashPlayer (download from here or use your own: version must be 14+)
* Done!
This is forwards-compatiable, or you can use your old save with this one! Check "Save Compatiability" section.
This is **NOT backwards-compatible**, so if you create a save that contains Zanyu, it cannot be used in the normal game. This is because if the game detects a modded minion without the right tools, it breaks the game. Check "Cleaning a Modded Save" in guides.md.


### Save Compatiability
Ready to upgrade? Here's how to, but first a few checks:
* Is your save from one of the "older" mod files I released?
  * You can check this by loading the game. If it shows "v1.03" in the corner, or something that isn't "v1.01", or contains "MOD", then it goes here.
  * if it is, see "Cleaning Old Modded Save" in guides.md
* Is your save from a completely vanilla game!
  * It can be used **as normal** in this SWF file!
  * To enable mods in it, see the section "Adding Mods to Save Manually" in guides.md

### MOD TOGGLES
You can only toggle mods at the beginning of a save.
Due to the method that I have constructed the mod toggles, you can toggle the minion corresponding to a "species" toggle all of them. Make sure to double-check if the minions are actually there! You can do this by immediately opening the Minionpedia, and seeing how many extra minions beyond 101 there are. This should correspond to the number of minions you added. For example, adding Zanyu, and Stingaray, would mean 3 extra minions, so if you don't see a number 104, then you've not actually toggled them!

## CURRENT VERSION:
The latest *committed* version, the default.swf that you find here, and not in releases. Content made in a release is detailed in its release notes
### Content:

#### MINIONS
* Zanyu
* Stingaray/Mantaray
* Arkvian/Arkclaw
* Adophan/Ophan/Ophance

#### OTHER
* BetterGems
* Deleted SoGood intro (for the greater good)

## TODO:

Core (things that are present across all versions)
* Fix the spelling mistakes in the code. It's so easy to do, we might as well
 
Multi (things just for the multiplayer as that's going to enter here RAAH)
* Check BattleSystem for socket entry point
* How to make a TrainerDataObject work with OwnedMinion list? (might be a new class)
