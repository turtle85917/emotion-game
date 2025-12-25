import random
from ursina import camera, Entity, sequence, time, Vec2, window
from sfxManager import sfxManager

class Snowflake(Entity):
  def __init__(self):
    super().__init__(
      model="quad",
      scale=0.03,
      texture="assets/textures/snowflake.png",
      parent=camera.ui
    )
    self.alpha = random.uniform(0.4, 0.6)
    self.gravity = random.uniform(-0.001, -0.03) # default: -0.015
    self.initialX = random.uniform(-window.aspect_ratio / 2, window.aspect_ratio / 2)
    self._initAttr()
    self.loopSeq = sequence.Sequence(
      sequence.Wait(0.1),
      sequence.Func(self._initAttr)
    )
    self.loopSeq.unscaled = False
    self.loopSeq.ignore_paused = False
    self.waited = False
    self.speical = False

  def update(self):
    if self.waited: return

    self.velocity.y += self.gravity * time.dt
    self.position += self.velocity * time.dt

    if self.speical:
      self.rotation_z += 20 * time.dt

    if self.position.y <= -0.6:
      self.waited = True
      self.loopSeq.start()

  def _initAttr(self):
    self.waited = False
    self.position = Vec2(self.initialX, 0.515)
    self.velocity = Vec2(random.uniform(-0.01, 0.01), 0)
    if random.randint(0, 99) == 0:
      self.scale = 0.05
      self.speical = True
      self.texture = "assets/textures/special snowflake.png"
      sfxManager.playEffect("special")
    else:
      self.scale = 0.03
      self.rotation.x = 0
      self.speical = False
      self.texture = "assets/textures/snowflake.png"

def spawnSnowflakes(count:int)->None:
  for _ in range(count):
    Snowflake()
