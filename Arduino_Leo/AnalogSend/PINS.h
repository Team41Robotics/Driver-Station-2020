#include <Arduino.h>

#ifndef PINS_H
#define PINS_H

#define NUM_SLIDERS 2                   // On analog pins A0-A1
#define NUM_DIALS 2                     // On analog pins A2 and A5
#define NUM_SWITCHES 9                  // On pins 2-13 (the momentary switches are each 2 inputs0
#define DATA_BUFFER_SIZE (2*NUM_SLIDERS) + (2*NUM_DIALS) + NUM_SWITCHES


extern int dialPins[];
extern int sliderPins[];
extern int switchPins[];
extern int transBuffSize;

extern byte checksum[];
extern byte dataBuffer[];
//extern byte transBuffer[];

#endif
