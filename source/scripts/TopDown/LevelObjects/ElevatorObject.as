package TopDown.LevelObjects
{
   import States.GameState;
   import States.SpecialRoom;
   import Utilities.Singleton;
   
   public class ElevatorObject extends WallCollObject
   {

      public var m_ElevatorType:String = "vanilla";
      
      public function ElevatorObject(param1:String = "vanilla")
      {
         super();
         this.m_ElevatorType = param1;
      }
      
      override public function OnColl() : void
      {
         super.OnColl();
         Singleton.dynamicData.m_FloorType = this.m_ElevatorType; //set the floor type to the elevator type
         trace("Setting floor type to: " + Singleton.dynamicData.m_FloorType);
         Singleton.dynamicData.m_currTransitionID = SpecialRoom.TOWER_FLOOR_SELECT;
         Singleton.utility.m_screenControllers.SetSceneTo(GameState.LEVEL_SELECT_SCREEN);
      }
   }
}

