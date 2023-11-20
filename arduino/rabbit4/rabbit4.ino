void setup() {
    base_setup();
    chaser_setup();

    Serial.begin(115200);
    Serial.println("RABBIT4");

}

void loop() {
    base_loop();
    chaser_loop();
}
