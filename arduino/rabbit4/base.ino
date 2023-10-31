#include "base.h"

int rps[4];
volatile long enc[4] = {0, 0, 0, 0};
volatile long prev_enc[4] = {0, 0, 0, 0};

void (*enc_cb[4])() = {
    [](){if (digitalRead(ENCB_PINS[0])) enc[0]++; else enc[0]--;},
    [](){if (digitalRead(ENCB_PINS[1])) enc[1]++; else enc[1]--;},
    [](){if (digitalRead(ENCB_PINS[2])) enc[2]++; else enc[2]--;},
    [](){if (digitalRead(ENCB_PINS[3])) enc[3]++; else enc[3]--;},
};


void cmd_vel(double lx=0.0, double ly=0.0, double az=0.0) {
    rps[0] = (lx - ly - D * az) * R;
    rps[1] = (lx + ly + D * az) * R;
    rps[2] = (lx + ly - D * az) * R;
    rps[3] = (lx - ly + D * az) * R;

    int max_rps = 0;
    for (int i=0; i<4; i++) {
        if (abs(rps[i]) > max_rps) {
            max_rps = abs(rps[i]);
        }
    }
    if (max_rps > MAX_RPS) {
        for (int i=0; i<4; i++) {
            rps[i] = rps[i] * MAX_RPS / max_rps;
        }
    }
}

void set_motor(int motor, int pwm) {
    if (abs(pwm) < MIN_PWM) {
        digitalWrite(PWM_PINS[motor], 0);
        digitalWrite(DIR1_PINS[motor], HIGH);
        digitalWrite(DIR2_PINS[motor], HIGH);
    } else {
        analogWrite(PWM_PINS[motor], abs(pwm));
        if (pwm > 0) {
            digitalWrite(DIR1_PINS[motor], HIGH);
            digitalWrite(DIR2_PINS[motor], LOW);
        } else {
            digitalWrite(DIR1_PINS[motor], LOW);
            digitalWrite(DIR2_PINS[motor], HIGH);
        }
    }
}

void base_setup() {
    for (int i=0; i<4; i++) {
        pinMode(PWM_PINS[i], OUTPUT);
        pinMode(DIR1_PINS[i], OUTPUT);
        pinMode(DIR2_PINS[i], OUTPUT);
        pinMode(ENCA_PINS[i], INPUT);
        pinMode(ENCB_PINS[i], INPUT);
        attachInterrupt(digitalPinToInterrupt(ENCA_PINS[i]), enc_cb[i], RISING);
    }
}

void base_loop() {
    for (int i=0; i<4; i++) {
        set_motor(i, rps[i]);
    }
}
