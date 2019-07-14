/*
********************************************************************************
* Filename      : Kinematic Controller
* Author        : Susung Park
* Description   : Kinematics controller for autonomous vehicle.
* Version       : On development...
********************************************************************************
*/

#include "pid_controller.h"

// Encoder values
const int encoderDir1Pin = 12;
const int encoderDir2Pin = 11;
const int encoderClockPin = 2;

int encoderDiff = 0;
int encoderSteps = 0;
float encoderSpeed = 0.0;

// Initiate PID controllers.
PIDController<float, float> motorPID(500, 10, 1);
PIDController<float, float> positionPID(5, 0.1, 0.5);
float positionPIDOutput;

void encoderCallback()
{
    int dir1 = digitalRead(encoderDir1Pin);
    int dir2 = digitalRead(encoderDir2Pin);
    
    if (dir1 == HIGH && dir2 == LOW)
        ++encoderSteps;
    else if (dir1 == LOW && dir2 == HIGH)
        --encoderSteps;
}

void setup()
{
    // Setup pins.
    pinMode(encoderDir1Pin, INPUT);
    pinMode(encoderDir2Pin, INPUT);
    pinMode(encoderClockPin, INPUT);

    // Attach interrupt to pin 2.
    attachInterrupt(digitalPinToInterrupt(2), encoderCallback, RISING);
}

void loop()
{
    positionPIDOutput = positionPID.ExecFreePID(encoderSteps);
}
