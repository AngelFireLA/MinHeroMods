package TopDown.Menus.MiniMap
{
   public class MiniMapDataObject
   {
      
      public var m_xPosition:int;
      
      public var m_yPosition:int;
      
      public var m_spriteName:String;
      
      public var m_roomID:int;
      
      public var m_groupID:int;
      
      public var m_isEggery:Boolean;
      
      public var m_overrideScale:Number;
      
      public function MiniMapDataObject(param1:String, param2:int, param3:int, param4:int, param5:int = 0, param6:Boolean = false, param7:Number = -99)
      {
         super();
         this.m_xPosition = param2;
         this.m_yPosition = param3;
         this.m_spriteName = param1;
         this.m_roomID = param4;
         this.m_groupID = param5;
         this.m_isEggery = param6;
         this.m_overrideScale = param7;
      }
   }
}

