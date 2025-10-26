/*
 * Voice-Controlled Embedded System
 * Compatible with Python voice control interface
 * 
 * Commands:
 * 'U' - Glow white LED
 * 'D' - Glow red LED
 * 'R' - Rotate servo 90 degrees
 * 'S' - Stop all operations
 */

#include <Servo.h>

// Pin definitions
const int WHITE_LED_PIN = 9;
const int RED_LED_PIN = 10;
const int SERVO_PIN = 11;

// Servo object
Servo myServo;

// Servo positions
const int SERVO_START = 0;
const int SERVO_END = 90;

// Current state
char currentCommand = 'S';
int servoPos = SERVO_START;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize LED pins
  pinMode(WHITE_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  
  // Initialize servo
  myServo.attach(SERVO_PIN);
  myServo.write(SERVO_START);
  
  // Turn off all LEDs initially
  digitalWrite(WHITE_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  
  // Signal ready
  Serial.println("Arduino Ready");
}

void loop() {
  // Check for incoming serial commands
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Process the command
    switch (command) {
      case 'U':
      case 'u':
        // Glow white LED
        digitalWrite(WHITE_LED_PIN, HIGH);
        digitalWrite(RED_LED_PIN, LOW);
        currentCommand = 'U';
        Serial.println("White LED ON");
        break;
        
      case 'D':
      case 'd':
        // Glow red LED
        digitalWrite(RED_LED_PIN, HIGH);
        digitalWrite(WHITE_LED_PIN, LOW);
        currentCommand = 'D';
        Serial.println("Red LED ON");
        break;
        
      case 'R':
      case 'r':
        // Rotate servo 90 degrees
        servoPos = SERVO_END;
        myServo.write(servoPos);
        currentCommand = 'R';
        Serial.println("Servo rotated 90 degrees");
        break;
        
      case 'S':
      case 's':
        // Stop all operations
        digitalWrite(WHITE_LED_PIN, LOW);
        digitalWrite(RED_LED_PIN, LOW);
        servoPos = SERVO_START;
        myServo.write(servoPos);
        currentCommand = 'S';
        Serial.println("All stopped");
        break;
        
      default:
        // Unknown command
        Serial.print("Unknown command: ");
        Serial.println(command);
        break;
    }
  }
  
  // Small delay to prevent overwhelming the serial buffer
  delay(10);
}
