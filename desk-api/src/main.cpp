#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>

const int POT_PIN = A0;
const int BUTTON_PIN = 2;
const int LDR_PIN = A1;

// Instantiate the AHT10 sensor object
Adafruit_AHTX0 aht;

void setup() {
  // run once:
  Serial.begin(9600);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Initialize the AHT10 sensor
  if (!aht.begin()) {
    Serial.println("{\"error\":\"Could not find AHT10!\"}");
    while (1) delay(10); // Halt if sensor isn't found
  }

}

void loop() {
  // Run repeatedly:
  int potValue = analogRead(POT_PIN);
  int buttonState = digitalRead(BUTTON_PIN);
  int ldrValue = analogRead(LDR_PIN);

  // Create event objects and read data from the AHT10
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  Serial.print("{\"pot\":");
  Serial.print(potValue);

  Serial.print(",\"button\":");
  Serial.print(buttonState);

  Serial.print(",\"ldr\":");
  Serial.print(ldrValue);

  Serial.print(",\"temperature\":");
  Serial.print(temp.temperature);

  Serial.print(",\"humidity\":");
  Serial.print(humidity.relative_humidity);

  Serial.println("}");

  delay(100);
}