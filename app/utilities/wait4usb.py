import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()

def callback_function(*args):
    print('Received something ... ', args)

iface = 'org.freedesktop.DBus.ObjectManager'
signal = 'InterfacesAdded'
bus.add_signal_receiver(callback_function, signal, iface)

from gi.repository import GObject as gobject
loop = gobject.MainLoop()
loop.run()
