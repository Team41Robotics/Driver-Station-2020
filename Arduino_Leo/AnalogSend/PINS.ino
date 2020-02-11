#include "PINS.h"

int dialPins[NUM_DIALS] = {2, 5};
int sliderPins[NUM_SLIDERS] = {0, 1};
int switchPins[NUM_SWITCHES] = {2, 3, 6, 7, 4, 5, 10, 12, 13};
int transBuffSize = DATA_BUFFER_SIZE + 4; // All data and a start and end code and checksum

byte checksum[2];
byte dataBuffer[DATA_BUFFER_SIZE];