from ursina import *
from scene.core import Scene

class MainScene(Scene):
  def __init__(self):
    super().__init__("main")

    self.title = Text(
      "동아리 프로젝트",
      scale=4,
      color=color.black,
      origin=(0, 0),
      position=(0, 0.2)
    )
    self.addChildInUI(self.title)

    self.description = Text(
      "얼굴 인식 모델을 만들며 CNN을 공부하기",
      scale=2,
      color=color.white,
      origin=(0, 0),
      position=(0, 0.1)
    )
    self.addChildInUI(self.description)

    sky = Sky(texture="assets/textures/sky.jpg")
    self.addChild(sky)

    self.startButton = Button(
      "게임 시작하기",
      scale=(0.2, 0.1),
      origin=(0, 0),
      position=(0, -0.3)
    )
    self.startButton.on_click = self._onStartButtonClick
    self.addChildInUI(self.startButton)

  def onChangeScene(self):
    camera.rotation = (23, -37, 0)
    camera.fov = 40

  def _onStartButtonClick(self):
    self.manager.changeScene("game")
