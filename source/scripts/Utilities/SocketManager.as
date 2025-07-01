package Utilities
{
   import flash.events.Event;
   import flash.events.EventDispatcher;
   import flash.events.IOErrorEvent;
   import flash.events.ProgressEvent;
   import flash.net.Socket;
   
   public class SocketManager extends EventDispatcher
   {
      
      private static var instance:SocketManager;
      
      private var socket:Socket;

      public static var isEnabled:Boolean; //used to track if we are meant to be active, and thus can be used to terminate connections
      
      public function SocketManager()
      {
         super();
         if(instance)
         {
            throw new Error("Singleton... use getInstance()");
         }
         instance = this;
         initializeSocket();
      }
      
      public static function getInstance() : SocketManager
      {
         if(!instance) //if we are not already having an instance -> this should be created regardless
         {
            instance = new SocketManager();
         }
         return instance; //this doesn't change, because in theory the getInstance() is only called if MULTI is on. Basically, don't mention it if needed
      }
      
      private function initializeSocket() : void
      {
         socket = new Socket();
         socket.addEventListener(Event.CONNECT,onSocketConnect);
         socket.addEventListener(IOErrorEvent.IO_ERROR,onSocketError);
         socket.addEventListener(Event.CLOSE,onSocketClose);
         socket.addEventListener(ProgressEvent.SOCKET_DATA,onSocketData);
         socket.connect("localhost",12345);
      }
      
      private function onSocketConnect(event:Event) : void
      {
         trace("Socket connected.");
      }
      
      private function onSocketError(event:IOErrorEvent) : void
      {
         trace("Socket error: " + event.text);
      }
      
      private function onSocketClose(event:Event) : void
      {
         trace("Socket closed.");
      }
      
      private function onSocketData(event:ProgressEvent) : void
      {
         var data:String = socket.readUTFBytes(socket.bytesAvailable);
         trace("Received data: " + data);
         dispatchEvent(new DataEvent(DataEvent.DATA_RECEIVED,data));
      }
      
      public function sendData(data:String) : void
      {
         if(socket.connected&&isEnabled) //if we are connected and we are meant to be
         {
            trace("Sending data: " + data);
            socket.writeUTFBytes(data);
            socket.flush();
         }
         else if(socket.connected&&!isEnabled) //if we are online and we are not meant to be
         {
            socket.close() //close the connection
         }
         else
         {
            trace("Socket is not connected.");
         }
      }
   }
}

