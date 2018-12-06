const int analogInPin = A0;  // Analog input pin that the pressure sensor is connected to
const int buttonPin =D5;
int calibVal= 0;
void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  
  pinMode(buttonPin, INPUT);
}

int sensorValue = 0;
void loop() {
  // read the analog in value:
  if (digitalRead(buttonPin)== HIGH)
    calibVal = avgCalib(100);
  sensorValue = analogRead(analogInPin)-calibVal;
  Serial.println(sensorValue);
 
  delay(2);
}

int avgCalib(int n){
  int result = 0;
  Serial.println("Calibrating");
  for(int i = 0; i< n;i++){
    result += analogRead(analogInPin);
    delay(2);
  }
  return result/n; 
}
