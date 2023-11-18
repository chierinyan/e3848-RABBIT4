#include "base.h"

byte cmd[4] = {0,0,0,0};

void setup() {
    Serial.begin(115200);
    Serial.println("RABBIT4");

    base_setup();
}

void loop() {
    if (Serial.available() >= 5) {
        byte header = Serial.read();
        if (header == 255) {
            for (int i = 0; i < 4; i++) {
                cmd[i] = Serial.read();
            }
        }

        Serial.write(ultrasonic());

        cmd_vel(cmd[0], cmd[1], cmd[2]);
        cmd_arm(cmd[3]);

    }
    base_loop();
}
