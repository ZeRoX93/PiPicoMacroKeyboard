# RaspberryPi Pico RP2040 Mechanical Keyboard

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import microcontroller

print("---Pico Pad Keyboard---")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# list of pins to use
pins = [
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP18,
    board.GP19,
    board.GP20,
]

MEDIA = 1
KEY = 2
KEYMAP_LAYOUT = 0

print("---Keymap Layout: ", KEYMAP_LAYOUT)
print("---Temp:", microcontroller.cpu.temperature, "C")


keymap = {
    (0): (KEY, (Keycode.GUI, Keycode.C)),
    (1): (KEY, (Keycode.GUI, Keycode.V)),
    (2): (KEY, [Keycode.THREE]),
    (3): (KEY, [Keycode.FOUR]),
    (4): (KEY, [Keycode.FIVE]),
    (5): (MEDIA, ConsumerControlCode.VOLUME_DECREMENT), #Volume Down
    (6): (MEDIA, ConsumerControlCode.VOLUME_INCREMENT), #Volume Up
    (7): (KEY, [Keycode.R]),
    (8): (KEY, [Keycode.G]),
    (9): (KEY, [Keycode.G]),
    (10): (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.KEYPAD_SEVEN)), #MUTE/UNMUTE MIC (LCTRL+LALT+Numpad 7)
    (11): (KEY, [Keycode.X]),
    (12): (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.KEYPAD_ONE)), #Starting Scene (LCTRL+LALT+Numpad 1)
    (13): (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.KEYPAD_TWO)), #Gaming Scene (LCTRL+LALT+Numpad 2)
    (14): (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.KEYPAD_THREE)), #Ending Scene (LCTRL+LALT+Numpad 3)
}
switches = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

for i in range(15):
    switches[i] = DigitalInOut(pins[i])
    switches[i].direction = Direction.INPUT
    switches[i].pull = Pull.UP

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while True:
    for button in range(15):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                    else:
                        cc.send(keymap[button][1])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])

                except ValueError:
                    pass
                switch_state[button] = 0


    time.sleep(0.01)  # debounce
