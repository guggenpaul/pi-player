def get_id():
    try:
        f = open('/home/multimedia/piplayer/id.txt')
        name = f.readline()
        f.close()
        return name.strip()
    except FileNotFoundError:
        return 'none'

def set_id(i):
    f = open('/home/multimedia/piplayer/id.txt', 'w+')
    f.write(i)
    f.close()
