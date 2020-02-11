#include <Arduino.h>
#include "PINS.h"
#include "getData.h"


void getData() {
    // Read data from all the dials
    //  Mask the high byte and cache the low byte
    //  Mask the low byte, shift the bits, and cahce the high byte
    for (int i = 0; i < NUM_DIALS; i++) {
        int dialRead = analogRead(dialPins[i]);
        dataBuffer[i*2] = (byte)(dialRead);         // Low byte
        dataBuffer[(i*2) + 1] = (byte)(dialRead >> 8);   // High byte

        checksum[0] ^= dataBuffer[2*i];
        checksum[1] ^= dataBuffer[(2*i)+1];
    }


    // Read all of the sliders
    // Doing the same thing as with the dials (see above)
    for (int i = 0; i < NUM_SLIDERS; i++) {
        int readVar = analogRead(sliderPins[i]);
        dataBuffer[2*(NUM_DIALS+i)] = (byte)(readVar);
        checksum[0] ^= dataBuffer[2*(NUM_DIALS+i)];
        dataBuffer[2*(NUM_DIALS+i)+1] = (byte)(readVar >> 8); 
        checksum[1] ^= dataBuffer[2*(NUM_DIALS+i)+1];
    }

    // Read all of the switches
    for (int i = 0; i < NUM_SWITCHES; i++) {
       dataBuffer[2*NUM_SLIDERS + 2*NUM_DIALS + i] = digitalRead(switchPins[i]);
       checksum[0] ^= dataBuffer[2*NUM_SLIDERS + 2*NUM_DIALS + i];
    }
}



// Print out everyhing in the buffer array
// Should be in the order that they appear on the board
// Put a "|" between the potentiometers and switches
void dumpBuffer(byte* buffer, int len) {
    for (int i = 0; i < DATA_BUFFER_SIZE; i++) {
        Serial.print(dataBuffer[i], HEX);
        Serial.print(" ");
        if (i == (2*NUM_SLIDERS + 2*NUM_DIALS)-1) {
            Serial.print("| ");
        }
    }
    //Serial.print(checksum[0], HEX);
    //Serial.print(checksum[1], HEX);
    Serial.println();
}


byte calcChecksum(byte vals[], int numVals, int byteNum) {
    for (int i = 0; i < numVals; i++) {
        checksum[byteNum] ^= vals[i];
    }
    return checksum[byteNum];
}


int calcTransBuffSize() {
    transBuffSize = DATA_BUFFER_SIZE + 4;
    for (int i = 0; i < DATA_BUFFER_SIZE; i++) {
        if (dataBuffer[i] == 0x55 || dataBuffer[i] == 0xAA || dataBuffer[i] == 0xFF) {
            transBuffSize++;
        }
    }
    return transBuffSize;
}


void sendData() {
    //Serial.println("Sending Data");
    byte transBuffer[calcTransBuffSize()];

    transBuffer[0] = 0x55;
    transBuffer[transBuffSize-1] = 0xAA;

    int count = 0;
    for (int i = 1; i < transBuffSize-2; i++) {
        if (dataBuffer[count] == 0x55 || dataBuffer[count] == 0xAA || dataBuffer[count] == 0xFF) {
            transBuffer[i++] = 0xFF;
        }
        transBuffer[i] = dataBuffer[count];
        count++;
    }
    for (int i = 0; i < transBuffSize; i++) {
        Serial1.write(transBuffer[i]);
        if (transBuffer[i] < 0x10) Serial.print("0");
        Serial.print(transBuffer[i], HEX);
    }
    Serial.println();
}