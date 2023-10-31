#define D 1.0
#define R 1
#define ENC_PR 330
#define MIN_RPS 0.1
#define MAX_RPS 255
#define MIN_PWM 16
#define MAX_PWM 255
#define MIN_VEL (MIN_RPS * 2 * 3.14 * R)
#define MAX_VEL (MAX_RPS * 2 * 3.14 * R)

static const int PWM_PINS[4] = {12, 8, 6, 5};
static const int DIR1_PINS[4] = {35, 37, 42, 58};
static const int DIR2_PINS[4] = {34, 36, 43, 59};
static const int ENCA_PINS[4] = {18, 19, 3, 2};
static const int ENCB_PINS[4] = {31, 38, 49, 23};
