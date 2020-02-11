void setup() {
    pinMode(2, INPUT_PULLUP);
}

void loop() {
    Serial.println(digitalRead(2));
}