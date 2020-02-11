#ifndef VARS_H
#define VARS_H

#define NUM_BUTTONS 10
#define NUM_SLIDERS 2                   // On analog pins A0-A1
#define NUM_DIALS 2                     // On analog pins A2 and A5
#define NUM_SWITCHES 9                  // On pins 2-13 (the momentary switche s are each 2 inputs0
#define DATA_BUFFER_SIZE (2*NUM_SLIDERS) + (2*NUM_DIALS) + NUM_SWITCHES
// Worst case scenario, everything has an escape character, 2 bytes for start and end, \
    two more for checksum, and 16 as extra headroom
#define RECEIVE_BUFFER_SIZE 2*DATA_BUFFER_SIZE + 2 + 2 + 16

// Receiver states
#define RCV_HUNT 0
#define RCV_SYNC 1
#define RCV_ESCAPE 2
// Receiver error codes
#define UNEXPECTED_SOP -1
#define BUFFER_OVERFLOW -2

//#define DEBUG 1


extern byte receiveBuffer[];
extern byte parsedData[];

extern int receiverState;
extern int receiveIndex;
extern int buttonPorts[];
extern int buttonRedPorts[];
extern int buttonGreenPorts[];
extern int buttonBluePorts[];

extern bool buttonStates[];
extern bool isReceiving;
//extern byte recBytes[];

#endif
