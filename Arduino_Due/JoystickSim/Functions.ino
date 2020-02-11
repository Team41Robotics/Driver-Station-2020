#include "VARS.h"
#include "Functions.h"
#include "Joystick.h"

void setupButtons() {
    for (int i = 0; i < NUM_BUTTONS; i++) {
        pinMode(buttonPorts[i], INPUT_PULLUP);
		pinMode(buttonRedPorts[i], OUTPUT);
		pinMode(buttonGreenPorts[i], OUTPUT);
		pinMode(buttonBluePorts[i], OUTPUT);
	}
}

void setColors(bool redVal, bool greenVal, bool blueVal) {
  for (int i = 0; i < NUM_BUTTONS; i++) {
    digitalWrite(buttonRedPorts[i], redVal);
    digitalWrite(buttonGreenPorts[i], greenVal);
    digitalWrite(buttonBluePorts[i], blueVal);
  }
}

void readButtons() {
	bool currentState;
	for (int i = 0; i < NUM_BUTTONS; i++) {
		currentState = digitalRead(buttonPorts[i]);
		buttonStates[i] = currentState;
	}
}

void sendJoyStates() {
	Joystick.clearState();
	//SerialUSB.println((parsedData[5] << 8) + parsedData[4]);
	Joystick.state.xRot.axis = (parsedData[1] << 8) + parsedData[0];
	Joystick.state.yRot.axis = (parsedData[3] << 8) + parsedData[2];
	Joystick.state.x.axis = (parsedData[5] << 8) + parsedData[4];
	Joystick.state.y.axis = (parsedData[7] << 8) + parsedData[6];	
	Joystick.state.buttons.b00 = !buttonStates[0];
	Joystick.state.buttons.b01 = !buttonStates[1];
	Joystick.state.buttons.b02 = !buttonStates[2];
	Joystick.state.buttons.b03 = !buttonStates[3];
	Joystick.state.buttons.b04 = !buttonStates[4];
	Joystick.state.buttons.b05 = !buttonStates[5];

	Joystick.state.buttons.b06 = parsedData[8];
	Joystick.state.buttons.b07 = parsedData[9];
	Joystick.state.buttons.b08 = parsedData[10];
	Joystick.state.buttons.b09 = parsedData[11];
	Joystick.state.buttons.b10 = parsedData[12];
	Joystick.state.buttons.b11 = parsedData[13];
	Joystick.state.buttons.b12 = parsedData[14];
	Joystick.state.buttons.b13 = parsedData[15];
	Joystick.state.buttons.b14 = parsedData[16];
	Joystick.sendState();
}

void prettyColors() {
	setColors(LOW, HIGH, HIGH);
	delay(1000);
	setColors(HIGH, LOW, HIGH);
	delay(1000);
	setColors(HIGH, LOW, LOW);
	delay(1000);
	setColors(LOW, LOW, HIGH);
	delay(1000);
	setColors(HIGH, HIGH, HIGH);
	delay(1000);
	setColors(LOW, HIGH, LOW);
	delay(1000);
	setColors(LOW, LOW, LOW);
	delay(1000);
	setColors(HIGH, HIGH, LOW);
	delay(1000);
}



int receiveBytes() {
	//if (Serial2.available()) SerialUSB.println("Receiving bytes:" + (int)Serial2.available());
	while (Serial2.available()) {
		byte recValue = Serial2.read();
		//if (recValue < 0) return 0;
		byte recByte = recValue;

		// This is a receiver state machine
		// States: 	hunt: looking for packet start
		//			sync: we are syncronized and receiving
		//			escape: we have found an escape character and are immediately
		//				entering the next byte without looking again
		switch (receiverState) {
			case RCV_HUNT:
#ifdef DEBUG
				SerialUSB.println("In RCV_HUNT");
#endif
				if (recByte == 0x55) receiverState = RCV_SYNC;
				receiveIndex = 0;
				break;



			case RCV_SYNC:
#ifdef DEBUG
				SerialUSB.println(  "In RCV_SYNC");
#endif
				if (recByte == 0xAA) {
					receiverState = RCV_HUNT;
					int returnVal = receiveIndex;
					receiveIndex = 0;
					return returnVal;
				} else if (recByte == 0x55) {
					receiveIndex = 0;
					receiverState = RCV_HUNT;
					return  UNEXPECTED_SOP;
				} else if (recByte == 0xFF) {
					receiverState = RCV_ESCAPE;
					receiveBuffer[receiveIndex++] = recByte;
					if (receiveIndex >= RECEIVE_BUFFER_SIZE) {
						SerialUSB.println(receiveIndex);
						receiverState = RCV_HUNT;
						receiveIndex = 0;
						return BUFFER_OVERFLOW;
					}
				} else {
					receiveBuffer[receiveIndex++] = recByte;
					if (receiveIndex >= RECEIVE_BUFFER_SIZE) {
						SerialUSB.println(receiveIndex);
						receiverState = RCV_HUNT;
						receiveIndex = 0;
						return BUFFER_OVERFLOW;
					}
				}
				break;



			case RCV_ESCAPE:
#ifdef DEBUG
				SerialUSB.println("In RCV_ESCAPE");
#endif
				receiveBuffer[receiveIndex++] = recByte;
				if (receiveIndex >= RECEIVE_BUFFER_SIZE) {
						receiverState = RCV_HUNT;
						receiveIndex = 0;
						return BUFFER_OVERFLOW;
				}	
				receiverState = RCV_SYNC;
				break;

			default:
				// Should never happen
				SerialUSB.print("FATAL ERROR OCCURRED: STATE IS ");
				SerialUSB.println(receiverState);
				break;
		}
	}


	
	return 0;
}


void parseBytes(int len) {
	//SerialUSB.print("Parsing bytes, dial #1 is: ");
	int dataIndex = 0;
	for (int i = 0; i < len; i++) {
		if (receiveBuffer[i] < 0x10) SerialUSB.print("0");
		SerialUSB.print(receiveBuffer[i], HEX);
		if (receiveBuffer[i] == 0xFF && (receiveBuffer[i+1] == 0xFF || receiveBuffer[i+1] == 0xAA || receiveBuffer[i+1] == 0x55)) {
			parsedData[dataIndex] = receiveBuffer[++i];
		} else {
			parsedData[dataIndex] = receiveBuffer[i];
		}
		dataIndex++;
	}
	for (int i = 0; i < len; i++) {
		//SerialUSB.print(parsedData[i]);
	}
	SerialUSB.println();
}
