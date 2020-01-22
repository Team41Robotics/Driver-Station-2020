#ifndef getData_H
#define getData_H
#include <Arduino.h>

extern void getData();
extern void dumpBuffer(byte*, int);
extern void sendData();
extern byte calcChecksum(byte*, int, int);

#endif
