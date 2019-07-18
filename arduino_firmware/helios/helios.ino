#include "serial_handler.h"
#include <TimerOne.h>

byte bitMask;
char inboundSerialBuffer[5];
char outboundSerialBuffer[3];
SerialHandler serial(inboundSerialBuffer, outboundSerialBuffer);

const int indicatorBlinkInterval = 400;

const int leftIndicatorPin = 12;
const int rightIndicatorPin = 13;
const int frontLightPin = 10;
const int rearLightPin = 9;

volatile byte leftIndicatorState = LOW;
volatile byte rightIndicatorState = LOW;

volatile bool timerInterruptAttached = false;

void leftIndicatorBlink()
{
    leftIndicatorState = !leftIndicatorState;
    digitalWrite(leftIndicatorPin, leftIndicatorState);
}

void rightIndicatorBlink()
{
    rightIndicatorState = !rightIndicatorState;
    digitalWrite(rightIndicatorPin, rightIndicatorState);
}

void alertBlink()
{
    leftIndicatorState = !leftIndicatorState;
    rightIndicatorState = leftIndicatorState;
    digitalWrite(leftIndicatorPin, leftIndicatorState);
    digitalWrite(rightIndicatorPin, rightIndicatorState);
}

bool verifyCode(byte code)
{
    byte mask = 0b00001000;
    int highCnt = 0;
    
    for (int i = 0; i < 3; i++)
    {
        if (code & mask)
            ++highCnt;
        mask <<= 1;
    }
    
    if (highCnt == 0 || highCnt == 1)
        return true;
    else
        return false;
}

void setup()
{
    // Initialize both serial buffers.
    memset(inboundSerialBuffer, '\0', 2);
    memset(outboundSerialBuffer, '\0', 3);
    
    // Set pin modes.
    pinMode(leftIndicatorPin, OUTPUT);
    pinMode(rightIndicatorPin, OUTPUT);
    pinMode(frontLightPin, OUTPUT);
    pinMode(rearLightPin, OUTPUT);

    // Start serial communication.
    Serial.begin(57600);

    // Initialize timer interrupt.
    Timer1.initialize(indicatorBlinkInterval * 1000);

    // Indicate the computer that the Arduino is ready.
    Serial.println(0x01);
}

void loop()
{
    serial.Receive();
    if (serial.IsDataReady())
    {
        Serial.println(inboundSerialBuffer);
        if (verifyCode(inboundSerialBuffer[0]))
        {
//            outboundSerialBuffer[0] = 0x15;
            outboundSerialBuffer[0] = 'a';
            outboundSerialBuffer[1] = '\n';
            outboundSerialBuffer[2] = '\0';
//            Serial.println(outboundSerialBuffer);
            Serial.println("Invalid");
        }
        else
        {
            Serial.println("Here!");
            if (timerInterruptAttached)
            {
                Timer1.detachInterrupt();
                timerInterruptAttached = false;
            }
            
            bitMask = 0b00001000;
            if (inboundSerialBuffer[0] & 0b00001000)
            {
                Timer1.attachInterrupt(alertBlink);
                timerInterruptAttached = true;
            }
            else if (inboundSerialBuffer[0] & 0b00010000)
            {
                Timer1.attachInterrupt(rightIndicatorBlink);
                timerInterruptAttached = true;
            }
            else if (inboundSerialBuffer[0] & 0b00100000)
            {
                Timer1.attachInterrupt(leftIndicatorBlink);
                timerInterruptAttached = true;
            }

            if (inboundSerialBuffer[0] & 0b01000000)
                digitalWrite(rearLightPin, HIGH);
            else
                digitalWrite(rearLightPin, LOW);
    
            if (inboundSerialBuffer[0] & 0b10000000)
                digitalWrite(frontLightPin, HIGH);
            else
                digitalWrite(frontLightPin, LOW);

            outboundSerialBuffer[0] = 0x06;
            outboundSerialBuffer[1] = '\n';
            outboundSerialBuffer[2] = '\0';
            Serial.println(outboundSerialBuffer);
        }

        serial.SetDataState(false);
    }

    serial.DeactivateSerial();
}
