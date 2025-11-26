import random
from ursina import color, destroy, Entity, invoke, Vec3, time
from utils import confettiGravity

class Confetti(Entity):
  def __init__(self, startPos):
    super().__init__(
      model="quad",
      texture="white_cube",
      scale=.12,
      color=color.rgb(random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)),
      position=startPos,
      billboard=True
    )
    self.startPos = startPos
    self.rotation = Vec3(
      random.uniform(-270, 270),
      0,
      random.uniform(-90, 90)
    )
    self.velocity = Vec3(
      random.uniform(-2, 2),
      random.uniform(3, 6),
      random.uniform(-1, 1)
    )

  def update(self):
    self.velocity.y += confettiGravity * time.dt
    self.position += self.velocity * time.dt
    self.rotation_z += random.uniform(100, 200) * time.dt

    if self.y < self.startPos.y - 4:
      destroy(self)

def spawnConfetti(startPosition, count=30):
  for _ in range(count):
    Confetti(startPosition)
