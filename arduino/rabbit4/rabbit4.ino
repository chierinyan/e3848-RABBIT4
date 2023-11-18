void setup() {
    Wire.begin();
    Serial.begin(115200);
    Serial.println("RABBIT4");

    base_setup();
}

int cmd[4] = {0, 0, 0, 0};
void loop() {
    if (Serial.parseInt() == -1) {
        for (int i = 0; i < 4; i++) {
            cmd[i] = Serial.parseInt();
        }
    }
    cmd_vel(cmd[0], cmd[1], cmd[2]);
    Serial.print(cmd[0]);
    Serial.print(" ");
    Serial.print(cmd[1]);
    Serial.print(" ");
    Serial.println(cmd[2]);
    base_loop();
}
