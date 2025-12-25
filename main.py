import mediapipe # code for solving DLL error
import sys
from panda3d.core import Filename, getModelPath
from ursina import *

application.asset_folder = Path(Path(".").resolve())/"assets" #Path(getattr(sys, "_MEIPASS", Path(".").resolve()))/"assets"

from pathlib import Path
from scene.manager import SceneManager
from scene.main import MainScene
from scene.game import GameScene
from sfxManager import sfxManager

app = Ursina()

# mp = getModelPath()
# mp.clear()
# mp.appendDirectory(Filename.fromOsSpecific(str(application.asset_folder)))

Text.default_font = Filename.fromOsSpecific(str(application.asset_folder/"fonts/MemomentKkukkukk.ttf")).get_fullpath()

sceneManager = SceneManager()
sceneManager.newScene(MainScene())
sceneManager.newScene(GameScene())

sfxManager.newEffect("start", "sfx/start.wav")
sfxManager.newEffect("click", "sfx/click.wav")
sfxManager.newEffect("special", "sfx/special.wav")
sfxManager.newEffect("knockback", "sfx/knockback.wav")
sfxManager.newEffect("clear", "sfx/clear.wav")
sfxManager.newEffect("clear2", "sfx/clear2.wav")

sceneManager.changeScene("main")

if __name__ == "__main__":
  app.run()
