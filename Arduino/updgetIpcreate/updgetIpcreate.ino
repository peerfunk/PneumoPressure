//#include <WiFiClient.h>

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string.h>

char* ssid = "";
char* pass = "";
char* own_ssid = "IOT";
char* own_password = "12345678";
int status = WL_IDLE_STATUS;
WiFiClient espClient;
WiFiUDP Udp;

unsigned int localPort = 8081;
const int analogInPin = A0;  // Analog input pin that the pressure sensor is connected to
const int buttonPin =D6; //Button pin
int sensorValue = 0;
int calibVal = 0;
int frequency = 10; //hz
IPAddress ip ;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  connect();
  pinMode(buttonPin, INPUT);
  calibVal = avgCalib(5000);
  Udp.begin(localPort);
  getIP();
}

void loop() {
  if (digitalRead(buttonPin)== HIGH)
    calibVal = avgCalib(100);
  sensorValue = 512+(analogRead(analogInPin)-calibVal);
  
  Serial.println(sensorValue);
  char buffer[6];
  String ret = itoa(sensorValue,buffer,10);
  sendUDP(String("m") + ret );
  delay(1000/frequency);
}

void getIP(){
  while (String(ip) == "0"){
    int packetSize = Udp.parsePacket();
      if (packetSize) {
           Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
           if(String(packetBuffer) == "c"){
            ip = Udp.remoteIP();
            Serial.print("Found Server at: ");
            Serial.println(ip);
            Udp.begin(localPort);
            String ret = "cd";
            sendUDP(ret);
            delay(5000);
           }
      }
      
  }
}


void sendUDP(String &content){
  Udp.beginPacket(ip,localPort);
  Udp.write(content.c_str());
  Udp.endPacket();
    
}
void connect() {
  while (!Serial) {
    ; // wait for serial port to connect. Needed USB support
 }
  //connect to Wifi network:
  Serial.print("Configuring access point...");
  WiFi.softAP(own_ssid, own_password);
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  Serial.println("Connected to wifi");
  printWifiStatus();

}

int avgCalib(int n){
  int result = 0;
  Serial.println("Calibrating");
  for(int i = 0; i< n;i++){
    result += analogRead(analogInPin);
    delay(2);
  }
  Serial.println("calibrated to ");
  return result/n; 
}
void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}



