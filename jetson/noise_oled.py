import time
import numpy as np
import sounddevice as sd
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

class Display:
    def __init__(self):
        self.create_display()

        # Create blank image for drawing
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("DejaVuSans.ttf", 24)

    def create_display(self):
        while True:
            try:
                self.display = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=0, gpio=1)
                self.display.begin()
                self.display.clear()
                self.display.display()
                break
            except Exception:
                print("Error creating display. Retrying...")
                time.sleep(1)

    def update_display(self, noise_level):
        try:
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw.text((0, 0), f'{noise_level} dB', font=self.font, fill=255)

            self.display.image(self.image)
            self.display.display()
        except IOError:
            print("Error updating display. Retrying...")
            self.create_display()


def get_noise_level():
    try:
        # Capture a short audio sample
        duration = 0.5
        samplerate = 44100
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float64')
        sd.wait()

        volume_norm = np.sqrt(np.mean(recording**2))
        dbfs = 20 * np.log10(volume_norm) + 70

        return int(dbfs)

    except Exception as e:
        print(f"Error capturing audio: {e}")
        return 0

if __name__ == '__main__':
    display = Display()
    while True:
        noise_level = get_noise_level()
        display.update_display(noise_level)
