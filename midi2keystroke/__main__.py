# Imports pyhton-rtmidi 1.1.0 for midi processing
# documentation can be found here: https://spotlightkid.github.io/python-rtmidi/rtmidi.html#usage-example
import rtmidi
import time
import ctypes
import pyaudio
import wave
import sys
import midi2keystroke.alias as alias
import midi2keystroke.audio as audio
########################
#   Keystroke Code     #
########################
LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))

class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARD = 2

def Input(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(INPUT_HARDWARE, _INPUTunion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')



def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)


def KeybdInput(code, flags):
    return KEYBDINPUT(code, code, flags, 0, None)

def HardwareInput(message, parameter):
    return HARDWAREINPUT(message & 0xFFFFFFFF,
                         parameter & 0xFFFF,
                         parameter >> 16 & 0xFFFF)

def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))

def Keyboard(code, flags=0):
    return Input(KeybdInput(code, flags))

def Hardware(message, parameter=0):
    return Input(HardwareInput(message, parameter))

###########################
#   Launchpad Functions   #
###########################

def poll_input():
    message = midi_in.get_message()

    if not message:
        return None, None, None
    controller, key, velocity = message[0]
    return controller, key, velocity

# Function for initializing each key on the launchpad to red. Verifies each key works.
def initialize_launchpad(color):
    grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18, 19, 20, 21, 22, 23, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 49,
            50, 51, 52, 53, 54, 55, 56, 57, 64, 65, 66, 67, 68, 69, 70, 71, 72, 80, 81, 82, 83, 84, 85, 86, 87, 88, 96,
            97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    for x in grid:
        # Initialize every key to set color
        if x <= 111 and x >= 104:
            midi_out.send_message([176, x, color])
        midi_out.send_message([144, x, color])


def set_grid_color(color):
    grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18, 19, 20, 21, 22, 23, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 49,
            50, 51, 52, 53, 54, 55, 56, 57, 64, 65, 66, 67, 68, 69, 70, 71, 72, 80, 81, 82, 83, 84, 85, 86, 87, 88, 96,
            97, 98, 99, 100, 101, 102, 103, 104, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    for x in grid:
        # Initialize every key to RED
        # if x <= 111 and x >= 104:
        #   midi_out.send_message([176, x, color])
        # time.sleep(0.01)
        midi_out.send_message([144, x, color])

def set_control_color(color):
    control_row  = [104, 105, 106, 107, 108, 109, 110, 111]
    for button in control_row:
        midi_out.send_message([176, button, color])


def spiral_set_grid(color):
    spiral = [0, 16, 32, 48, 64, 80, 96, 112, 113, 114, 115, 116, 117, 118, 119, 103, 87, 71, 55, 39, 23, 7, 6, 5, 4, 3,
              2, 1, 17, 33, 49, 65, 81, 97, 98, 99, 100, 101, 102, 86, 70, 54, 38, 22, 21, 20, 19, 18, 34, 50, 66, 82,
              83, 84, 85, 69, 53, 37, 36, 35, 51, 67, 68, 52]
    for key in spiral:
        midi_out.send_message([144, key, color])
        time.sleep(0.02)

def rings(ring, color):
    # Ring 1-4 for which wring to set
    ring={
        1: [0,1,2,3,4,5,6,7]
    }

# function for setting key to a solid color. version defines which launchpad is being used, currently only mk.1 Works
# color for mk.1 are only red and green
def solid_light(key, color, version, brightness):
    pass

def map_key_color(key_dict, color):
    for cont in key_dict:
        for key in key_dict[cont]:
            midi_out.send_message([cont, key, color])

def flash_key(controller, key, color1, color2):
    midi_out.send_message([controller, key, color2])
    time.sleep(.1)
    midi_out.send_message([controller, key, color1])
    time.sleep(.1)
    midi_out.send_message([controller, key, color2])
    time.sleep(.1)
    midi_out.send_message([controller, key, color1])



# sets input/output object
midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()

# Searches port names for the Launchpad and opens the midi port associated with it
#print midi_in.get_ports()

for port_names in midi_in.get_ports():
    name_in, port_in = port_names.rsplit(' ', 1)

    # debug code
#    print name_in, port_in

    if name_in == "Launchpad":
        midi_in.open_port(int(port_in))
        break

#print midi_out.get_ports()

for port_names in midi_out.get_ports():
    name_out, port_out = port_names.rsplit(' ', 1)

    # debug code
#    print name_out, port_out

    if name_out == "Launchpad":
        midi_out.open_port(int(port_out))
        break

# Prints the current message in the Midi Buffer; prints nothing if there is nothing in the midi buffer
print midi_in.get_message()


responses = {
    144: { 114: "Ring10.wav",
           115: "boop.wav",
           116: "This is a string",
           117: alias.VK_MEDIA_PREV_TRACK,
           118: alias.VK_MEDIA_PLAY_PAUSE,
           119: alias.VK_MEDIA_NEXT_TRACK
           },
    176: { 104: alias.VK_VOLUME_UP,
           105: alias.VK_VOLUME_DOWN
           }
}
set_control_color(0)
initialize_launchpad(15)
spiral_set_grid(0)
time.sleep(1)
map_key_color(responses, 63)
while True:
#    message = midi_in.get_message()
#
#    if not message:
#
#        continue
    message = poll_input()
    if message:
        controller, key, velocity = poll_input()


        if velocity == 127:
            print controller, key, velocity
            try:
                response = responses[controller][key]
                if str(response).isdigit():
                    SendInput(Keyboard(response))
                    #flash_key(controller, key, 63, 15)
                else:
                    print "'" + response + "' is not Not Numerical"
                    if '.wav' in response:
                        audio.play_audio(response, key, poll_input()[1])
                        #flash_key(controller, key, 63, 15)



            except KeyError:
                    pass

