#include "VARS.h"

byte receiveBuffer[RECEIVE_BUFFER_SIZE];
byte parsedData[DATA_BUFFER_SIZE];

int receiveIndex = 0;
int receiverState = RCV_HUNT;
int buttonPorts[NUM_BUTTONS] = {2, 3, 4, 7, 8, 9};
int buttonRedPorts[NUM_BUTTONS] = {22, 23, 24, 27, 28, 29};
int buttonGreenPorts[NUM_BUTTONS] = {32, 33, 34, 37, 38, 39};
int buttonBluePorts[NUM_BUTTONS] = {42, 43, 44, 47, 48, 49};

bool buttonStates[NUM_BUTTONS];
bool isReceiving = false;
//byte recBytes[50];
