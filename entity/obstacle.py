from ursina import Entity
from utils import emotions

class Obstacle:
  def __init__(self, index:int, emt:int):
    z = index * 10 + 10
    self.entity = Entity(
      model="cube",
      texture="assets/textures/bricks.png",
      scale=(5, 3, 0.2),
      collider="box"
    )
    self.entity.position = (0, 1.5, z)
    self._emotionEntity = Entity(
      model="plane",
      texture=f"assets/players/{emotions[emt]}",
      scale=(1.5, 1, 1.5)
    )
    self._emotionEntity.position = (0, 1.5, z - 0.11)
    self._emotionEntity.rotation = (-90, 0, 0)
