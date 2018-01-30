from flask import Flask

UPLOAD_FOLDER = '/home/multimedia/media'
ALLOWED_EXTENSIONS = set(['mp4', 'mov', 'm4v', 'mkv', 'mpg', 'mpeg', 'mp3', 'avi'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER    
from app import views
