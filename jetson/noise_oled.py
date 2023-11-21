import time
import numpy as np
import sounddevice as sd
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# OLED display initialization
display = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=0, gpio=1)
display.begin()
display.clear()
display.display()

# Create blank image for drawing
width = display.width
height = display.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def update_display(noise_level):
    try:
        # Draw a black filled box to clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        font_size = 20
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)

        # Draw the text
        draw.text((0, 0), f'{noise_level} dB', font=font, fill=255)

        display.image(image)
        display.display()
    except IOError:
        print("Error updating display. Retrying...")
        time.sleep(1)

def get_noise_level():
    try:
        # Capture a short audio sample
        duration = 0.5 # Duration in seconds
        samplerate = 44100 # Sample rate in Hz
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float64')
        sd.wait()

        # Calculate noise level
        volume_norm = np.sqrt(np.mean(recording**2))

        dbfs = 20 * np.log10(volume_norm) + 70
        return int(dbfs)
    except Exception as e:
        print(f"Error capturing audio: {e}")
        return 0

try:
    while True:
        # Get the current noise level
        noise_level = get_noise_level()

        # Update the display with the noise level
        update_display(noise_level)

except KeyboardInterrupt:
    print("Stopping noise measurement")
    display.clear()
    display.display()
