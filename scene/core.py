from ursina import *

class Scene(Entity):
  def __init__(self, sceneName):
    super().__init__(enabled=False)

    self.tag = sceneName

  def addChild(self, entity:Entity):
    entity.parent = self

  def update(self): pass
