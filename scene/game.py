from ursina import *
from scene.core import Scene
from entity import confetti, obstacle
from utils import emotions

# environment
speed = 15
friction = 4

class GameScene(Scene):
  def __init__(self):
    super().__init__("game")

    # clear ui
    self.clearUi = Entity(enabled=False, parent=camera.ui)
    self.uiTitle = Text(
      "축하합니다!",
      scale=3,
      origin=(0, 0),
      position=(0, 0)
    )
    self.uiTitle.parent = self.clearUi
    self.uiRestartButton = Button(
      "다시 하기",
      scale=(0.2, 0.1),
      origin=(0, 0),
      position=(0, -0.2)
    )
    self.uiRestartButton.parent = self.clearUi

    self.uiSubTitles = [
      Text("멋진 플레이", scale=1.3, origin=(0, 0), position=(-0.2, 0.08), rotation=(0, 0, -30)),
      Text("훌룡하다!", scale=1.3, origin=(0, 0), position=(0.25, 0.06), rotation=(0, 0, 20)),
    ]
    destRot = [-10, 40]
    for i in range(len(self.uiSubTitles)):
      sub = self.uiSubTitles[i]
      sub.parent = self.clearUi
      sub.animate_rotation((0, 0, destRot[i]), duration=0.5, loop=True, curve=curve.sin)
      sub.animate_scale(1.6, duration=0.5, loop=True, curve=curve.out_bounce)
      # invoke(sub.animate_scale, 1.6, duration=0.5, loop=True, curve=curve.out_bounce, delay=1000)

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
      self.addChild(self.obstacles[-1].entity)
    self.emotionsInObstacle = [0, 0, 0, 0, 0]

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
      self.clearUi.enabled = True

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
