#include <Wire.h>

void setup() {
    Wire.begin();
    Serial.begin(115200);
    Serial.println("RABBIT4");

    base_setup();
    oled_setup();
    chaser_setup();
}

void loop() {
    base_loop();
    oled_loop();
    chaser_loop();
}
