/*
********************************************************************************
* Filename      : Kinematic Controller
* Author        : Susung Park
* Description   : Kinematics controller for autonomous vehicle.
* Version       : On development...
********************************************************************************
*/

#include "pid_controller.h"
#include "serial_handler.h"
#include "motor.h"

// Serial handler buffers.
char inboundSerialBuffer[100];
char outboundSerialBuffer[100];
SerialHandler serial(inboundSerialBuffer, outboundSerialBuffer);

// Encoder values
EncoderMotor encoderMotor(13, 11, 2, 3);

long posTarget;

// Initiate PID controllers.
PIDController<long, long> positionPID(15, 0.001, 0.001);
PIDController<long, long> velocityPID(2, 0.001, 0.001);
long positionPIDOutput;
int velocityPIDOutput;

void encoderCallback()
{
    if (digitalRead(encoderMotor.GetEncoderDirPin()) == LOW)
        encoderMotor.Increment();
    else
        encoderMotor.Decrement();
        
    positionPID.SetSysoutVal(encoderMotor.GetEncoderVal());
    velocityPID.SetSysoutVal(encoderMotor.GetEncoderSpeed());

    int val = encoderMotor.GetEncoderVal();
    if (val % 20 == 0)
        Serial.println(val);
}

void setup()
{
    Serial.begin(57600);

    // Attach interrupt to pin 2.
    attachInterrupt(digitalPinToInterrupt(2), encoderCallback, FALLING);
}

void loop()
{
    serial.Receive();
    if (serial.IsDataReady())
    {
        posTarget = atol(inboundSerialBuffer);
        positionPID.SetTargetVal(posTarget);
        Serial.print(posTarget);
        Serial.println(" is given as target.");
        serial.ConsumeData();
    }
    
    positionPIDOutput = positionPID.ExecFreePID(posTarget);
    velocityPID.SetTargetVal(positionPIDOutput);
    velocityPIDOutput = velocityPID.ExecClippedPID(positionPIDOutput, -50, 50);
    encoderMotor.SetSpeed(velocityPIDOutput);
    
//    Serial.print("Target Pos: ");
//    Serial.print(posTarget);
//    Serial.print(" / Current Pos: ");
//    Serial.print(encoderMotor.GetEncoderVal());
//    Serial.print(" / Position PID: ");
//    Serial.print(positionPIDOutput);
//    Serial.print(" / Velocity PID: ");
//    Serial.println(velocityPIDOutput);
//    delay(100);
}
