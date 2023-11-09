#include <SPI.h>
const int camLed = 3;

const int dir = 4;
const int pulse = 5;
const int hf = 6;
const int tim = 7;

//SS pins to LS7366R
const int slave_frame = 8; 
const int slave_lie = 9;
const int slave_loft = 10; 

const int right_limit = 14;
const int left_limit = 15;
const int lock_limit = 16;

const int pulseDuration = 500;
const int stepsPerRevolution = 1600;
const int stepSize = 72; //Motor moves [360/stepSize] degrees per step eg: @
const int rotationsPerFrameDeg;

float lie = 90;
float loft = 15;
float frame = 0;
float frameDefaultAngle = 30;

int ledValue = 120;

//Encoder Counter variables
int cntr;
int mdr0, mdr1;
int mdr0Setting = 0b00000011;
int mdr1Setting = 0b00000010;
float deg_per_count = 0.09; //0.087

//command character
int standby;
int command[5];
int *cmd;

void setup() {
  Serial.begin(9600);
  
  pinMode(left_limit, INPUT);
  pinMode(right_limit, INPUT);
  pinMode(lock_limit, INPUT);
  pinMode(camLed, OUTPUT);
  pinMode(tim, INPUT);
  pinMode(hf, OUTPUT);
  pinMode(pulse, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(slave_loft, OUTPUT); 
  pinMode(slave_lie, OUTPUT);
  pinMode(slave_frame, OUTPUT);

  analogWrite(camLed, ledValue);
  digitalWrite(hf, LOW);
  digitalWrite(pulse, LOW);
  digitalWrite(dir, LOW); 
  digitalWrite(slave_loft, HIGH);
  digitalWrite(slave_lie, HIGH);
  digitalWrite(slave_frame, HIGH);
  
  SPI.begin();

  //Encoder setup: 16 bit read mode, 4x quadrature count
  //Check LS7366R Datasheet for more info...
  writeToMDR0(slave_loft, mdr0Setting);
  writeToMDR1(slave_loft, mdr1Setting);
  writeToMDR0(slave_lie, mdr0Setting);
  writeToMDR1(slave_lie, mdr1Setting);
  writeToMDR0(slave_frame, mdr0Setting);
  writeToMDR1(slave_frame, mdr1Setting);
  
  resetCNTR(slave_loft);
  resetCNTR(slave_lie);
  resetCNTR(slave_frame);

//  if(leftIsOpen() == true){
//    Serial.print("Left: OPEN ");}
//  else{
//    Serial.print("Left: CLOSED ");}
//  if(rightIsOpen() == true){
//    Serial.print("Right: OPEN ");}
//  else{
//    Serial.print("Right: CLOSED ");}
//  if(lockIsOpen() == true){
//    Serial.print("Lock: OPEN ");}
//  else{
//    Serial.print("Lock: CLOSED ");}
//  Serial.print("\n");
}

void loop() {
  standby = 0;
  standby = standBy();
  if (standby == 1) {
    cmd = getCMD();}
  parseCMD(cmd[0], cmd[1], cmd[2], cmd[3], cmd[4]);
}

void resetCNTR(int slave){
  digitalWrite(slave, LOW);
  SPI.transfer(0x20);
  digitalWrite(slave, HIGH);
}

void writeToMDR0(int slave, int cmd){
  digitalWrite(slave, LOW);
  SPI.transfer(0x88);
  SPI.transfer(cmd);
  digitalWrite(slave, HIGH);
  delay(100);
}

void writeToMDR1(int slave, int cmd){
  digitalWrite(slave, LOW);
  SPI.transfer(0x90);
  SPI.transfer(cmd);
  digitalWrite(slave, HIGH);
  delay(100);
}

void printMDRvals(){
  int mdr0_lie, mdr0_loft, mdr0_frame;
  int mdr1_lie, mdr1_loft, mdr1_frame;
  digitalWrite(slave_lie, LOW);
  SPI.transfer(0x48);
  mdr0_lie = SPI.transfer(0x00);
  digitalWrite(slave_lie, HIGH);
  
  digitalWrite(slave_loft, LOW);
  SPI.transfer(0x48);
  mdr0_loft = SPI.transfer(0x00);
  digitalWrite(slave_loft, HIGH);

  digitalWrite(slave_frame, LOW);
  SPI.transfer(0x48);
  mdr0_frame = SPI.transfer(0x00);
  digitalWrite(slave_frame, HIGH);

  digitalWrite(slave_lie, LOW);
  SPI.transfer(0x50);
  mdr1_lie = SPI.transfer(0x00);
  digitalWrite(slave_lie, HIGH);

  digitalWrite(slave_loft, LOW);
  SPI.transfer(0x50);
  mdr1_loft = SPI.transfer(0x00);
  digitalWrite(slave_loft, HIGH);

  digitalWrite(slave_frame, LOW);
  SPI.transfer(0x50);
  mdr1_frame = SPI.transfer(0x00);
  digitalWrite(slave_frame, HIGH);
  
//  Serial.print(mdr0_lie);
//  Serial.print(", ");
//  Serial.print(mdr1_lie);
//  Serial.print(", ");
//  Serial.print(mdr0_loft);
//  Serial.print(", ");
//  Serial.print(mdr1_loft);
//  Serial.print(", ");
//  Serial.print(mdr0_frame);
//  Serial.print(", ");
//  Serial.print(mdr1_frame);
}

int readCNTR(int slave){
  unsigned int count1, count2;
  long result;
  digitalWrite(slave, LOW);
  SPI.transfer(0x60);
  count1 = SPI.transfer(0x00);
  count2 = SPI.transfer(0x00);
  digitalWrite(slave, HIGH);
  result = ((long)count1<<8) + ((long)count2); 
  return result;
}

float getLoft(){
  float loft;
  loft = readCNTR(slave_loft)*deg_per_count;
  return round2(loft);
}

float getLie(){
  float lie, raw;
  raw = readCNTR(slave_lie);
  lie = raw*deg_per_count;
  return round2(lie);
}

float getFrame(){
  float frame, raw;
  raw = readCNTR(slave_frame);
  frame = raw*deg_per_count;
  frame = round2(frame);
  return frame;
}

float round2(float val){
  //Round number to first decimal place
  val = val * 10;
  val = round(val);
  val = val * 0.1;
  return val;
}

int standBy() {
  int input;
  while (true) {
    input = Serial.read();
    if (input == 42) {
      return 1;
    }
  }
}

int * getCMD() {
  int input;
  int i = 0;
  unsigned long t1, t2;
  t1 = micros();
  while (true) {
    t2 = micros();
    if (t2 - t1 > 3000000) {
      for (int j=0; j<8; j++) {
        command[j] = 0;
      }
      return;
    }
    input = Serial.read();
    if (input != -1) {
      command[i] = input;
      i += 1;}
    if (i ==5) {
      return command;}
  }
}

float numArrayToFloat(int sign, int dig1, int dig2, int dig3) {
  float num = 0;
  num = num + (dig1-48);
  num = num * 10;
  num = num + (dig2-48);
  num = num + (dig3-48)*0.1;
  if (sign == 43) {
    return num;
  }
  if (sign == 45) {
    return num * -1;
  }
}

//Rotates stepper (stepsPerRevolution/stepSize)*360 degrees 
void stepCW(){
  if ((rightIsOpen() == true) and (lockIsOpen() == true)){
    digitalWrite(dir, HIGH);
    for (int i = 0; i<(stepsPerRevolution/stepSize); i++){
      digitalWrite(pulse, HIGH);
      delayMicroseconds(pulseDuration);
      digitalWrite(pulse, LOW);
      delayMicroseconds(pulseDuration);    
    }
  }
}

void stepCCW(){
  if ((leftIsOpen()==true) and (lockIsOpen() == true)){
    digitalWrite(dir, LOW);
    for (int i = 0; i<(stepsPerRevolution/stepSize); i++){
      digitalWrite(pulse, HIGH);
      delayMicroseconds(pulseDuration);
      digitalWrite(pulse, LOW);
      delayMicroseconds(pulseDuration);    
    }
  }
}

bool leftIsOpen(){
  int sensorLeft;
  sensorLeft = digitalRead(left_limit);
  if (sensorLeft == 0){
    return true;}
  else{
    return false;}
}

bool rightIsOpen(){
  int sensorRight;
  sensorRight = digitalRead(right_limit);
  if (sensorRight == 0){
    return true;}
  else{
    return false;}
}

bool lockIsOpen(){
  int sensorLock;
  sensorLock = digitalRead(lock_limit);
  if (sensorLock == 0){
    return true;}
  else{
    return false;}
}

int seekAngle(float target) {
  //Return Value Meaning:
  // 1: Successfully reached target value
  //-1: Triggered limit switch
  //-2: timed out probably stuck
  //-3: Frame lock engaged (at start)
  //-4: Frame lock engaged (mid operation)
  float startFrame = getFrame();
  float targetFrame = startFrame + target;
  unsigned long startTime, currentTime, diffTime;
  unsigned long timeLimit = 15000000;
  //startTime = micros();
  if (lockIsOpen() != true){return -3;}
  while (true) {
    float currentFrame = getFrame();
    float diff = targetFrame - currentFrame;
    if (diff < 0.1 && diff > -0.1){return 1; }
    else if (lockIsOpen()==false){return -4;}
    else if (diff > 0) {
      if (rightIsOpen()==false){return -1;}
      stepCW();}
    else if (diff < 0) {
      if (leftIsOpen()==false){return -1;}
      stepCCW();}
    //currentTime = micros();
    //diffTime = currentTime - startTime;
    //if (diffTime > timeLimit){
    //  return -2;}
    }
  }

int findCenter() {
  if (lockIsOpen() != true) {return -3;}
  while (rightIsOpen() != false) {
    stepCW();
  }
  float currentFrame = getFrame();
  float targetFrame = currentFrame - 19;
  unsigned long startTime, currentTime, diffTime;
  unsigned long timeLimit = 15000000;
  startTime = micros();

  while (getFrame() > targetFrame) {
    stepCCW();
    if (getFrame() <= targetFrame) {
      return 1;}}
    currentTime = micros();
    diffTime = currentTime - startTime;
    if (diffTime > timeLimit){return -2;}
}

void parseCMD(int cmd0, int cmd1, int cmd2, int cmd3, int cmd4) {
  float target = numArrayToFloat(cmd1, cmd2, cmd3, cmd4);
  int result = 0;
  switch(cmd0){
    case '1':
      loft = getLoft();
      Serial.println(loft);
      break;
      
    case '2':
      lie = getLie();
      Serial.println(lie);
      break;
      
    case '3':
      frame = getFrame();
      Serial.println(frame);
      break;

    case 's':
      result = seekAngle(target);
      Serial.println(result);
      break;
      
    case 'r':
      resetCNTR(slave_loft);
      resetCNTR(slave_lie);
      break;

    //Auto Hold Off
    case 'h':
      digitalWrite(hf, HIGH);
      break;
      
    //Auto Hold On
    case 'j':
      digitalWrite(hf, LOW);
      break;
      
    case 'f':
      resetCNTR(slave_frame);
      break;
      
    case '>': //Frame Up, Strong, Positive
      stepCW();
      break;
      
    case '<': //Frame Down, Weak, Negative
      stepCCW();
      break;
      
    case '+':
      if (ledValue < 255){
        ledValue = ledValue + 15;
        analogWrite(camLed, ledValue);}
      break;
      
    case '-':
      if (ledValue > 1){
        ledValue = ledValue - 15;
        analogWrite(camLed, ledValue);}
      break;

//Case 't': For testing 
    case 't':
      if(leftIsOpen() == true){
        Serial.print("Left: OPEN ");}
      else{
        Serial.print("Left: CLOSED ");}
      if(rightIsOpen() == true){
        Serial.print("Right: OPEN");}
      else{
        Serial.print("Right: CLOSED");}
      if(lockIsOpen() == true){
        Serial.print("Lock: OPEN");}
      else{
        Serial.print("Lock: CLOSED");}
      Serial.print("\n");
      break;

    case 'c':
      result = findCenter();
      Serial.println(result);
      break;
  }
}
