from flask import render_template, request, redirect, url_for, jsonify
from app import *
from werkzeug.utils import secure_filename
import mediamanager
from playercontroller import PlayerController
import outputmanager
import idmanager
import keyboard
import time
import os
from subprocess import call
import threading

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

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    name = idmanager.get_id()
    media_files = manager.get_media_files()
    current_default_file = manager.get_playlist()[0]
    pause_state = player_controller.get_pause()
    return render_template('index.html', name=name, media_files=media_files, current_default_file=current_default_file, pause_state=pause_state)

@app.route('/files', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file found.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Non selected file.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('upload_file', filename=filename))
            return redirect('/')
    return redirect('/')
    #return render_template('files.html', media_files=manager.get_media_files(), current_default_file=manager.get_playlist()[0])

@app.route('/control', methods=['GET', 'POST'])
def control():
    pause_state = player_controller.get_pause()
    print('Pause state = {0}'.format(pause_state))
    if request.method == 'POST':
        button = request.form['pausebutton']
        if button == 'pause':
            player_controller.set_pause(True)
        else:
            player_controller.set_pause(False)
        time.sleep(0.3)
        #pause_state = player_controller.get_pause()
        #return render_template('player.html', pause_state=pause_state)
        #redirect(request.url)
        return redirect('/')
    return redirect('/')
    #return render_template('player.html', pause_state=pause_state)

@app.route('/output', methods=['GET', 'POST'])
def output():
    if request.method == 'POST':
        video_output_mode = request.form['videomode']
        video_output_aspect = request.form['videoaspect']
        outputmanager.set_video_output(video_output_mode, video_output_aspect)
        #time.sleep(1.0)
        player_controller.reload(False)
    return redirect('/')
    #return render_template('output.html')

@app.route('/default', methods=['GET','POST'])
def default():
    if request.method == 'POST':
        default_file = request.form['default-button']
        print('Setting {0} as default.'.format(default_file))
        manager.set_playlist([default_file])
    return redirect('/')

@app.route('/load', methods=['GET', 'POST'])
def load():
    if request.method == 'POST':
        print('Loading {0}'.format(request.form['playnow-button']))
        file_to_load = request.form['playnow-button']
        player_controller.load(file_to_load)
    return redirect('/')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        file_to_delete = request.form['delete-button']
        print('Deleting {0}'.format(file_to_delete))
        manager.delete_file(file_to_delete)
    return redirect('/')

@app.route('/rename', methods=['GET', 'POST'])
def rename():
    if request.method == 'POST':
        name = request.form['id']
        print('Setting id to {0}'.format(name))
        idmanager.set_id(name)
    return redirect('/')

def shutdown():
    time.sleep(1.0)
    call(['sudo','shutdown','-r', 'now'])

@app.route('/reboot', methods=['GET', 'POST'])
def reboot():
    if request.method == 'POST':
        t = threading.Thread(target=shutdown)
        t.start()
    return redirect('/')

@app.route('/reload', methods=['GET', 'POST'])
def reload():
    if request.method == 'POST':
        player_controller.reload()
    return redirect('/')
