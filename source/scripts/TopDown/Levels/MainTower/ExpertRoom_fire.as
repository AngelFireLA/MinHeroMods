package TopDown.Levels.MainTower
{
   import TopDown.LevelObjects.BaseInGameInteractionObject;
   import TopDown.LevelObjects.ButtonZone;
   import TopDown.LevelObjects.RoomTransitionEntryPointObject;
   import TopDown.LevelObjects.RoomTransitionObject;
   import TopDown.LevelObjects.ChatBox.StandardChatBox;
   import TopDown.LevelObjects.VisualLevelObject;
   import TopDown.Levels.BaseTopDownLevel;
   import States.SpecialRoom;
   import Utilities.Singleton;
   
   public class ExpertRoom_fire extends BaseTopDownLevel
   {

      private var m_secretSageVisual:VisualLevelObject;

      private var m_secretRickVisual:VisualLevelObject;

      private var m_hasQuestionedVisitor:Boolean = false;
      
      public function ExpertRoom_fire()
      {
         super();
      }

      override public function LoadSprites() : void
      {
         super.LoadSprites();
         if(Singleton.dynamicData.m_currTransitionID == SpecialRoom.SECRET_SAGE_ROOM)
         {
            this.m_hasQuestionedVisitor = false;
            this.ShowSecretSage();
         }
      }
      
      override public function CreateObjects() : void
      {
         var _loc3_:ButtonZone = null;
         if(Singleton.dynamicData.m_currTransitionID == SpecialRoom.SECRET_SAGE_ROOM)
         {
            this.CreateSecretSageRoom();
            return;
         }
         m_roomBounds.graphics.beginFill(0);
         m_roomBounds.graphics.drawRect(0,0,695.3,826.55);
         m_roomBounds.graphics.endFill();
         Singleton.utility.m_screenControllers.m_topDownScreen.m_topDownMovementScreen.m_bottomVisualLayer.addChild(m_roomBounds);
         AddObject("generalRoom_floorTile",53,546.5,1,1,0);
         AddObject("generalRoom_floorTile",173,546.5,1,1,0);
         AddObject("generalRoom_floorTile",293,546.5,1,1,0);
         AddObject("generalRoom_floorTile",413,546.5,1,1,0);
         AddObject("generalRoom_floorTile",533,546.5,1,1,0);
         AddObject("generalRoom_floorTile",73,426.5,1,1,0);
         AddObject("generalRoom_floorTile",193,426.5,1,1,0);
         AddObject("generalRoom_floorTile",313,426.5,1,1,0);
         AddObject("generalRoom_floorTile",433,426.5,1,1,0);
         AddObject("generalRoom_floorTile",553,426.5,0.7868804931640625,1,0);
         AddObject("generalRoom_floorTile",57,306.5,1,1,0);
         AddObject("generalRoom_floorTile",177,306.5,1,1,0);
         AddObject("generalRoom_floorTile",297,306.5,1,1,0);
         AddObject("generalRoom_floorTile",417,306.5,1,1,0);
         AddObject("generalRoom_floorTile",537,306.5,1,1,0);
         AddObject("generalRoom_floorTile",77,186.5,1,1,0);
         AddObject("generalRoom_floorTile",197,186.5,1,1,0);
         AddObject("generalRoom_upperLeftCorner",5.55,0,1,1,0);
         AddObject("generalRoom_floorTile",317,186.5,1,1,0);
         AddObject("generalRoom_topWall",136.5,-0.05,1,1,0);
         AddObject("generalRoom_floorTile",437,186.5,1,1,0);
         AddObject("generalRoom_floorTile",557,186.5,0.7704925537109375,1,0);
         AddObject("generalRoom_sideWall",611.5,229,1,0.6888427734375,0);
         AddObject("generalRoom_upperRightCorner",567.5,0.5,1,1,0);
         AddObject("generalRoom_lowerRightCorner",568,508,1,1,0);
         AddObject("generalRoom_bottomWall",133,605.2,1.021575927734375,1,0);
         AddObject("generalRoom_lowerLeftCorner",4.7,507.65,1,1,0);
         AddObject("generalRoom_sideWall",92.55,229.2,-1,0.6888427734375,0);
         AddObject("generalRoom_bottomWall",339,605.2,1.138671875,1,0);
         AddObject("generalRoom_topWall",337,-0.05,1.1484222412109375,1,0);
         AddObject("generalRoom_sideWall",611.5,366,1,0.7140655517578125,0);
         AddObject("generalRoom_sideWall",92.55,366.2,-1,0.7140655517578125,0);
         AddObject("generalRoom_floorRunnerTop",258,308,1,1,0);
         AddObject("generalRoom_floorRunnerTop",460,497,1,1,180);
         AddObject("generalRoom_floorRunner_rotationConnect",259,400,1,1,0);
         AddObject("generalRoom_genericTapestry_fire",431.5,40,1,1,0);
         AddObject("generalRoom_candelabra",537,43.5,1,1,0);
         AddObject("generalRoom_detailTapestry_fire",288,41,1,1,0);
         AddObject("generalRoom_statuePedestal",443.5,220.5,1,1,0);
         AddObject("generalRoom_genericTapestry_fire",143.5,40,1,1,0);
         AddObject("generalRoom_candelabra",76,43.5,1,1,0);
         AddObject("generalRoom_statuePedestal",183.5,220.5,1,1,0);
         AddObject("generalRoom_expertStatue",185.5,184,1,1,0);
         AddObject("generalRoom_expertStatue",445.5,184,1,1,0);
         AddObject("room_teleporterOff",288.5,499,1,1,0);
         AddObject("room_expertTeleporter_glow",293,367,1,1,0);
         AddObject("generalRoom_sideTorch",611,253,1,1,0);
         AddObject("generalRoom_sideTorch",611,423,1,1,0);
         AddObject("generalRoom_sideTorch",93,424,-1,1,0);
         AddObject("generalRoom_sideTorch",93,254,-1,1,0);
         AddObject("generalRoom_bottomTorch",493,590.5,1,1,0);
         AddObject("generalRoom_bottomTorch",133,590.5,1,1,0);
         AddObject("generalRoom_expertEnemy",308,187,1,1,0);
         AddObject("collRect",72,169,5.5099945068359375,0.3600006103515625,0);
         AddObject("collRect",567,185,0.3204193115234375,0.55999755859375,0);
         AddObject("collRect",107,185,0.3204193115234375,0.55999755859375,0);
         AddObject("collRect",613,180,0.32000732421875,8.671630859375,0);
         AddObject("collRect",59,180,0.32000732421875,8.8153076171875,0);
         AddObject("collRect",82,605,5.5099945068359375,0.55999755859375,0);
         AddObject("collRect",449,269,0.8000030517578125,0.720001220703125,0);
         AddObject("collRect",189,269,0.8000030517578125,0.720001220703125,0);
         _loc3_ = AddObject("buttonZoneObject",280.05,186,1.5694580078125,1.809295654296875,0) as ButtonZone;
         _loc3_.m_buttonZoneID = 0;
         AddObject("collRect",328,269.5,0.6199951171875,0.2599945068359375,0);
         AddObject("expert_entryObject",341,425,1,1,0);
         AddObject("expert_roomTransitionObject",345,517,0.477447509765625,0.477447509765625,0);
         AddObject("menus_speechBubble",232,117.5,1,1,0);
         AddObject("fire_music_override",87,763.5,1,1,0);
      }

      private function CreateSecretSageRoom() : void
      {
         var _loc1_:int = 0;
         var _loc2_:ButtonZone = null;
         m_roomBounds.graphics.beginFill(0);
         m_roomBounds.graphics.drawRect(0,0,695,700);
         m_roomBounds.graphics.endFill();
         Singleton.utility.m_screenControllers.m_topDownScreen.m_topDownMovementScreen.m_bottomVisualLayer.addChild(m_roomBounds);
         _loc1_ = 0;
         while(_loc1_ < 5)
         {
            AddObject("generalRoom_floorTile",53 + _loc1_ * 120,186.5,1,1,0);
            AddObject("generalRoom_floorTile",53 + _loc1_ * 120,306.5,1,1,0);
            AddObject("generalRoom_floorTile",53 + _loc1_ * 120,426.5,1,1,0);
            AddObject("generalRoom_floorTile",53 + _loc1_ * 120,546.5,1,1,0);
            _loc1_++;
         }
         AddObject("generalRoom_upperLeftCorner",5.5,0,1,1,0);
         AddObject("generalRoom_topWall",136.5,0,1,1,0);
         AddObject("generalRoom_topWall",337,0,1.15,1,0);
         AddObject("generalRoom_upperRightCorner",567.5,0,1,1,0);
         AddObject("generalRoom_sideWall",92.5,229,-1,1.38,0);
         AddObject("generalRoom_sideWall",611.5,229,1,1.38,0);
         AddObject("generalRoom_lowerLeftCorner",5,507.5,1,1,0);
         AddObject("generalRoom_bottomWall",133,605,1.02,1,0);
         AddObject("generalRoom_bottomWall",339,605,1.14,1,0);
         AddObject("generalRoom_lowerRightCorner",568,507.5,1,1,0);
         AddObject("generalRoom_bottomDoor",279,596,1,1,0);
         AddObject("generalRoom_detailTapestry_fire",288,41,1,1,0);
         AddObject("generalRoom_candelabra",76,43.5,1,1,0);
         AddObject("generalRoom_candelabra",537,43.5,1,1,0);
         AddJustVisualObject("generalRoom_grandWizard",296,220,1,1,0);
         this.m_secretSageVisual = m_visualObjects[m_visualObjects.length - 1];
         AddJustVisualObject("generalRoom_hardEnemy",304,222,1,1,0);
         this.m_secretRickVisual = m_visualObjects[m_visualObjects.length - 1];
         _loc2_ = AddObject("buttonZoneObject",280,218,1.57,1.81,0) as ButtonZone;
         _loc2_.m_buttonZoneID = 7;
         AddObject("collRect",315,301,0.62,0.3,0);
         AddObject("collRect",59,180,0.32,8.8,0);
         AddObject("collRect",613,180,0.32,8.8,0);
         AddObject("collRect",72,169,5.51,0.36,0);
         AddObject("collRect",82,605,2.35,0.56,0);
         AddObject("collRect",438,605,1.55,0.56,0);
         AddObject("entryObject_secretSageRoom",341,525,1,1,0);
         AddObject("roomTransitionObject104",345,590,0.48,0.48,0);
         AddObject("menus_speechBubble7",232,150,1,1,0);
         AddObject("fire_music_override",87,650,1,1,0);
         this.ShowSecretSage();
      }

      override protected function PreformButtonAction(param1:int) : void
      {
         var _loc1_:StandardChatBox = null;
         if(Singleton.dynamicData.m_currTransitionID != SpecialRoom.SECRET_SAGE_ROOM || param1 != 7)
         {
            super.PreformButtonAction(param1);
            return;
         }
         _loc1_ = GetChatBoxForButtonZone(7);
         _loc1_.SetFunctions();
         if(!this.m_hasQuestionedVisitor)
         {
            this.m_hasQuestionedVisitor = true;
            _loc1_.BringInWithText("How did you get in here? That door was never supposed to open.","Grand Sage");
         }
         else
         {
            this.m_secretSageVisual.m_currSprite.visible = false;
            this.m_secretRickVisual.m_currSprite.visible = true;
            _loc1_.BringInWithText("Never gonna give you up... You have been Rickrolled!","Rick Astley");
         }
      }

      private function ShowSecretSage() : void
      {
         if(this.m_secretSageVisual != null && this.m_secretSageVisual.m_currSprite != null)
         {
            this.m_secretSageVisual.m_currSprite.visible = true;
            this.m_secretRickVisual.m_currSprite.visible = false;
         }
      }
   }
}

