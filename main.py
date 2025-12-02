from ursina import *
from scene.manager import SceneManager
from scene.game import GameScene

app = Ursina()
Sky(texture="assets/textures/sky.jpg")

sceneManager = SceneManager()
sceneManager.newScene(GameScene())

sceneManager.changeScene("game")

Text.default_font = "assets/fonts/MemomentKkukkukk.ttf"

if __name__ == "__main__":
  app.run()
