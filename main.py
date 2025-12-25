import mediapipe # code for solving DLL error
from ursina import *
from scene.manager import SceneManager
from scene.main import MainScene
from scene.game import GameScene

app = Ursina()

Text.default_font = "assets/fonts/MemomentKkukkukk.ttf"

sceneManager = SceneManager()
sceneManager.newScene(MainScene())
sceneManager.newScene(GameScene())

sceneManager.changeScene("main")

if __name__ == "__main__":
  app.run()
