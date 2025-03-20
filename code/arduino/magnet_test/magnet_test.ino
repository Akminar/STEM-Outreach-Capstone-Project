const int hallSensorPin = 2;  // Sensor output connected to pin 2
const int ledPin = 13;        // LED connected to pin 13 (optional)

void setup() {
    pinMode(hallSensorPin, INPUT);
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    int sensorState = digitalRead(hallSensorPin);

    if (sensorState == LOW) {  // Magnet detected
        Serial.println("Magnet detected!");
        digitalWrite(ledPin, HIGH);  // Turn on LED
    } else {
        Serial.println("No magnet detected.");
        digitalWrite(ledPin, LOW);  // Turn off LED
    }

    delay(1);
}