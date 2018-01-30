from subprocess import call

TVSERVICE_PATH = '/opt/vc/bin/tvservice'
AMIXER_PATH = 'amixer'

commands = {}

commands['V:HDMI:16:9'] = [TVSERVICE_PATH, '-p']
commands['V:NTSC:4:3'] = [TVSERVICE_PATH, '-c', 'NTSC 4:3']
commands['V:NTSC:16:9'] = [TVSERVICE_PATH, '-c', 'NTSC 16:9']
commands['V:PAL:4:3'] = [TVSERVICE_PATH, '-c', 'PAL 4:3']
commands['V:PAL:16:9'] = [TVSERVICE_PATH, '-c', 'PAL 16:9']

commands['A:HDMI'] = [AMIXER_PATH, 'cset', 'numid=3', '2']
commands['A:ANALOG'] = [AMIXER_PATH, 'cset', 'numid=3', '1']

FBSET_8 = ['fbset', '-depth', '8']
FBSET_16 = ['fbset', '-depth', '16']

def set_video_output(mode, aspect= '16:9'):
    arg_str = 'V:' + mode.upper() + ':' + aspect
    command = commands[arg_str]
    call(command)
    call(FBSET_8)
    call(FBSET_16)
    
def set_audio_output(mode):
    arg_str = 'A' + ':' + mode.upper()
    command = commands[arg_str]
    call(command)

def set_audio_output_hdmi():
    set_audio_output('HDMI')

def set_audio_output_analog():
    set_audio_output('ANALOG')
