# Imports pyhton-rtmidi 1.1.0 for midi processing
# documentation can be found here: https://spotlightkid.github.io/python-rtmidi/rtmidi.html#usage-example
import rtmidi
import time


# Function for initializing each key on the launchpad to red. Verifies each key works.
def initialize_launchpad():
    grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18, 19, 20, 21, 22, 23, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 64, 65, 66, 67, 68, 69, 70, 71, 72, 80, 81, 82, 83, 84, 85, 86, 87, 88, 96, 97, 98, 99, 100, 101, 102, 103, 104, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    for x in grid:
        # Initialize every key to RED
        if x <= 111 and x >= 104:
            midi_out.send_message([176, x, 31])
        midi_out.send_message([144, x, 31])

def set_gric_color(color):
    grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18, 19, 20, 21, 22, 23, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 64, 65, 66, 67, 68, 69, 70, 71, 72, 80, 81, 82, 83, 84, 85, 86, 87, 88, 96, 97, 98, 99, 100, 101, 102, 103, 104, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    for x in grid:
        # Initialize every key to RED
        #if x <= 111 and x >= 104:
         #   midi_out.send_message([176, x, color])
            # time.sleep(0.01)
        midi_out.send_message([144, x, color])

def spiral_set_grid(color):
    spiral = [0, 16, 32, 48, 64, 80, 96, 112, 113, 114, 115, 116, 117, 118, 119, 103, 87, 71, 55, 39, 23, 7, 6, 5, 4, 3, 2, 1, 17, 33, 49, 65, 81, 97, 98, 99, 100, 101, 102, 86, 70, 54, 38, 22, 21, 20, 19, 18, 34, 50, 66, 82, 83, 84, 85, 69, 53, 37, 36, 35, 51, 67, 68, 52]
    for key in spiral:
        midi_out.send_message([144, key, color])
        time.sleep(0.03)


# function for setting key to a solid color. version defines which launchpad is being used, currently only mk.1 Works
# color for mk.1 are only red and green
def solid_light(key, color, version, brightness):
    pass

#sets input/output object
midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()

# Searches port names for the Launchpad and opens the midi port associated with it
print midi_in.get_ports()

for port_names in midi_in.get_ports():
    name_in, port_in = port_names.rsplit(' ',1)

    #debug code
    print name_in, port_in

    if name_in == "Launchpad":
        midi_in.open_port(int(port_in))
        break

print midi_out.get_ports()

for port_names in midi_out.get_ports():
    name_out, port_out = port_names.rsplit(' ', 1)

    # debug code
    print name_out, port_out

    if name_out == "Launchpad":
        midi_out.open_port(int(port_out))
        break



        # for port_name in midi_in:
#    if 'Launchpad' in port_name:
#        midi_in.open_port(port_name[::-1])

# Prints the current message in the Midi Buffer; prints nothing if there is nothing in the midi buffer
print midi_in.get_message()

initialize_launchpad()
time.sleep(1)
'''
set_gric_color(43)
time.sleep(1)
set_gric_color(44)
time.sleep(1)
set_gric_color(60)
time.sleep(1)
set_gric_color(61)
time.sleep(1)
set_gric_color(62)
time.sleep(1)
set_gric_color(63)
time.sleep(1)
set_gric_color(31)
'''
set_gric_color(64)
time.sleep(0.5)
spiral_set_grid(60)
#while True:
#    print midi_in.get_message()
#    time.sleep(1)

#  midiout.send_message([144, 0, 127]) Row 1, button 1 set to green



'''
# Row 1
midi_out.send_message([144, 0, 1])
midi_out.send_message([144, 1, 2])
midi_out.send_message([144, 2, 3])
midi_out.send_message([144, 3, 4])
midi_out.send_message([144, 4, 5])
midi_out.send_message([144, 5, 6])
midi_out.send_message([144, 6, 7])
midi_out.send_message([144, 7, 8])

# Row 2
midi_out.send_message([144, 16, 9])
midi_out.send_message([144, 17, 10])
midi_out.send_message([144, 18, 11])
midi_out.send_message([144, 19, 12])
midi_out.send_message([144, 20, 13])
midi_out.send_message([144, 21, 14])
midi_out.send_message([144, 22, 15])
midi_out.send_message([144, 23, 16])

# Row 3
midi_out.send_message([144, 32, 17])
midi_out.send_message([144, 33, 18])
midi_out.send_message([144, 34, 19])
midi_out.send_message([144, 35, 20])
midi_out.send_message([144, 36, 21])
midi_out.send_message([144, 37, 22])
midi_out.send_message([144, 38, 23])
midi_out.send_message([144, 39, 24])

# Row 4
midi_out.send_message([144, 48, 25])
midi_out.send_message([144, 49, 26])
midi_out.send_message([144, 50, 27])
midi_out.send_message([144, 51, 28])
midi_out.send_message([144, 52, 29])
midi_out.send_message([144, 53, 30])
midi_out.send_message([144, 54, 31])
midi_out.send_message([144, 55, 32])

# Row 5
midi_out.send_message([144, 64, 33])
midi_out.send_message([144, 65, 34])
midi_out.send_message([144, 66, 35])
midi_out.send_message([144, 67, 36])
midi_out.send_message([144, 68, 37])
midi_out.send_message([144, 69, 38])
midi_out.send_message([144, 70, 39])
midi_out.send_message([144, 71, 40])

# Row 6
midi_out.send_message([144, 80, 41])
midi_out.send_message([144, 81, 42])
midi_out.send_message([144, 82, 43])
midi_out.send_message([144, 83, 44])
midi_out.send_message([144, 84, 45])
midi_out.send_message([144, 85, 46])
midi_out.send_message([144, 86, 47])
midi_out.send_message([144, 87, 48])

# Row 7
midi_out.send_message([144, 97, 49])
midi_out.send_message([144, 98, 50])
midi_out.send_message([144, 99, 51])
midi_out.send_message([144, 100, 52])
midi_out.send_message([144, 101, 53])
midi_out.send_message([144, 102, 54])
midi_out.send_message([144, 103, 55])
midi_out.send_message([144, 104, 56])

# Row 8
midi_out.send_message([144, 112, 57])
midi_out.send_message([144, 113, 58])
midi_out.send_message([144, 114, 59])
midi_out.send_message([144, 115, 60])
midi_out.send_message([144, 116, 61])
midi_out.send_message([144, 117, 62])
midi_out.send_message([144, 118, 63])
midi_out.send_message([144, 119, 64])
'''
