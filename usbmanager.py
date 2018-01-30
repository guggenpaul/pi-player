import os
import functools
import pyinotify

usb_path = '/media'

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

def usb_create(path):
    print('{0} created.'.format(path))

def usb_delete(path):
    print('{0} deleted.'.format(path))

class EventHander(pyinotify.ProcessEvent):

    def __init__(self, create_callback, delete_callback):
        self.create_callback = create_callback
        self.delete_callback = delete_callback

    def process_IN_CREATE(self, event):
        self.create_callback(event.pathname)

    def process_IN_DELETE(self, event):
        self.delete_callback(event.pathname)

def start():
    pass

def stop():
    pass

notifier = pyinotify.ThreadedNotifier(wm, EventHander(usb_create, usb_delete))
notifier.start()
wdd = wm.add_watch(usb_path, mask)
