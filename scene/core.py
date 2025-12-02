from ursina import *

class Scene(Entity):
  def __init__(self, sceneName):
    super().__init__(enabled=False)

    self.tag = sceneName
    self.manager = None
    self.ui = Entity(parent=camera.ui, enabled=False)

  def addChild(self, entity:Entity):
    entity.parent = self
  def addChildInUI(self, entity:Entity):
    entity.parent = self.ui

  def enableUI(self, flag:bool):
    self.ui.enabled = flag

  def update(self): pass
