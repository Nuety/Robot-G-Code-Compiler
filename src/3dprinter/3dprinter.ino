#include <Stepper.h>
#include <AceRoutine.h>
using namespace ace_routine;

#define stp 8
#define dir 7
#define MS1 5
#define MS2 6
#define enable 4
#define relayPinHotend 2
#define relayPinBed 3
#define ThermistorPinHotend A0
#define ThermistorPinBed A1

int VoBed, VoHotend;
float R1 = 100000;
float LogRBed, RBed, TBed;
float LogRHotend, RHotend, THotend;
float A = 0.4184502937e-03, B = 2.524894441e-04, C = 0.1879018527e-07;
float maxHotendTemp = 30.0;
float maxBedTemp = 30.0;


bool servoRun = false;
String x; 

COROUTINE(Commands) {
  COROUTINE_LOOP() {
    while (!Serial.available()) {
      COROUTINE_DELAY(0);
    } 
    x = Serial.readString(); 
    if (x == "G1") {
      servoRun = true;
      Serial.print(servoRun);
      
    }
    else if(x == "G0") {
      servoRun = false;
      Serial.print(servoRun);
    } 
  }
}

COROUTINE(HeatingRoutine){
  COROUTINE_LOOP() {
    COROUTINE_DELAY(1000);
    VoBed = analogRead(ThermistorPinBed);
    RBed = R1 * (1023.0 / (float)VoBed - 1.0);
    LogRBed = log(RBed);
    TBed = ((1.0 / (A + B*LogRBed + C*LogRBed*LogRBed*LogRBed)) - 273.15);

    VoHotend = analogRead(ThermistorPinHotend);
    RHotend = R1 * (1023.0 / (float)VoHotend - 1.0);
    LogRHotend = log(RHotend);
    THotend = ((1.0 / (A + B*LogRHotend + C*LogRHotend*LogRHotend*LogRHotend)) - 273.15);
    //check hotend temperature

    if (THotend >= maxHotendTemp) {
      digitalWrite(relayPinHotend, LOW);
    } else {
      digitalWrite(relayPinHotend, HIGH);
    }

    //check bed temperature
    if (TBed >= maxBedTemp) {
      digitalWrite(relayPinBed, LOW);
    } else {
      digitalWrite(relayPinBed, HIGH);
    }
  }
}

COROUTINE(ServoRoutine){
  COROUTINE_LOOP() {
      COROUTINE_AWAIT(servoRun);
      digitalWrite(stp, HIGH);
      digitalWrite(stp, LOW);
      COROUTINE_DELAY(17.2787);
  }
}

void setup() { 
	Serial.begin(115200); 
	Serial.setTimeout(1); 
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(enable, OUTPUT);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(dir, LOW);

} 

void loop() { 
  ServoRoutine.runCoroutine();
  HeatingRoutine.runCoroutine();
  Commands.runCoroutine();
}
