#include "Arduino_BMI270_BMM150.h"
#include <Servo.h>
// for the arduino nano BLE Sense Rev 2

const float TILT_THRESHOLD = 0.1;
const int SCALE_FACTOR = 100;
const int MAX_RAW_VALUE = 97;
const int MAX_DEGREES = 90;

Servo servo;
float lastAngle = -1;

void setup() {
    Serial.begin(9600);
    while (!Serial);
    Serial.println("Started");

    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }

    Serial.print("Accelerometer sample rate = ");
    Serial.print(IMU.accelerationSampleRate());
    Serial.println(" Hz");

    servo.attach(9);  // Attach the servo to pin 9
}

void handleTilt(float value, const char* direction1, const char* direction2) {
    value *= SCALE_FACTOR;
    int degrees = map(abs(value), 0, MAX_RAW_VALUE, 0, MAX_DEGREES);
    Serial.print("Tilting ");
    Serial.print(value > 0 ? direction1 : direction2);
    Serial.print(" ");
    Serial.print(degrees);
    Serial.println(" degrees");
}

void set_servo_angle(float angle, int pin) {
  // Convert the angle to pulse width
  float pulse_width = (angle / 180.0) * 1000.0 + 1000.0;  // Scale from 1ms to 2ms
  int duty = int((pulse_width / 20000.0) * 255.0);  // Convert to duty cycle (0-255 range)
  
  analogWrite(pin, duty);
}

void loop() {
  while (Serial.available() > 0) {
    String receivedMessage = Serial.readString();
    receivedMessage.trim(); // Remove any leading/trailing whitespace

    if (receivedMessage.startsWith("IMU")) {
      float x, y, z;
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(x, y, z);
        if(abs(x) > TILT_THRESHOLD || abs(y) > TILT_THRESHOLD){
          float roll = atan2(y, z) * 180.0 / PI;
          float pitch = atan2(-x, sqrt(y * y + z * z)) * 180.0 / PI;

          Serial.print("Roll = ");
          Serial.print(roll);
          Serial.print(", Pitch = ");
          Serial.println(pitch);
        }
      }
    } else {
      float number = receivedMessage.toFloat();
      if (number >= 0.0 && number <= 1.0) {
        int angle = round((number*.3 +.35) * 180);
        if (angle != lastAngle) {  // Only write to the servo if the angle has changed
          Serial.print("Received number: ");
          Serial.println(number);
          servo.write(angle); // control pwm D9 servo
          lastAngle = angle;  // Update the last angle
        }
      }
    }
  }
}