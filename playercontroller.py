import socket
import threading
import time

DEFAULT_PLAYER_PORT = 13131

class PlayerController:

    def __init__(self, player_host='0.0.0.0', player_port=DEFAULT_PLAYER_PORT):
        self.player_host = player_host
        self.player_port = player_port
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = '0.0.0.0'
        self.port = self.player_port + 1
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock.bind((self.host, self.port))
        self.t = threading.Thread(target=self._wait_for_message)
        self.t.start()
        self.player_pause_state = False
        self.get_pause()

    def __del__(self):
        print('Player controller closing socket...')
        self.recv_sock.close()

    def _send_msg(self, msg):
        #print('Sending control message - {0}'.format(msg))
        self.send_sock.sendto(msg.encode(), (self.player_host, self.player_port))

    def _wait_for_message(self):
        while True:
            msg = self.recv_sock.recv(1024)
            #print('Echoing message {0}'.format(msg.decode()))
            #self._send_msg(msg.decode())
            self._parse_message(msg.decode())

    def _parse_message(self, msg):
        if 'pause:' in msg:
            state = msg.split(':')[1]
            if state == 'true':
                self.player_pause_state = True
            if state == 'false':
                self.player_pause_state = False
            #print('Player pause state = {0}'.format(self.player_pause_state))
    
    def set_pause(self, p):
        msg = 'pause:'
        if p:
            msg += 'true'
        else:
            msg += 'false'
        self._send_msg(msg)

    def _get_pause(self):
        msg = 'pause:get'
        self._send_msg(msg)

    def get_pause(self):
        return self.player_pause_state

    def toggle_pause(self):
        msg = 'pause:toggle'
        self._send_msg(msg)

    def load(self, file):
        msg = 'load:' + file
        self._send_msg(msg)

    def reload(self, default=True):
        if default:
            msg = 'rel:true'
        else:
            msg = 'rel:false'
        self._send_msg(msg)

if __name__ == '__main__':
    pc = PlayerController()
    while True:
        time.sleep(0.1)
        
