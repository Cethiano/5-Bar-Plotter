#include <Arduino.h>
#include <FastAccelStepper.h>
#include <LittleFS.h>



int stepPinMotor1 = 2;
int dirPinMotor1 = 3;
int enablePinMotor1 = 4;

int stepPinMotor2 = 5;
int dirPinMotor2 = 6;   
int enablePinMotor2 = 7;

File waypoints;

FastAccelStepperEngine engine = FastAccelStepperEngine();  
FastAccelStepper *stepper1 = NULL;  
FastAccelStepper *stepper2 = NULL;  

int motor1Rotation = 0;
int motor2Rotation = 0;

void setup() {
  LittleFS.begin();

  Serial.begin(115200);

  waypoints = LittleFS.open("/waypoints.csv", "r");

  
  delay(10000);

  stepper1 = engine.stepperConnectToPin(stepPinMotor1);
  stepper1->setDirectionPin(dirPinMotor1);  
  stepper1->setEnablePin(enablePinMotor1);
  stepper1->setAutoEnable(true);

  stepper2 = engine.stepperConnectToPin(stepPinMotor2);
  stepper2->setDirectionPin(dirPinMotor2);  
  stepper2->setEnablePin(enablePinMotor2);
  stepper2->setAutoEnable(true);

}


void loop() {
  if (!(stepper1->isRunning() || stepper2->isRunning())) {
    String currentWaypoint = waypoints.readStringUntil('\n');

    int commaIndex = currentWaypoint.indexOf(',');

    motor1Rotation = currentWaypoint.substring(0, commaIndex).toInt();
    motor2Rotation = currentWaypoint.substring(commaIndex + 1, currentWaypoint.indexOf('\n')).toInt();

    //Serial.print("Motor 1 Rotation: ");
    //Serial.println(motor1Rotation); 
    //Serial.print("Motor 2 Rotation: ");
    //Serial.println(motor2Rotation);
  
    stepper1->moveTo(motor1Rotation);
    stepper2->moveTo(motor2Rotation);
  }

  delay(100);

  
}
