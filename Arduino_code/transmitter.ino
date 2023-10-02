#include <SoftwareSerial.h>
#include "TinyGPS++.h"
#include <RH_ASK.h>
#include <SPI.h>

TinyGPSPlus gps;

// The serial connection to the GPS module
SoftwareSerial ss(4, 3);

// Create Amplitude Shift Keying Object
RH_ASK rf_driver;

String incomingByte;  

void setup(){
  Serial.begin(9600);
  ss.begin(9600);
  // Initialize ASK Object
  rf_driver.init();
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop(){

  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println(F("No GPS detected: check wiring."));
    while(true);
  }

  if (Serial.available() > 0) {
  incomingByte = Serial.readStringUntil('\n');
  
    if (incomingByte == "on") {
      digitalWrite(LED_BUILTIN, HIGH);
      // This sketch displays information every time a new sentence is correctly encoded.
      while (ss.available() > 0)
      if (gps.encode(ss.read()))
        displayInfo();
      Serial.write("Led on");
    }

    else if (incomingByte == "off") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.write("Led off");
    }

    else{
     Serial.write("invald input");
    }
  }

}

void displayInfo()
{
  Serial.write("Location: "); 
  if (gps.location.isValid())
  {
    const char *msg = "Hello World";
    rf_driver.send((uint8_t *)msg, strlen(msg));
    rf_driver.waitPacketSent();
    delay(1000);
  }
  else
  {
    Serial.write("INVALID");
  }

}