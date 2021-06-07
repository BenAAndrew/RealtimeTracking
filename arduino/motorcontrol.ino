#include <Servo.h>
#define INST_ARRAY_LEN          20

Servo pan;
Servo tilt;
int panPosition = 0;
int tiltPosition = 0;
char instruction[INST_ARRAY_LEN];
int instIndex = 0;
int minPan = 0;
int maxPan = 400;
int minTilt = 0;
int maxTilt = 400;

void processInstruction(char *instruction);

void setup() {
  pan.attach(0);
  tilt.attach(1);
  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  if(Serial.available() > 0) {
    char nextChar = Serial.read();
    // if char is new line last instruction complete, process instruction
    if(nextChar == '\n') {
      if(instIndex > 0) {
        instruction[instIndex] = nextChar;
        processInstruction(instruction);
        instIndex = 0;
      }
    }
    // add to instruction string
    else {
      if(instIndex >= INST_ARRAY_LEN){
        Serial.println("ERROR - loop() instruction parser: Instruction index out of bounds.");
      } else {
        instruction[instIndex] = nextChar;
        instIndex++;
      }
    }
  }
}

void processInstruction(char *input){
  int panValue = input.substring(4).toInt();
  int tiltValue = input.substring(6,10).toInt();
  int newPan = panPosition + panValue;
  int newTilt = tiltPosition + tiltValue;
  if(newPan < maxPan && newPan > minPan) {
      panPosition = newPan;
      pan.write(panPostion); 
  }
  if(newTilt < maxTilt && newTilt > minTilt) {
      tiltPosition = newTilt;
      tilt.write(tiltPostion); 
  }
}