#include <AceRoutine.h>
#include <AccelStepper.h>
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
float maxHotendTemp = 200.0;
float maxBedTemp = 60.0;

AccelStepper stepper(1, stp, dir);
bool servoRun = 0;
String Gcommand; 

COROUTINE(Commands) {
  COROUTINE_LOOP() {
    while (!Serial.available()) {
      COROUTINE_DELAY(0);
    } 
    Gcommand = Serial.readString(); 
    if (Gcommand.substring(0, 2) == "G1") {
      servoRun = 1;      
    }
    else if(Gcommand.substring(0, 2) == "G0") {
      servoRun = 0;
    } 
    else if (Gcommand.substring(0, 4) == "M140") {
      maxBedTemp = Gcommand.substring(4).toFloat();
    }
    else if (Gcommand.substring(0, 4) == "M190") {
      maxBedTemp = Gcommand.substring(4).toFloat();
    }
    else if (Gcommand.substring(0, 4) == "M104") {
      maxHotendTemp = Gcommand.substring(4).toFloat();
    }
    else if (Gcommand.substring(0, 4) == "M109") {
      maxHotendTemp = Gcommand.substring(4).toFloat();
    }
  }
}

COROUTINE(HeatingRoutine){
  COROUTINE_LOOP() {
    COROUTINE_DELAY(500);
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
      stepper.runSpeed();
  }
}

void setup() { 
	Serial.begin(115200); 
	Serial.setTimeout(1); 
  stepper.setMaxSpeed(1000);
  //speed of stepper in steps per second
  stepper.setSpeed(-(1500/((PI*11)/200)/60)*0.2);
} 

void loop() { 
  ServoRoutine.runCoroutine();
  HeatingRoutine.runCoroutine();
  Commands.runCoroutine();
}
