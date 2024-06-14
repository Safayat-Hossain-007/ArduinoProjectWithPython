int pirPin = 2; // PIR sensor connected to digital pin 2
int relayPin = 3; // Relay module connected to digital pin 3
int pirState = LOW; // By default, no motion detected

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // Turn off relay (fan) initially
  Serial.begin(9600);
}

void loop() {
  pirState = digitalRead(pirPin);
  if (pirState == HIGH) {
    Serial.println("MOTION_DETECTED");
    digitalWrite(relayPin, HIGH); // Turn on relay (fan)
    delay(10000); // Keep the fan on for 10 seconds
    digitalWrite(relayPin, LOW); // Turn off relay (fan)
  }
  delay(500); // Small delay to avoid spamming serial messages
}
