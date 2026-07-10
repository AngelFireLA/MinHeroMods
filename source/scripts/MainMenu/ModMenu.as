package MainMenu
{
   import SharedObjects.BaseInterfacePieces.ToggleButton;
   import Utilities.Singleton;
   import flash.display.Sprite;
   import flash.text.TextField;
   import flash.text.TextFieldAutoSize;
   import flash.text.TextFormat;
   import flash.text.TextFormatAlign;
   import flash.utils.Dictionary;
   import SharedObjects.BaseInterfacePieces.TCButton;
   import flash.events.MouseEvent;
   import com.greensock.TweenLite;

   public class ModMenu extends Sprite
   {
      // --- layout constants ---
      private static const ITEM_STRIDE:int      = 38;   // row spacing
      private static const VISIBLE_COUNT:int    = 5;    // rows visible at once

      // mask position
      private static const MASK_X:int           = 5;
      private static const MASK_Y:int           = 55;

      // first row y relative to holder
      private static const FIRST_ROW_OFFSET:int = 11;

      // align row 0 top to mask top
      private static const LIST_TOP_Y:int       = MASK_Y - FIRST_ROW_OFFSET;

      private var m_background:Sprite;

      private var m_settingTexts:Vector.<TextField>;
      private var m_toggleButtons:Vector.<ToggleButton>;
      private var m_toggleTexts:Vector.<String>;
      private var m_toggleDict:Dictionary;

      private var m_modSelectHolder:Sprite; // scrolled content
      private var m_modSelectMask:Sprite;   // viewport

      private var m_upButton:TCButton;
      private var m_downButton:TCButton;

      private var m_scrollPosition:int = 0; // first-visible row
      private var m_scrollMax:int = 0;      // max first-visible row
      private var m_totalItems:int = 0;

      public function ModMenu()
      {
         super();
         this.m_toggleTexts = new Vector.<String>();
         this.m_toggleTexts.push("Zanyu","Stingaray","Arkvian","Ophan", "Ice Floor", "Nuzlocke", "No Regen"); //still need this for ordering. Make as small as possibe
         this.m_toggleDict = new Dictionary();
         this.m_toggleDict["Example"] = ["Tooltip description about the Example mod.", "Toggle1 (the minion)", "Extra toggles like this"];
         this.m_toggleDict["Zanyu"] = ["Bring the might of the legendary beast to your team! Featuring a custom Skill Tree, and powerful moves, they can be found in Floor 5-2!", "dirtFish"];
         this.m_toggleDict["Stingaray"] = ["A fearsome minion of the sea, ready to bring a Water-infused playstyle! Swim over to Stingaray in Floor 1-3, and 3-1!", "waterRay1", "waterRay2"];
         this.m_toggleDict["Arkvian"] = ["A holy counterpart to Airmony and Falcona, a serene bird prepared to become the next party member! Soar to Arkvian in Floor 1-4 and Arkclaw in Floor 4-2", "holyBirb1", "holyBirb2"];
         this.m_toggleDict["Ophan"] = ["Cultivate a curious one-eyed creature into a fast, lethal minion under your command! Find Ophan in 4-2 and Adophan in 5-3!", "HolyEye1", "HolyEye2", "HolyEye3"];
         this.m_toggleDict["Ice Floor"] = ["The Ice Floor is now available. Adventure through this chilly domain through the side entrance, and discover new minions, moves and Trainers!", "iMammoth1", "iMammoth2", "iMammoth3","iUnicorn1","iUnicorn2", "iUnicorn3", "iSloth1", "iSloth2", "iSloth3", "iSeal1", "iSeal2", "iSeal3", "iceFloor"] //toggles are all Ice Floor minion mods (used for DexID), and the general-purpose "iceFloor" toggle
         this.m_toggleDict["Nuzlocke"] = ["If your minion faints, it's gone for good!", "nuzlocke"];
         this.m_toggleDict["No Regen"] = ["Your Minions will not regenerate their health naturally except between floors.", "no_natural_regen"];
      }
      
      public function LoadSprites() : void
      {
         this.m_background = Singleton.utility.m_spriteHandler.CreateSprite("mainMenu_modMenuBackground");
         addChild(this.m_background);

         this.m_settingTexts  = new Vector.<TextField>(this.m_toggleTexts.length);
         this.m_toggleButtons = new Vector.<ToggleButton>(this.m_toggleTexts.length);

         var fmt:TextFormat = new TextFormat();
         fmt.color = 16448250;
         fmt.size = 16;
         fmt.font = "BurbinCasual";
         fmt.align = TextFormatAlign.LEFT;

         // --- scrolling window ---
         this.m_modSelectHolder = new Sprite();
         this.m_modSelectHolder.x = 10;
         this.m_modSelectHolder.y = LIST_TOP_Y; // exact alignment
         addChild(this.m_modSelectHolder);

         this.m_modSelectMask = new Sprite();
         this.m_modSelectMask.x = MASK_X;
         this.m_modSelectMask.y = MASK_Y;
         this.m_modSelectMask.graphics.beginFill(0x555555);
         this.m_modSelectMask.graphics.drawRect(0, 0, 200, VISIBLE_COUNT * ITEM_STRIDE);
         this.m_modSelectMask.graphics.endFill();
         addChild(this.m_modSelectMask);
         this.m_modSelectHolder.mask = this.m_modSelectMask;

         // rows
         var i:int = 0;
         while(i < this.m_settingTexts.length)
         {
            this.m_settingTexts[i] = new TextField();
            this.m_settingTexts[i].embedFonts = true;
            this.m_settingTexts[i].defaultTextFormat = fmt;
            this.m_settingTexts[i].wordWrap = true;
            this.m_settingTexts[i].autoSize = TextFieldAutoSize.LEFT;
            this.m_settingTexts[i].text = this.m_toggleTexts[i];
            this.m_settingTexts[i].width = 115;
            this.m_settingTexts[i].x = 5;
            this.m_settingTexts[i].y = FIRST_ROW_OFFSET + i * ITEM_STRIDE;
            this.m_settingTexts[i].selectable = false;
            this.m_modSelectHolder.addChild(this.m_settingTexts[i]);

            this.m_toggleButtons[i] = new ToggleButton(this.ToggleCarousel,"menus_settings_onButton","menus_settings_offButton","","",this.m_toggleTexts[i]);
            this.m_toggleButtons[i].x = 128;
            this.m_toggleButtons[i].y = FIRST_ROW_OFFSET + i * ITEM_STRIDE;
            this.m_modSelectHolder.addChild(this.m_toggleButtons[i]);
            i++;
         }

         // arrows
         this.m_upButton = new TCButton(this.UpPressed,"minionPedia_upArrow");
         this.m_upButton.x = 175;
         this.m_upButton.y = 10;
         addChild(this.m_upButton);

         this.m_downButton = new TCButton(this.DownPressed,"minionPedia_upArrow"); // reuse up arrow, flip
         this.m_downButton.x = 175;
         this.m_downButton.y = 280;
         this.m_downButton.scaleY = -1;
         addChild(this.m_downButton);

         // make arrows active (TCButton deactivates itself unless alwaysActive)
         this.m_upButton.m_alwaysActive = true;
         this.m_downButton.m_alwaysActive = true;

         // bounds & initial visibility/state
         m_totalItems = this.m_toggleTexts.length;
         m_scrollMax  = Math.max(0, m_totalItems - VISIBLE_COUNT);

         this.m_upButton.visible   = false;
         this.m_downButton.visible = (m_scrollMax > 0);

         // disable click when hidden
         this.m_upButton.m_isOn   = this.m_upButton.visible;
         this.m_downButton.m_isOn = this.m_downButton.visible;

         trace("[ModMenu] LoadSprites: total=" + m_totalItems + " scrollMax=" + m_scrollMax + " holderY=" + this.m_modSelectHolder.y + " maskY=" + this.m_modSelectMask.y);
         visible = false;
      }

      private function UpPressed(e:MouseEvent) : void
      {
         trace("[ModMenu] UpPressed: pos(before)=" + m_scrollPosition + " max=" + m_scrollMax);
         if (this.m_scrollPosition > 0)
         {
            --this.m_scrollPosition;
            this.UpdateTheScrollBoxPosition();
         }
      }

      private function DownPressed(e:MouseEvent) : void
      {
         trace("[ModMenu] DownPressed: pos(before)=" + m_scrollPosition + " max=" + m_scrollMax);
         if (this.m_scrollPosition < this.m_scrollMax)
         {
            ++this.m_scrollPosition;
            this.UpdateTheScrollBoxPosition();
         }
      }

      private function UpdateTheScrollBoxPosition() : void
      {
         if (this.m_scrollPosition < 0) this.m_scrollPosition = 0;
         if (this.m_scrollPosition > this.m_scrollMax) this.m_scrollPosition = this.m_scrollMax;

         var targetY:Number = LIST_TOP_Y - this.m_scrollPosition * ITEM_STRIDE;
         trace("[ModMenu] UpdateScroll: pos=" + m_scrollPosition + " targetY=" + targetY);

         TweenLite.to(this.m_modSelectHolder, 0.25, { "y": targetY });

         // arrows at edges + clickability
         this.m_upButton.visible   = (this.m_scrollPosition > 0);
         this.m_downButton.visible = (this.m_scrollPosition < this.m_scrollMax);
         this.m_upButton.m_isOn    = this.m_upButton.visible;
         this.m_downButton.m_isOn  = this.m_downButton.visible;
      }

      public function BringIn() : void
      {
         var i:int = 0;
         while(i < this.m_toggleButtons.length)
         {
            this.m_toggleButtons[i].m_isToggleOn = Singleton.dynamicData.m_isMod[Singleton.staticData.m_all_mods[i]];
            i++;
         }

         // recompute bounds (future-proof)
         m_totalItems = this.m_toggleTexts.length;
         m_scrollMax  = Math.max(0, m_totalItems - VISIBLE_COUNT);

         Singleton.utility.m_screenControllers.m_topDownScreen.m_topDownMenuScreen
            .ApplyMenuBringInAnimationJustFade(this);

         this.m_scrollPosition = 0;
         this.UpdateTheScrollBoxPosition();

         trace("[ModMenu] BringIn: total=" + m_totalItems + " scrollMax=" + m_scrollMax);
      }

      public function ToggleCarousel(param1:String) : void
      {
         for (var k:String in this.m_toggleDict)
         {
            if (param1 == k)
            {
               var i:int = 1; // skip description
               while (i < this.m_toggleDict[k].length)
               {
                  var toggleName:String = this.m_toggleDict[k][i];
                  Singleton.dynamicData.m_isMod[toggleName] = !Singleton.dynamicData.m_isMod[toggleName];
                  trace("[ModMenu] Toggled: " + toggleName + " -> " + Singleton.dynamicData.m_isMod[toggleName]);
                  i++;
               }
               break;
            }
         }
      }

      public function Update() : void
      {
         // ensure arrow buttons get processed by the global button manager
         if (this.m_upButton)   this.m_upButton.Update();
         if (this.m_downButton) this.m_downButton.Update();

         var i:int = this.m_scrollPosition;
         while(i < VISIBLE_COUNT+this.m_scrollPosition)
         {
            this.m_toggleButtons[i].Update();
            i++;
         }
      }
   }
}
