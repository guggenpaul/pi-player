from picontrol.player import Player
import os
import json
import time
import pyinotify
import socket

LOAD_DELAY = 5.0
CMD_PORT = 13131

#Media and USB directory paths
media_path = os.environ['MEDIA_DIR']
usb_path = '/media'

#File extensions that player can load
valid_file_extensions = ('mp4', 'm4v', 'mkv', 'mov', 'mpg')

#The Player
player = None
b_playing = True

#Socket
cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cmd_sock.settimeout(0.1)
cmd_sock.bind(('0.0.0.0', CMD_PORT))

def check_socket():
    #print('Checking socket.')
    try:
        data = cmd_sock.recv(1024)
        print('Runner received message - {0}'.format(data.decode()))
        parse_message(data.decode())
    except socket.timeout:
        return

def parse_message(msg):
    if msg == 'stop':
        player.stop()
    if msg == 'pause:toggle':
        player.toggle_pause()
        send_pause_state()
    if msg == 'pause:true':
        player.set_pause(True)
        send_pause_state()
    if msg == 'pause:false':
        player.set_pause(False)
        send_pause_state()
    if msg == 'pause:get':
        send_pause_state()
    if 'load:' in msg:
        video_file = msg.split(':')[1]
        if video_file == 'USB==USB':
            load_file()
        else:
            player.load(video_file)
    if msg == 'reload':
        load_file()

def send_pause_state():
    state = player.get_pause()
    r_msg = 'pause:'
    if state:
        r_msg += 'true'
    else:
        r_msg += 'false'
    cmd_sock.sendto(r_msg.encode(), ('0.0.0.0', CMD_PORT +1))

def usb_create(path):
    print('{0} mounted.'.format(path))
    load_file() 

def usb_delete(path):
    print('{0} unmounted.'.format(path))
    load_file()

class EventHander(pyinotify.ProcessEvent):

    def __init__(self, create_callback, delete_callback):
        self.create_callback = create_callback
        self.delete_callback = delete_callback

    def process_IN_CREATE(self, event):
        self.create_callback(event.pathname)
        

    def process_IN_DELETE(self, event):
        self.delete_callback(event.pathname)

def load_from_json():
    global player
    json_file = os.path.join(media_path, 'playlist.json')
    with open(json_file) as playlist_file:
        playlist = json.load(playlist_file)
    file_to_play = playlist['playlist'][0]
    print('Playing {0} from playlist.'.format(file_to_play))
    player = Player(file_to_play)
    return True

def load_from_usb():
    global player
    dirs = os.listdir(usb_path)
    for d in dirs:
        drive_path = os.path.join(usb_path, d)
        try:
            files = os.listdir(drive_path)
            for f in files:
                if f.endswith(valid_file_extensions):
                    file_to_play = os.path.join(drive_path, f)
                    print('Playing {0} from usb.'.format(file_to_play))
                    player = Player(file_to_play)
                    return True
        except PermissionError:
            continue
        return False

def load_file():
    global player
    if player is not None:
        player.quit()
        del player
    if not load_from_usb():
        load_from_json()

def main():
    #wm = pyinotify.WatchManager()
    #mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE
    #notifier = pyinotify.ThreadedNotifier(wm, EventHander(usb_create, usb_delete))
    #notifier.start()
    #wdd = wm.add_watch(usb_path, mask)
    time.sleep(LOAD_DELAY)
    load_file()
    while(b_playing):
        time.sleep(0.1)
        check_socket()

if __name__ == '__main__':
    main()
