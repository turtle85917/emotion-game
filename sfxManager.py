from ursina import *

class SfxManager:
  def __init__(self):
    self.effects:dict[str, Audio] = {}
    self.volume = 0.45

  def newEffect(self, name:str, path:str):
    self.effects[name] = Audio(path, self.volume, loop=False, autoplay=False)

  def playEffect(self, name:str):
    if name not in self.effects.keys(): return
    self.effects[name].stop(False)
    self.effects[name].play()

sfxManager = SfxManager()
