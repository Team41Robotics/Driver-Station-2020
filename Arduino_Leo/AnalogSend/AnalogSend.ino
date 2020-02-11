/*
    Order of operations: Dials, Sliders, Switches
*/


#include "PINS.h"
#include "getData.h"


// Set pins for all switches as inputs\
   and start serial comm. w/ Due
void setup () {
    for (int i = 0; i < NUM_SWITCHES; i++) {
        pinMode(switchPins[i], INPUT);
    }
    Serial.begin(9600);
    Serial1.begin(9600);
} 


// Get the values of all devices, print it\
   to the screen and wait a quarter of a sec
void loop() {
    getData();
    //dumpBuffer(dataBuffer, DATA_BUFFER_SIZE);
    sendData();
    //Serial.println("THIS IS THE LEO");
    delay(25);
}