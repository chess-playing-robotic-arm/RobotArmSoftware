#include <Servo.h>

Servo servoBase;
Servo servoRight;
Servo servoLeft;
Servo servoGripper;

void setup() {
  Serial.begin(9600);   // initialize serial communication at 9600 bits per second
  servoBase.attach(2);   // attach the base servo to pin 2
  servoRight.attach(3);   // attach the right servo to pin 3
  servoLeft.attach(4);   // attach the left servo to pin 4
  servoGripper.attach(5);   // attach the gripper servo to pin 5
}

void loop() {
  if (Serial.available() > 0) {   // check if there is any incoming serial data
    String inputString = Serial.readStringUntil('|');   // read the incoming string until the '|' character is received
    
    // print the received string to the serial monitor
    Serial.print("Received string: ");
    Serial.println(inputString);
    
    // parse the string into its component parts
    int motorNumber = inputString.charAt(0) - '0';   // extract the motor number as an integer
    int degrees = inputString.substring(1).toInt();   // extract the degrees as an integer
    
    // map the motor number to the appropriate servo object
    Servo* servo = NULL;
    switch(motorNumber) {
      case 2:
        servo = &servoBase;
        break;
      case 0:
        servo = &servoRight;
        break;
      case 1:
        servo = &servoLeft;
        break;
      case 3:
        servo = &servoGripper;
        break;
    }
    
    // set the servo position based on the parsed degrees
    if (servo != NULL) {
      servo->write(degrees);
    }
    
    // print the parsed parts to the serial monitor
    Serial.print("Motor ");
    Serial.print(motorNumber);
    Serial.print(" set to degrees ");
    Serial.println(degrees);
  }
}
