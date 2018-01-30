from omxplayer.player import OMXPlayer
import os

media_dir = '/home/multimedia/media'

class Player:

    def __init__(self, video_file):
        self.player = None
        self.load(video_file)

    def load(self, video_file):
        print('Player loading {0}'.format(video_file))
        #if self.player != None:
        #    self.player.stop()
        #    del self.player
        self.path = os.path.join(media_dir, video_file)
        if self.player is None:
            self.player = OMXPlayer(self.path, args=['--loop', '--blank', '-o', 'both'])
        else:
            self.player.load(self.path)
        self.player.stopEvent += lambda _: self._complete()
        self.player.pauseEvent += lambda _: self._pauseEvent()
        self.player.playEvent += lambda _: self._playEvent()
        self.player.positionEvent += lambda _: self._positionEvent()
        self.player.seekEvent += lambda _: self._seekEvent()

    def _complete(self):
        print('Playback finished.')
   
    def _pauseEvent(self):
        print('Player pause event.')
   
    def _playEvent(self):
        print('Player play event.')

    def _positionEvent(self):
        print('Player position event.')

    def _positionEvent(self):
        print('Player seek event.')

    def set_pause(self, p):
        if p:
            self.player.pause()
        else:
            self.player.play()

    def get_pause(self):
        if self.player.is_playing():
            return False
        else:
            return True

    def toggle_pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def stop(self):
        self.player.stop()

    def quit(self):
        self.player.quit()
