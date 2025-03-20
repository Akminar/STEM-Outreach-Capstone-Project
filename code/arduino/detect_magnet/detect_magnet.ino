const int hallSensorPin = 2;  // Hall sensor connected to pin 2
const int ledPin = 13;        // LED for visual indication (optional)

volatile int magnetCount = 0;  // Count of magnet detections
unsigned long lastTime = 0;    // Time tracking for RPM calculation
const unsigned long interval = 1000;  // Interval for RPM calculation (1 second)
const int magnetsPerRevolution = 8;   // 8 magnets per full revolution

// Interrupt service routine (ISR) - Runs when a magnet is detected
void hallSensorISR() {
    magnetCount++;  // Increment count when magnet is detected
}

void setup() {
    pinMode(hallSensorPin, INPUT_PULLUP); // Enable internal pull-up resistor
    pinMode(ledPin, OUTPUT);
    Serial.begin(115200);

    attachInterrupt(digitalPinToInterrupt(hallSensorPin), hallSensorISR, FALLING);  
    // Triggers on falling edge when the magnet passes
}

void loop() {
    unsigned long currentTime = millis();

    if (currentTime - lastTime >= interval) {  // Every second, calculate RPM
        float revolutions = (float)magnetCount / magnetsPerRevolution;  // Convert magnet count to revolutions
        int rpm = (revolutions * 60);  // Convert to RPM

        Serial.println(rpm);  // Send RPM value over serial
        
        // Reset counter
        magnetCount = 0;
        lastTime = currentTime;
    }
}
