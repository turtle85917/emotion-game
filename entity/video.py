import cv2
import threading
import time
from ursina import *
from PIL import Image
from panda3d.core import Texture as PandaTexture
from mediapipe.python.solutions import face_detection

class Video(Entity):
  def __init__(self):
    super().__init__(
      parent=camera.ui,
      model="quad",
      scale=(0.4, 0.3),
      origin=(-0.5, 0.5),
      position=window.top_left + Vec2(0.03, -0.03)
    )

    self._faceDetection = face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    self.cap = cv2.VideoCapture(0)
    _, img = self.cap.read()
    img = cv2.flip(img, 0)
    img = cv2.flip(img, 1)

    self.pandaTexture = PandaTexture()
    self.pandaTexture.setup2dTexture(
      640, 480,
      PandaTexture.T_unsigned_byte,
      PandaTexture.F_rgb
    )
    self.pandaTexture.setRamImage(Image.fromarray(img).tobytes())
    self.texture = Texture(self.pandaTexture)

    threading.Thread(target=self._render, daemon=True).start()

  def _render(self):
    while True:
      ret, img = self.cap.read()

      if not ret: continue

      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      img = cv2.flip(img, 1)
      faceDetectionResult = self._faceDetection.process(img)
      img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

      if faceDetectionResult.detections is None: continue
      if len(faceDetectionResult.detections) == 0: continue

      oneOfFaceDetectionResult = faceDetectionResult.detections[0]
      box = oneOfFaceDetectionResult.location_data.relative_bounding_box
      cv2.rectangle(img,
        (self._getRealPoint(box.xmin, img.shape[1]), self._getRealPoint(box.ymin, img.shape[0])),
        (self._getRealPoint((box.xmin + box.width), img.shape[1]), self._getRealPoint((box.ymin + box.height), img.shape[0])),
        (0, 0, 255), 2
      )
      img = cv2.flip(img, 0)
      img = Image.fromarray(img)
      self.pandaTexture.setRamImage(img.tobytes())
      self.texture._texture = self.pandaTexture

      time.sleep(0.03)

  def _getRealPoint(self, x:float, base:int)->int:
    return math.floor(x * base)
