import os
from os.path import isfile, join
import json
import copy

accepted_media_types = ('.mp4','.mov','.mpg','.mpeg','.m4v','.mkv','.avi', '.vob', '.MP4', '.MOV', 'MPG', 'MPEG', '.M4V', '.MKV', '.AVI', '.VOB')
playlist_file = 'playlist.json'
blank_json = {'playlist':[]}

class MediaDirectoryManager:

    def __init__(self, directory=None):
        self.directory = directory

    def set_directory(self, directory):
        self.directory = directory

    def _list_directory(self, accepted=False):
        files = []
        for file in os.listdir(self.directory):
            if accepted:
                if file.endswith(accepted_media_types):
                    files.append(file)
            else:
                files.append(file)
        return files

    def get_media_files(self):
        return self._list_directory(True)

    def get_all_files(self):
        return self._list_directory(False)

    def get_playlist(self):
        json_filename = os.path.join(self.directory, playlist_file)
        json_obj = json.load(open(json_filename))
        playlist = json_obj['playlist']
        return playlist

    def set_playlist(self, playlist):
        new_json = copy.copy(blank_json)
        new_json['playlist'] = playlist
        json_filename = os.path.join(self.directory, playlist_file)
        with open(json_filename, 'w') as output_file:
            json.dump(new_json, output_file)

    def delete_file(self, file):
        os.remove(os.path.join(self.directory, file))
