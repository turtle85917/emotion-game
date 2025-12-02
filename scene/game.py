from ursina import *
from scene.core import Scene
from entity import confetti, obstacle
from utils import emotions

# environment
speed = 3
friction = 4

class GameScene(Scene):
  def __init__(self):
    super().__init__("game")

    # entities
    camera.position = (8, 7, -17)
    camera.rotation = (23, -37, 0)

    self.ground = Entity(model="cube", color=color.azure, texture="assets/textures/grass.png", scale=(5, 0.3, 80))
    self.ground.position = (0, -0.15, 30)
    self.ground.texture_scale = (1, 10)
    self.addChild(self.ground)

    self.obstacles:list[obstacle.Obstacle] = []
    self.emotionsInObstacle:list[int] = []
    obstacleCount = 5
    for i in range(obstacleCount):
      pickupEmt = lambda: random.randint(0, len(emotions) - 1)
      emt = pickupEmt()
      while any(emt == x for x in self.emotionsInObstacle):
        emt = pickupEmt()
      self.obstacles.append(obstacle.Obstacle(i, emt))
      self.emotionsInObstacle.append(emt)
      self.addChild(self.obstacles[-1])

    self.player = Entity(
      model="plane",
      texture="assets/players/neutral.png",
      scale=(1.5, 1, 1.5),
      collider="sphere"
    )
    self.player.position = (0, 1.5, -3)
    self.player.rotation = (-90, 0, 0)
    self.addChild(self.player)

    # variable
    self.delta = 0
    self.playerLv = 0
    self.obstacleLv = 0
    self.knockbackVelocity = 0

    self.gameClear = False

    self.prevCollision = False
    self.ignoreCollision = False

  def update(self):
    if not self.gameClear:
      delta = time.dt * speed

      if self.knockbackVelocity != 0:
        delta += self.knockbackVelocity * time.dt
        self.knockbackVelocity = min(0, self.knockbackVelocity + friction * time.dt)

      camera.z += delta
      self.player.z += delta

    if not self.gameClear and self.obstacleLv == len(self.obstacles) and camera.z >= 52.:
      self.gameClear = True
      confetti.spawnConfetti(self.player.position, 300)
      # invoke(self.showClearUI, delay=1)

    hit = self.player.intersects()
    if hit.hit and not self.prevCollision and any(hit.entity == x.entity for x in self.obstacles):
      self.prevCollision = True
      if not self.ignoreCollision and self.playerLv != self.emotionsInObstacle[self.obstacleLv]:
        self.knockbackVelocity = -10
        self.prevCollision = False
      elif not self.ignoreCollision:
        self.ignoreCollision = True
    if not hit.hit and self.prevCollision and self.ignoreCollision:
      self.obstacleLv += 1
      self.prevCollision = False
      self.ignoreCollision = False
