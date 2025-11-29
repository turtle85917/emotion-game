import cv2
import threading
import time
from ursina import *
from PIL import Image
from panda3d.core import Texture as PandaTexture

class Video(Entity):
  def __init__(self):
    super().__init__(
      parent=camera.ui,
      model="quad",
      scale=(0.4, 0.3),
      origin=(-0.5, 0.5),
      position=window.top_left + Vec2(0.03, -0.03)
    )

    self.cap = cv2.VideoCapture(0)
    _, img = self.cap.read()
    img = self._frameToImg(img)

    self.pandaTexture = PandaTexture()
    self.pandaTexture.setup2dTexture(
      640, 480,
      PandaTexture.T_unsigned_byte,
      PandaTexture.F_rgb
    )
    self.pandaTexture.setRamImage(img.tobytes())
    self.texture = Texture(self.pandaTexture)

    threading.Thread(target=self._render, daemon=True).start()

  def _render(self):
    while True:
      ret, img = self.cap.read()

      if not ret: continue

      img = self._frameToImg(img)
      self.pandaTexture.setRamImage(img.tobytes())
      self.texture._texture = self.pandaTexture

      time.sleep(0.03)

  def _frameToImg(self, frame):
    # f = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # wtf?
    f = cv2.flip(frame, 0)
    f = cv2.flip(f, 1)
    img = Image.fromarray(f)
    return img
