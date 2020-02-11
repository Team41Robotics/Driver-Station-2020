// pinMode(PIN, (OUTPUT, INPUT));
// digitalWrite(PIN, HIGH/LOW);
// delay(ms);
// R: 22, 23, 24, 27, 28, 29
// G: 32, 33, 34, 37, 38, 39
// B: 42, 43, 44, 47, 48, 49

int red[6] = {22, 23, 24, 27, 28, 29};
int green[6] = {32, 33, 34, 37, 38, 39};
int blue[6] = {42, 43, 44, 47, 48, 49};


void setupButtons() {
  // put your setup code here, to run once:
   for (int i; i < 6; i++) {
    pinMode(red[i], OUTPUT);
    pinMode(green[i], OUTPUT);
    pinMode(blue[i], OUTPUT);
   }
}

void makeColors() {
  // put your main code here, to run repeatedly:
 setColor(LOW, HIGH, HIGH);
 delay(1000);
 setColor(HIGH, LOW, HIGH);
 delay(1000);
 setColor(HIGH, LOW, LOW);
 delay(1000);
 setColor(LOW, LOW, HIGH);
 delay(1000);
 setColor(HIGH, HIGH, HIGH);
 delay(1000);
 setColor(LOW, HIGH, LOW);
 delay(1000);
 setColor(LOW, LOW, LOW);
 delay(1000);
 setColor(HIGH, HIGH, LOW);
 delay(1000);
}

void setColor(bool redVal, bool greenVal, bool blueVal){
  for (int i; i < 6; i++) {
    digitalWrite(red[i], redVal);
    digitalWrite(green[i], greenVal);
    digitalWrite(blue[i], blueVal);
  }
}
