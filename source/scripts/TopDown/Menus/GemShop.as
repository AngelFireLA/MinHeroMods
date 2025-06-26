package TopDown.Menus
{
   import SharedObjects.BaseInterfacePieces.TCButton;
   import SharedObjects.Gems.GemVisuals;
   import SharedObjects.Gems.OwnedGem;
   import States.GemSelectorState;
   import States.TopDownStates;
   import Utilities.Singleton;
   import flash.display.Sprite;
   import flash.events.MouseEvent;
   import flash.text.TextField;
   import flash.text.TextFieldAutoSize;
   import flash.text.TextFormat;
   import flash.text.TextFormatAlign;
   
   public class GemShop extends TopDown.Menus.BaseLargeGemMenu
   {
      
      private var m_sellButton:TCButton;
      
      private var m_sellButtonsText:TextField;
      
      private var m_buyButton:TCButton;
      
      private var m_buyButtonsText:TextField;
      
      private var m_refreshButton:TCButton;
      
      private var m_refreshButtonText:TextField;
      
      protected var m_gemSelectButtons:Vector.<TCButton>;
      
      protected var m_gemVisuals:Vector.<GemVisuals>;
      
      protected var m_gems:Vector.<OwnedGem>;
      
      protected var m_isGemPurchased:Vector.<Boolean>;
      
      private var m_selectedGemPosition:int;
      
      private var m_selectedIcon:Sprite;
      
      public function GemShop()
      {
         super();
      }
      
      override public function LoadSprites() : void
      {
         var _loc1_:TextFormat = null;
         super.LoadSprites();
         _loc1_ = new TextFormat();
         _loc1_.color = 15790320;
         _loc1_.size = 16;
         _loc1_.font = "BurbinCasual";
         _loc1_.align = TextFormatAlign.CENTER;
         this.m_sellButton = new TCButton(this.SellButtonPressed,"menus_gemCombiner_buySellButton");
         this.m_sellButton.x = 553;
         this.m_sellButton.y = 224;
         m_background.addChild(this.m_sellButton);
         this.m_sellButtonsText = new TextField();
         this.m_sellButtonsText.embedFonts = true;
         this.m_sellButtonsText.defaultTextFormat = _loc1_;
         this.m_sellButtonsText.wordWrap = true;
         this.m_sellButtonsText.autoSize = TextFieldAutoSize.CENTER;
         this.m_sellButtonsText.text = "Sell ($999)";
         this.m_sellButtonsText.x = -19;
         this.m_sellButtonsText.y = 6;
         this.m_sellButtonsText.width = 150;
         this.m_sellButtonsText.selectable = false;
         this.m_sellButton.addChild(this.m_sellButtonsText);
         this.m_buyButton = new TCButton(this.BuyButtonPressed,"menus_gemCombiner_buySellButton");
         this.m_buyButton.x = 553;
         this.m_buyButton.y = 396;
         m_background.addChild(this.m_buyButton);
         this.m_buyButtonsText = new TextField();
         this.m_buyButtonsText.embedFonts = true;
         this.m_buyButtonsText.defaultTextFormat = _loc1_;
         this.m_buyButtonsText.wordWrap = true;
         this.m_buyButtonsText.autoSize = TextFieldAutoSize.CENTER;
         this.m_buyButtonsText.text = "Buy ($999)";
         this.m_buyButtonsText.x = -19;
         this.m_buyButtonsText.y = 6;
         this.m_buyButtonsText.width = 150;
         this.m_buyButtonsText.selectable = false;
         this.m_buyButton.addChild(this.m_buyButtonsText);
         this.m_refreshButton = new TCButton(this.RefreshButtonPressed,"menus_gemCombiner_buySellButton");
         this.m_refreshButton.x = 343;
         this.m_refreshButton.y = 396;
         m_background.addChild(this.m_refreshButton);
         this.m_refreshButtonText = new TextField();
         this.m_refreshButtonText.embedFonts = true;
         this.m_refreshButtonText.defaultTextFormat = _loc1_;
         this.m_refreshButtonText.wordWrap = true;
         this.m_refreshButtonText.autoSize = TextFieldAutoSize.CENTER;
         this.m_refreshButtonText.text = "Refresh";
         this.m_refreshButtonText.x = -19;
         this.m_refreshButtonText.y = 6;
         this.m_refreshButtonText.width = 150;
         this.m_refreshButtonText.selectable = false;
         this.m_refreshButton.addChild(this.m_refreshButtonText);
         this.m_gemSelectButtons = new Vector.<TCButton>(6);
         this.m_gemVisuals = new Vector.<GemVisuals>(6);
         this.m_selectedIcon = Singleton.utility.m_spriteHandler.CreateSprite("menus_gemMenuGemSelected");
         m_background.addChild(this.m_selectedIcon);
         var _loc2_:Array = new Array(this.GemButton1Pressed,this.GemButton2Pressed,this.GemButton3Pressed,this.GemButton4Pressed,this.GemButton5Pressed,this.GemButton6Pressed);
         var _loc4_:int = 0;
         while(_loc4_ < this.m_gemSelectButtons.length)
         {
            this.m_gemSelectButtons[_loc4_] = new TCButton(_loc2_[_loc4_],"menus_emptyGemSocket");
            this.m_gemSelectButtons[_loc4_].x = 334 + _loc4_ * 50;
            this.m_gemSelectButtons[_loc4_].y = 308;
            this.m_gemSelectButtons[_loc4_].visible = false;
            this.m_gemSelectButtons[_loc4_].ActivateTooltip();
            m_background.addChild(this.m_gemSelectButtons[_loc4_]);
            _loc4_++;
         }
         _loc4_ = 0;
         while(_loc4_ < this.m_gemSelectButtons.length)
         {
            this.m_gemVisuals[_loc4_] = new GemVisuals();
            this.m_gemVisuals[_loc4_].x = this.m_gemSelectButtons[_loc4_].x;
            this.m_gemVisuals[_loc4_].y = this.m_gemSelectButtons[_loc4_].y;
            m_background.addChild(this.m_gemVisuals[_loc4_]);
            _loc4_++;
         }
      }
      
      public function CreateNewGems() : void
      {
         var _loc2_:OwnedGem = null;
         this.m_gems = new Vector.<OwnedGem>(6);
         this.m_isGemPurchased = new Vector.<Boolean>(6);
         var _loc1_:int = Singleton.staticData.GetGemTierForShop();
         var _loc3_:int = 0;
         while(_loc3_ < this.m_gems.length)
         {
            _loc2_ = new OwnedGem();
            var _tier:int = _loc1_;
            if(_loc3_ >= 2 && _loc3_ < 4)
            {
               _tier = _loc1_ + 1;
            }
            else if(_loc3_ == 4)
            {
               _tier = _loc1_ + 2;
            }
            else if(_loc3_ == 5)
            {
               _tier = _loc1_ + 3;
            }
            if(Math.random() * 100 < 30)
            {
               if(_loc3_ == 1)
               {
                  _loc2_.CreateGemWithTier(_tier,int(Math.random() * 5));
               }
               else
               {
                  _loc2_.CreateGemWithTier(_tier,int(Math.random() * 5));
               }
            }
            else if(_loc3_ == 1)
            {
               _loc2_.CreateRandomGemWithTier(_tier);
            }
            else
            {
               _loc2_.CreateRandomGemWithTier(_tier);
            }
            this.m_gems[_loc3_] = _loc2_;
            this.m_gemVisuals[_loc3_].SetGem(this.m_gems[_loc3_]);
            this.m_gemSelectButtons[_loc3_].SetNewPopupSprite(this.m_gems[_loc3_].GetTooltip());
            _loc3_++;
         }
         _loc3_ = 0;
         while(_loc3_ < this.m_isGemPurchased.length)
         {
            this.m_isGemPurchased[_loc3_] = false;
            _loc3_++;
         }
      }
      
      override protected function UpdateAllTheInterfacePieces() : void
      {
         m_playersMoneyText.text = "$" + Singleton.dynamicData.m_currMoney;
         if(m_gemSelector.m_state != GemSelectorState.GSS_GEM_SELECTED)
         {
            this.m_sellButtonsText.text = "Sell";
            this.m_sellButton.alpha = 0.3;
         }
         else
         {
            this.m_sellButtonsText.text = "Sell ($" + Singleton.staticData.GetGemSellAmount(m_gemSelector.m_selectedGem.m_tier) + ")";
            this.m_sellButton.alpha = 1;
         }
         var _loc1_:int = 0;
         while(_loc1_ < this.m_gemSelectButtons.length)
         {
            if(this.m_isGemPurchased[_loc1_])
            {
               this.m_gemVisuals[_loc1_].visible = false;
            }
            else
            {
               this.m_gemVisuals[_loc1_].visible = true;
            }
            _loc1_++;
         }
         if(this.m_selectedGemPosition == -99)
         {
            this.m_buyButtonsText.text = "Buy";
            this.m_buyButton.alpha = 0.3;
            this.m_selectedIcon.visible = false;
         }
         else
         {
            this.m_buyButtonsText.text = "Buy ($" + Singleton.staticData.GetGemBuyAmount(this.m_gems[this.m_selectedGemPosition].m_tier) + ")";
            if(Singleton.staticData.GetGemBuyAmount(this.m_gems[this.m_selectedGemPosition].m_tier) <= Singleton.dynamicData.m_currMoney)
            {
               this.m_buyButton.alpha = 1;
            }
            else
            {
               this.m_buyButton.alpha = 0.3;
            }
            this.m_selectedIcon.visible = true;
         }
      }
      
      override public function BringIn() : void
      {
         this.m_selectedGemPosition = -99;
         super.BringIn();
         m_gemSelector.m_onGemPressedFunction = this.UpdateAllTheInterfacePieces;
         Singleton.utility.m_screenControllers.m_topDownScreen.m_currState = TopDownStates.IN_GEM_STORE;
      }
      
      override public function Update() : void
      {
         super.Update();
         if(this.m_sellButton.alpha == 1)
         {
            this.m_sellButton.m_isActive = true;
         }
         if(this.m_buyButton.alpha == 1)
         {
            this.m_buyButton.m_isActive = true;
         }
         if(this.m_refreshButton.alpha == 1)
         {
            this.m_refreshButton.m_isActive = true;
         }
         var _loc1_:int = 0;
         while(_loc1_ < this.m_gemSelectButtons.length)
         {
            if(!this.m_isGemPurchased[_loc1_])
            {
               this.m_gemSelectButtons[_loc1_].m_isActive = true;
            }
            _loc1_++;
         }
      }
      
      public function BuyButtonPressed(param1:MouseEvent) : void
      {
         Singleton.utility.m_soundController.PlaySound("menu_buyingItem",0.6);
         Singleton.dynamicData.m_currMoney -= Singleton.staticData.GetGemBuyAmount(this.m_gems[this.m_selectedGemPosition].m_tier);
         this.m_isGemPurchased[this.m_selectedGemPosition] = true;
         Singleton.dynamicData.AddToOwnedGemsFromPage(this.m_gems[this.m_selectedGemPosition],m_gemSelector.m_currPageOfGems);
         var currentPage:int = m_gemSelector.m_currPageOfGems;
         this.m_selectedGemPosition = -99;
         m_gemSelector.BringIn();
         m_gemSelector.m_currPageOfGems = currentPage;
         m_gemSelector.UpdateGems_Snap();
         this.UpdateAllTheInterfacePieces();
         trace("gem was bought");
      }
      
      public function SellButtonPressed(param1:MouseEvent) : void
      {
         Singleton.utility.m_soundController.PlaySound("tower_moneyPickup");
         Singleton.dynamicData.m_currMoney += Singleton.staticData.GetGemSellAmount(m_gemSelector.m_selectedGem.m_tier);
         var _loc2_:int = int(Singleton.dynamicData.GetGemPosition(m_gemSelector.m_selectedGem));
         Singleton.dynamicData.SetGemAt(null,_loc2_);
         m_gemSelector.BringIn();
         this.UpdateAllTheInterfacePieces();
      }
      
      public function RefreshButtonPressed(param1:MouseEvent) : void
      {
         trace("refreshed gems");
         Singleton.utility.m_soundController.PlaySound("menu_buyingItem",0.6);
         CreateNewGems();
         m_gemSelector.UpdateGems_Snap();
         this.UpdateAllTheInterfacePieces();
      }
      
      private function GemButtonHasBeenPressed(param1:int) : void
      {
         this.m_selectedGemPosition = param1;
         this.m_selectedIcon.x = this.m_gemSelectButtons[param1].x - 10;
         this.m_selectedIcon.y = this.m_gemSelectButtons[param1].y - 11;
         this.UpdateAllTheInterfacePieces();
      }
      
      private function GemButton1Pressed(param1:MouseEvent) : void
      {
         trace("selected gem 1");
         this.GemButtonHasBeenPressed(0);
      }
      
      private function GemButton2Pressed(param1:MouseEvent) : void
      {
         trace("selected gem 2");
         this.GemButtonHasBeenPressed(1);
      }
      
      private function GemButton3Pressed(param1:MouseEvent) : void
      {
         trace("selected gem 3");
         this.GemButtonHasBeenPressed(2);
      }
      
      private function GemButton4Pressed(param1:MouseEvent) : void
      {
         trace("selected gem 4");
         this.GemButtonHasBeenPressed(3);
      }
      
      private function GemButton5Pressed(param1:MouseEvent) : void
      {
         trace("selected gem 5");
         this.GemButtonHasBeenPressed(4);
      }
      
      private function GemButton6Pressed(param1:MouseEvent) : void
      {
         trace("selected gem 6");
         this.GemButtonHasBeenPressed(5);
      }
   }
}

