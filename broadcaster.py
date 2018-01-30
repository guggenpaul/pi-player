import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def main():
    while True:
        f = open('/home/multimedia/id.txt')
        identity = f.readline().strip()
        sock.sendto(identity.encode('ascii'), ('255.255.255.255', 9955))
        time.sleep(10.0)

if __name__ == '__main__':
    main()

