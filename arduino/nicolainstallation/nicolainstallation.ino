#include <Servo.h>

#include <Wire.h> 

#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

Adafruit_7segment matrix = Adafruit_7segment();
Servo servoRotate; 
Servo servoRelease;

int inByte = 0;         // incoming serial byte
boolean continueRead = false;

int one = 0;
int two = 0;
int three = 0;
int four = 0;

int total  = 0;

int counter  = 0;

unsigned long startRotate;
boolean rotateCylinder = false;

void setup() {

  Serial.begin(9600);
  Serial.println("7 Segment Backpack Test");

  matrix.begin(0x70);
  
  servoRotate.attach(3);
  servoRelease.attach(5);
  
  servoRotate.write(95); //Rotate medium on the right   
  servoRelease.write(80); //Reset angle
  
  updateLCD(counter);
  
  startRotate = millis();
  
}

void loop() {
  
  if (Serial.available() > 0) {
      continueRead = false;
      while(inByte = Serial.read()) {
           if (inByte == 13 || inByte == -1) break;
           if (inByte == 'U') {
               continueRead = true;
               total = 0;
           }
           
           if (!continueRead)  { //flush input
               Serial.flush();
           } else {
             if (inByte != 'U') { //Cast into 4 vars
                 if (total == 0) one = inByte;
                 else if (total == 1) two = inByte;
                 else if (total == 2) three = inByte;
                 else if (total == 3) four = inByte;
                 total++;
             }
           }
           delay(10);
      }
      if (total > 0) {
          castNumber();
          updateLCD(counter);
          if (counter > 0)  //release only when is more than zero
              releaseMarble();
          total = 0;
          Serial.println(counter);
      }
      
  }
  if (rotateCylinder) { //Rotate the cyclinder
        if (millis() - startRotate > 5000) { //Exit after 5 seconds
            rotateCylinder = false;
            servoRotate.write(95);
        }  else {
            servoRotate.write(170);
        }
        
  }
// releaseMarble();
  delay(100);
}


void castNumber() {
  char converter[]={one,two,three,four};
  counter = atoi(converter);
  one = 0;
  two = 0;
  three = 0;
  four = 0;   
}

void releaseMarble() {
  servoRelease.write(170); //Open 
  delay(1000);
  servoRelease.write(80); //Close
  delay(2000);
  servoRelease.write(170); //Open 
  delay(1000);
  startRotate = millis();
  rotateCylinder = true;
}


void updateLCD(int number) {
  matrix.drawColon(false); //Dont print dots
  
  matrix.print(number, DEC);
  matrix.writeDisplay();
}


