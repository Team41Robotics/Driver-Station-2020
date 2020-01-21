/*
    Checksum order: Sliders, Dials, Switches
*/


#include "PINS.h"
#include "getData.h"

byte checksum[2];                          // A math equation that is done on both sides of the serial connection to make sure the data is not corrupted




void setup () {
    // Set pins for all switches as inputs
    for (int i = 2; i <= 13; i++) {
        pinMode(i, INPUT_PULLUP);
    }
    // Start serial comm. w/ Due
    Serial.begin(9600);
}



void loop() {
    getData();
    dumpBuffer(dataBuffer, DATA_BUFFER_SIZE);
    delay(1000);
}