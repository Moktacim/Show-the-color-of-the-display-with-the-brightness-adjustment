import serial
from tkinter import *
import time
import pyautogui
from PIL import Image
import numpy as np

# Set up serial communication with Arduino Uno
ser = serial.Serial('COM3', 115200)

# Define LED strip parameters
NUM_LEDS = 33
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Send brightness value to Arduino Uno
def send_brightness(brightness):
    # Send the brightness value to the Arduino
    ser.write(bytes([brightness]))

# Create the GUI window
root = Tk()
root.title("LED Brightness Control")
root.geometry("300x100")

# Create a label for the brightness slider
brightness_label = Label(root, text="Brightness")
brightness_label.pack()

# Create a scale to adjust the brightness
brightness_scale = Scale(root, from_=0, to=255, orient=HORIZONTAL, command=send_brightness)
brightness_scale.set(60)  # Set the default brightness to 100
brightness_scale.pack()

# Continuously send color matrix with brightness
while True:
    # Capture screen and resize to LED strip resolution
    screen = pyautogui.screenshot(region=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = screen.resize((NUM_LEDS, 1), resample=Image.BILINEAR)

    # Convert image to RGB values
    screen_array = np.array(screen)
    screen_array = screen_array.reshape((NUM_LEDS, 3))
    screen_array = screen_array.tolist()

    # Send RGB values to Arduino Uno
    pixel_str = ' '.join([f'{p[0]} {p[1]} {p[2]}' for p in screen_array])
    #print(pixel_str)
    matrix_str = f'[{pixel_str}]'
    #print(matrix_str)

    # Update the color matrix with the selected brightness
    brightness = int(brightness_scale.get())
    color_matrix_with_brightness = [brightness] + [int(x) for x in matrix_str.strip("[]").split()]
    #print(color_matrix_with_brightness)

    matrix_str = ' '.join(str(c) for c in color_matrix_with_brightness)
    matrix_str1 = f'[{matrix_str}]'

    # Send the matrix string to the Arduino
    ser.write(matrix_str1.encode())
    print(matrix_str1)

    # Update the GUI window
    root.update()
    #time.sleep(0.001)
