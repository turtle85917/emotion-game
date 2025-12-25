from ursina import Entity
from utils import emotions

class Obstacle:
  def __init__(self, index:int, emt:int):
    self.entity = Entity(
      model="cube",
      texture="textures/bricks.png",
      scale=(5, 3, 0.2),
      collider="box"
    )
    self.entity.position = (0, 1.5, index * 30 + 10)
    self._emotionEntity = Entity(
      model="plane",
      texture=f"players/{emotions[emt]}",
      scale=(0.3, 0.3, 0.5)
    )
    self._emotionEntity.parent = self.entity
    self._emotionEntity.position = (0, 0, -0.51)
    self._emotionEntity.rotation = (-90, 0, 0)

  def updateEmotion(self, emt:int):
    self._emotionEntity.texture = f"players/{emotions[emt]}"
