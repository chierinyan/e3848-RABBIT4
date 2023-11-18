#pragma once

#define D 1
#define R 2
#define ENC_PR 330
#define MIN_PWM 16
#define MAX_PWM 255

#define ARM_PIN 62
#define ARM_HOLD_ANGLE 180
#define ARM_RELEASE_ANGLE 0

static const int PWM_PINS[4] = {12, 8, 6, 5};
static const int DIR1_PINS[4] = {35, 37, 42, 58};
static const int DIR2_PINS[4] = {34, 36, 43, 59};
static const int ENCA_PINS[4] = {18, 19, 3, 2};
static const int ENCB_PINS[4] = {31, 38, 49, 23};

void set_vel(int, int, int);
void set_arm();
byte ultrasonic();
