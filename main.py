import mediapipe # code for solving DLL error
from ursina import *
from scene.manager import SceneManager
from scene.main import MainScene
from scene.game import GameScene
from entity.snow import spawnSnowflakes
from sfxManager import sfxManager

app = Ursina()

Text.default_font = "assets/fonts/MemomentKkukkukk.ttf"

sceneManager = SceneManager()
sceneManager.newScene(MainScene())
sceneManager.newScene(GameScene())

sfxManager.newEffect("start", "assets/sfx/start.mp3")
sfxManager.newEffect("click", "assets/sfx/click.mp3")
sfxManager.newEffect("special", "assets/sfx/special.mp3")
sfxManager.newEffect("knockback", "assets/sfx/knockback.mp3")
sfxManager.newEffect("clear", "assets/sfx/clear.mp3")
sfxManager.newEffect("clear2", "assets/sfx/clear2.mp3")

sceneManager.changeScene("main")

# ❄️ snow!
spawnSnowflakes(30)

if __name__ == "__main__":
  app.run()
