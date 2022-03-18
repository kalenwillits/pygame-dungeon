import os

from pygame import mixer

from core.node import Node


class Sound(Node):
    source: str = None
    content: mixer.Sound = None
    repeat: int = None
    fade: float = None

    def fit(self):
        self.content = mixer.Sound(os.path.join(*self.source.split('/')))
        self.initattr('repeat', self.get_root().settings.sound.repeat)
        self.volume = self.kwargs.get('volume', self.get_root().settings.sound.volume)
        self.initattr('fade', self.get_root().settings.sound.fade)
        self.set_volume(self, self.volume)
        super().fit()

    def play(self):
        self.content.play(self.repeat)

    def stop(self):
        self.content.stop()

    def pause(self):
        self.content.pause()

    def unpause(self):
        self.content.unpause()

    def fadeout(self):
        self.content.fadeout(self.fade)

    @property
    def volume(self) -> float:
        return self.content.get_volume()

    @volume.setter
    def volume(self, volume: float):
        self.content.set_volume(volume)
