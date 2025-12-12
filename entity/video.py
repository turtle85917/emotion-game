import cv2
import keras
import joblib
import numpy
import time
import threading
from ursina import *
from PIL import Image
from panda3d.core import Texture as PandaTexture
from mediapipe.python.solutions import face_detection, face_mesh

FACEMESH_LIPS_IDX = [0, 267, 269, 270, 13, 14, 17, 402, 146, 405, 409, 415, 291, 37, 39, 40, 178, 308, 181, 310, 311, 312, 185, 314, 317, 318, 61, 191, 321, 324, 78, 80, 81, 82, 84, 87, 88, 91, 95, 375]
FACEMESH_LEFT_EYE_IDX = [384, 385, 386, 387, 388, 390, 263, 362, 398, 466, 373, 374, 249, 380, 381, 382]
FACEMESH_LEFT_EYEBROW_IDX = [293, 295, 296, 300, 334, 336, 276, 282, 283, 285]
FACEMESH_RIGHT_EYE_IDX = [160, 33, 161, 163, 133, 7, 173, 144, 145, 246, 153, 154, 155, 157, 158, 159]
FACEMESH_RIGHT_EYEBROW_IDX = [65, 66, 70, 105, 107, 46, 52, 53, 55, 63]
FACEMESH_NOSE_IDX = [1, 2, 4, 5, 6, 19, 275, 278, 294, 168, 45, 48, 440, 64, 195, 197, 326, 327, 344, 220, 94, 97, 98, 115]

class Video(Entity):
  def __init__(self):
    super().__init__(
      model="quad",
      scale=(0.4, 0.3),
      origin=(-0.5, 0.5),
      position=window.top_left + Vec2(0.03, -0.03),
      enabled=False
    )

    self._faceMesh = face_mesh.FaceMesh(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5
    )
    self._faceDetection = face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    self._scaler = joblib.load("assets/ai/scaler.pkl")
    self._classficationModel = keras.models.load_model("assets/ai/emotion_classification.keras")

    self.emotion = -1

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
      if not self.enabled: continue
      ret, img = self.cap.read()

      if not ret: continue

      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      img = cv2.flip(img, 1)
      faceResult = self._faceMesh.process(img)
      faceDetectionResult = self._faceDetection.process(img)
      img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

      if faceResult.multi_face_landmarks is None: continue
      if faceDetectionResult.detections is None: continue
      if len(faceDetectionResult.detections) == 0: continue

      faceLandmarks = faceResult.multi_face_landmarks[0]
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

      positions = self._getModelInput(faceLandmarks.landmark)
      p = numpy.array(positions).reshape((116, 3))
      center = p.mean(axis=0, keepdims=True)
      p = (p - center).reshape((348,))
      p = self._scaler.transform([p])[0]
      p = p.reshape((1, 116, 3))
      pred = self._classficationModel.predict(p, verbose=0)
      predZip = [(pred[0][i], i) for i in range(len(pred[0]))]
      self.emotion = max(predZip)[1]

      time.sleep(0.03)

  def _pickUpSpecificPointsInFace(self, face:any, indices:list[int])->list[tuple[int]]:
    return [(face[i].x, face[i].y, face[i].z) for i in indices]
  def _getModelInput(self, face:any)->list[float]:
    indices = [
      *self._pickUpSpecificPointsInFace(face, FACEMESH_LIPS_IDX),
      *self._pickUpSpecificPointsInFace(face, FACEMESH_LEFT_EYE_IDX),
      *self._pickUpSpecificPointsInFace(face, FACEMESH_LEFT_EYEBROW_IDX),
      *self._pickUpSpecificPointsInFace(face, FACEMESH_RIGHT_EYE_IDX),
      *self._pickUpSpecificPointsInFace(face, FACEMESH_RIGHT_EYEBROW_IDX),
      *self._pickUpSpecificPointsInFace(face, FACEMESH_NOSE_IDX),
    ]
    res = []
    for item in indices:
      res.extend(list(item))
    return res
  def _getRealPoint(self, x:float, base:int)->int:
    return math.floor(x * base)
