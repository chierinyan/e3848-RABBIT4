#include <INA226.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET 28

INA226 ina;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

unsigned long time;


void oled_setup() {
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
        Serial.println(F("SSD1306 allocation failed"));
    }
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.cp437(true);

    ina.begin();
    ina.configure(INA226_AVERAGES_16, INA226_BUS_CONV_TIME_2116US, INA226_SHUNT_CONV_TIME_2116US, INA226_MODE_SHUNT_BUS_CONT);
    ina.calibrate(0.002, 0.2);
}


void oled_loop() {
    if (millis() > time) {
        time = millis() + 500;

        display.clearDisplay();
        display.setCursor(0, 0);
        display.print("Voltage: ");
        display.print(ina.readBusVoltage(), 3);
        display.println(" V");
        display.print("Power: ");
        display.print(ina.readBusPower(), 3);
        display.println(" W");
        display.display();
    }
}
