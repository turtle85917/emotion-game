from ursina import *
from panda3d.core import NodePath, Camera as PandaCamera, OrthographicLens
from scene.core import Scene
from entity import confetti, obstacle
from entity.video import Video
from sfxManager import sfxManager
from utils import emotions

# environment
speed = 12
friction = 10
knockback = -26
obstacleCount = 5

class GameScene(Scene):
  def __init__(self):
    super().__init__("game")

    # clear ui
    self.clearUi = Entity(enabled=False)
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
    self.uiRestartButton.on_click = lambda: self._resetGame()
    self.uiRestartButton.parent = self.clearUi
    self.addChildInUI(self.clearUi)

    # entities
    self.ground = Entity(
      model="cube",
      color=color.white,
      texture="textures/tile.png",
      scale=(5, 0.3, 200)
    )
    self.ground.position = (0, -0.15, 90)
    self.ground.texture_scale = (0.5, 20)
    self.addChild(self.ground)
    groundSide = Entity(
      model="quad",
      color=color.rgb32 (189, 194, 207),
      scale=(200, 0.3),
      position=(2.51, -0.15, 90),
      rotation=(0, 90, 0)
    )
    groundSide.double_sided = True
    self.addChild(groundSide)

    self.obstacles:list[obstacle.Obstacle] = []
    self.emotionsInObstacle:list[int] = []
    for i in range(obstacleCount):
      pickupEmt = lambda: random.randint(0, len(emotions) - 1)
      emt = pickupEmt()
      while any(emt == x for x in self.emotionsInObstacle):
        emt = pickupEmt()
      self.obstacles.append(obstacle.Obstacle(i, emt))
      self.emotionsInObstacle.append(emt)
      self.addChild(self.obstacles[-1].entity)

    self.player = Entity(
      model="plane",
      texture="players/neutral.png",
      scale=(1.5, 1, 1.5),
      collider="sphere"
    )
    self.player.position = (0, 1.5, -10)
    self.player.rotation = (-90, 0, 0)
    self.addChild(self.player)

    # video setting
    self.video = Video()
    self.video.enabled = False

    bgRegion = camera.display_region.get_window().make_display_region()
    bgRegion.setSort(-20)

    bgRender = NodePath("bg_render")
    bgCamNode = PandaCamera("bg_camera")
    bgLens = OrthographicLens()

    bgLens.set_film_size(2 * window.aspect_ratio, 2)
    bgLens.set_near_far(-1000, 1000)

    bgCamNode.set_lens(bgLens)
    bgCamera = bgRender.attach_new_node(bgCamNode)

    bgRegion.set_camera(bgCamera)
    bgRender.set_depth_test(False)
    bgRender.set_depth_write(False)

    self.video.reparent_to(bgCamera)
    # end

    # variable
    self.delta = 0
    self.playerLv = 0
    self.obstacleLv = 0
    self.knockbackVelocity = 0

    self.gameClear = False

    self.prevCollision = False
    self.ignoreCollision = False

  def onChangeScene(self):
    self.video.enabled = True
    camera.position = (9.8, 4.6, -19.7)
    camera.rotation = (6.2, -32, 0)
  def update(self):
    if not self.gameClear:
      delta = time.dt * speed

      self.playerLv = self.video.emotion
      self.player.texture = f"players/{emotions[self.video.emotion]}.png"

      if self.knockbackVelocity != 0:
        delta += self.knockbackVelocity * time.dt
        self.knockbackVelocity = min(0, self.knockbackVelocity + friction * time.dt)

      camera.z += delta
      self.player.z += delta

    if not self.gameClear and camera.z >= 165:
      self.gameClear = True
      sfxManager.playEffect("clear")
      sfxManager.playEffect("clear2")
      confetti.spawnConfetti(self.player.position, 300)
      self.clearUi.enabled = True

    hit = self.player.intersects()
    if hit.hit and not self.prevCollision and any(hit.entity == x.entity for x in self.obstacles):
      self.prevCollision = True
      if not self.ignoreCollision and self.playerLv != self.emotionsInObstacle[self.obstacleLv]:
        self.knockbackVelocity = knockback
        self.prevCollision = False
        self.shake(duration=0.4, magnitude=3)
        sfxManager.playEffect("knockback")
      elif not self.ignoreCollision:
        self.ignoreCollision = True
    if not hit.hit and self.prevCollision and self.ignoreCollision:
      self.obstacleLv += 1
      self.prevCollision = False
      self.ignoreCollision = False

  def _resetGame(self):
    sfxManager.playEffect("click")

    camera.position = (9.8, 4.6, -19.7)
    camera.rotation = (6.2, -32, 0)

    self.player.position = (0, 1.5, -3)
    self.player.rotation = (-90, 0, 0)

    self.clearUi.enabled = False

    self.emotionsInObstacle = []
    for i in range(obstacleCount):
      pickupEmt = lambda: random.randint(0, len(emotions) - 1)
      emt = pickupEmt()
      while any(emt == x for x in self.emotionsInObstacle):
        emt = pickupEmt()
      self.obstacles[i].updateEmotion(emt)
      self.emotionsInObstacle.append(emt)

    # variable
    self.delta = 0
    self.playerLv = 0
    self.obstacleLv = 0
    self.knockbackVelocity = 0

    self.gameClear = False

    self.prevCollision = False
    self.ignoreCollision = False
