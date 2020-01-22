#include <Arduino.h>
#include "PINS.h"
#include "getData.h"

void getData() {
    // Dials are on pins 2 and 5 so I'm just going to read them manually :(
    // Doing the same thing as with the sliders (see above)
    for (int i = 0; i < NUM_DIALS; i++) {
        int dialRead = analogRead(dialPins[i]);
        dataBuffer[i*2] = (byte)(dialRead & 0xff);         // First byte
        dataBuffer[(i*2) + 1] = (byte)(dialRead & 0x0300 >> 8);   // Last byte
    }


    // Read all of the sliders
    for (int i = 0; i <= NUM_SLIDERS; i++) {
        // Create a var for caching the read value
        int readVar = analogRead(sliderPins[i]);
        // To read the bytes, we need to take the first part in one byte, then add to the checksum
        dataBuffer[2*(NUM_DIALS+i)] = (byte)(readVar & 0xff);
        //checksum[0] ^= sliders[i*2];
        // Then take the rest of it and put it in the next byte
        dataBuffer[2*(NUM_DIALS+i)+1] = (byte)(readVar & 0x0300 >> 8); // Take the 10 bit value and remove the first 8 bits by shifting them left (out of existence)
        //checksum[1] ^= sliders[((i*2) + 1)];
    }

    // Read all of the switches
    for (int i = 0; i < NUM_SWITCHES; i++) {
       dataBuffer[2*NUM_SLIDERS + 2*NUM_DIALS + i] = (byte)digitalRead(switchPins[i]);
    }
}

void dumpBuffer(byte* buffer, int len) {
    for (int i = 0; i < len; i++) {
        Serial.print(buffer[i], HEX);
        Serial.print(" ");
        if (i == 2*NUM_SLIDERS + 2*NUM_DIALS) {
            Serial.print("| ");
        }
    }
    Serial.println("");
}