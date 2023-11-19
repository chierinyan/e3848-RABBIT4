#include <Servo.h>
#include "base.h"

double prev_error[4] = {0,0,0,0};
double integral[4] = {0,0,0,0};

unsigned long prev_time = 0;
long prev_enc[4] = {0,0,0,0};
volatile long enc[4] = {0,0,0,0};

int hold = 1;
double rps[4] = {0,0,0,0};
double curr_rps[4] = {0,0,0,0};

Servo armServo;

void (*enc_cb[4])() = {
    [](){if (digitalRead(ENCB_PINS[0])) --enc[0]; else ++enc[0];},
    [](){if (digitalRead(ENCB_PINS[1])) ++enc[1]; else --enc[1];},
    [](){if (digitalRead(ENCB_PINS[2])) --enc[2]; else ++enc[2];},
    [](){if (digitalRead(ENCB_PINS[3])) ++enc[3]; else --enc[3];},
};

void set_vel(int lx=0, int ly=0, int az=0) {
    rps[0] = (lx + ly - D * az) * R;
    rps[1] = (lx - ly + D * az) * R;
    rps[2] = (lx - ly - D * az) * R;
    rps[3] = (lx + ly + D * az) * R;
}

void set_arm(int cmd) {
    hold = cmd;
}

byte ultrasonic() {
    return 233;
}

void set_motor(int motor) {
    double error = rps[motor] - curr_rps[motor];
    double derivative = error - prev_error[motor];
    integral[motor] += error;
    prev_error[motor] = error;
    int pwm = KP * error + KI * integral[motor] + KD * derivative;

    int dir = pwm > 0;
    pwm = abs(pwm);
    if (pwm < MIN_PWM) {
        digitalWrite(PWM_PINS[motor], 0);
        digitalWrite(DIR1_PINS[motor], HIGH);
        digitalWrite(DIR2_PINS[motor], HIGH);
    } else {
        if (pwm > MAX_PWM) pwm = MAX_PWM;
        analogWrite(PWM_PINS[motor], pwm);
        digitalWrite(DIR1_PINS[motor], dir);
        digitalWrite(DIR2_PINS[motor], !dir);
    }
}

void base_setup() {
    armServo.attach(ARM_PIN);

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
    unsigned long curr_time = micros();
    if (curr_time - prev_time > 5000) {
        for (int i=0; i<4; i++) {
            curr_rps[i] = (enc[i] - prev_enc[i]) * 1.0e6 / (curr_time - prev_time) / ENC_PR;
            prev_enc[i] = enc[i];
        }
        prev_time = curr_time;
    }

    for (int i=0; i<4; i++) {
        set_motor(i);
    }

    if (hold) {
        armServo.write(ARM_HOLD_ANGLE);
    } else {
        armServo.write(ARM_RELEASE_ANGLE);
    }
}
