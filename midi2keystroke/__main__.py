
import time
import midi2keystroke.alias as alias
import midi2keystroke.util as util

responses = {
    144: { 114: "Spooky Scary Skeletons.wav",
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

# Map input and output for midi functions
util.bind_io()


util.set_control_color(0)
util.initialize_launchpad(15)
util.spiral_set_grid(0)
time.sleep(1)
util.map_key_color(responses, 63)
while True:
    controller, key, velocity = util.poll_input()

    if velocity == 127:
        print controller, key, velocity
        try:
            response = responses[controller][key]
            if str(response).isdigit():
                util.SendInput(util.Keyboard(response))
                # flash_key(controller, key, 63, 15)
            else:
                # print "'" + response + "' is not Not Numerical"
                if '.wav' in response:
                    # print key
                     util.play_audio(response, key)
                    # flash_key(controller, key, 63, 15)

        except KeyError:
                pass

