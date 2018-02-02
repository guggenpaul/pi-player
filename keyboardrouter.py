from playercontroller import PlayerController
import keyboard
import time
import mediamanager

player_controller = PlayerController()
manager = mediamanager.MediaDirectoryManager('/home/multimedia/media')
kr = keyboard.KeyboardReader()

def load_video(num):
    v_int = int(num) - 1
    playlist = manager.get_media_files()
    print('Playing {0} from {1} len = {2}'.format(v_int, num, len(playlist)))
    if v_int < len(playlist):
        player_controller.load(playlist[v_int])

def set_video_output(key):
    if key == 'n':
        outputmanager.set_video_output('ntsc', '16:9')
    if key == 'm':
        outputmanager.set_video_output('ntsc', '4:3')
    if key == 'p':
        outputmanager.set_video_output('pal', '16:9')
    if key == 'o':
        outputmanager.set_video_output('pal', '4:3')
    if key == 'h':
        outputmanager.set_video_output('hdmi', '16:9')
    player_controller.reload(False)

def load_usb(k):
    player_controller.load('USB==USB')

def reload_pi(k):
    player_controller.reload()

for i in range(len(manager.get_media_files()) + 1):
    kr.add_binding(str(i), load_video)

kr.add_binding('h', set_video_output)
kr.add_binding('n', set_video_output)
kr.add_binding('m', set_video_output)
kr.add_binding('p', set_video_output)
kr.add_binding('o', set_video_output)
kr.add_binding('u', load_usb)
kr.add_binding('r', reload_pi)

if __name__ == '__main__':
    while True:
        time.sleep(0.01)
