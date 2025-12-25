import mediapipe # code for solving DLL error
from ursina import *
from scene.manager import SceneManager
from scene.main import MainScene
from scene.game import GameScene
from sfxManager import sfxManager

app = Ursina(development_mode=False)

window.borderless = False
window.fullscreen = True

Text.default_font = "assets/fonts/MemomentKkukkukk.ttf"

sceneManager = SceneManager()
sceneManager.newScene(MainScene())
sceneManager.newScene(GameScene())

# sfxManager.newEffect("start", "sfx/start.wav")
sfxManager.newEffect("click", "assets/sfx/click.wav")
sfxManager.newEffect("special", "assets/sfx/special.wav")
sfxManager.newEffect("knockback", "assets/sfx/knockback.wav")
sfxManager.newEffect("clear", "assets/sfx/clear.wav")
sfxManager.newEffect("clear2", "assets/sfx/clear2.wav")

sceneManager.changeScene("main")

if __name__ == "__main__":
  app.run()
