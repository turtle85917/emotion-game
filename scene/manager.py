from scene.core import Scene

class SceneManager():
  def __init__(self):
    self.scenes:list[Scene] = []
    self.currentSceneName:str|None = None

  def newScene(self, scene:Scene):
    self.scenes.append(scene)
  def changeScene(self, sceneName:str):
    newScene:Scene = list(filter(lambda x: x.tag == sceneName, self.scenes))[0]
    currScene:Scene = list(filter(lambda x: x.tag == self.currentSceneName, self.scenes))[0] if self.currentSceneName != None else None
    if currScene != None and newScene.tag == currScene.tag: return
    if currScene != None: currScene.enabled = False
    newScene.enabled = True
    self.currentSceneName = newScene.tag
