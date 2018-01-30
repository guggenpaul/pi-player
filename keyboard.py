from evdev import InputDevice, categorize, ecodes
import threading
import time

class KeyboardReader:

    def __init__(self):
        self.bindings = []
        self.events = []
        self.connected = False
        self._connect()
        self.thread = threading.Thread(target=self._poll_keyboard)
        self.daemon = True
        self.running = False
        self.start()
        self.catch_all = None

    def _connect(self):
        try:
            self.keyboard = InputDevice('/dev/input/event0')
            print('Keyboard connected.')
            self.connected = True
        except (FileNotFoundError, PermissionError):
            self.keyboard = None;
            self.connected = False

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def is_connected(self):
        return self.connected

    def get_events(self):
        return self.events

    def add_binding(self, key, callback):
        self.bindings.append({'key':key,'callback':callback})

    def add_catch_all(self, callback):
        self.catch_all = callback

    def _key_pressed(self, key):
        for b in self.bindings:
            if b['key'] == key:
                b['callback'](key)
        if self.catch_all is not None:
            self.catch_all(key)

    def _poll_keyboard(self):
        while self.running:
            if self.connected:
                try:
                    event = self.keyboard.read_one()
                    if event != None:
                        if event.type == ecodes.EV_KEY:
                            #self.events.append(event)
                            #iprint(categorize(event))
                            c = categorize(event)
                            if c.keystate == 1:
                                char = c.keycode.split('_')[1].lower()
                                #print('{0} pressed'.format(char))
                                self._key_pressed(char)
                except OSError:
                    self.keyboard = None
                    print('Keyboard disconnected.')
                    self.connected = False
            else:
                self._connect()
                time.sleep(0.01)
