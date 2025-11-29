import random
from ursina import *
from entity import obstacle, confetti, video
from utils import emotions

app = Ursina()

# environment
speed = 3
friction = 4
knockbackVelocity = 0

Text.default_font = "assets/fonts/MemomentKkukkukk.ttf"

camera.position = (8, 7, -17)
camera.rotation = (23, -37, 0)

ground = Entity(model="cube", color=color.azure, texture="assets/textures/grass.png", scale=(5, 0.3, 80))
ground.position = (0, -0.15, 30)
ground.texture_scale = (1, 10)

obstacles:list[obstacle.Obstacle] = []
emotionsInObstacle:list[int] = []
obstacleCount = 5
for i in range(obstacleCount):
  pickupEmt = lambda: random.randint(0, len(emotions) - 1)
  emt = pickupEmt()
  while any(emt == x for x in emotionsInObstacle):
    emt = pickupEmt()
  obstacles.append(obstacle.Obstacle(i, emt))
  emotionsInObstacle.append(emt)

player = Entity(
  model="plane",
  texture="assets/players/neutral.png",
  scale=(1.5, 1, 1.5),
  collider="sphere"
)
player.position = (0, 1.5, -3)
player.rotation = (-90, 0, 0)

# post process
video.Video()
Sky(texture="assets/textures/sky.jpg")

# variable
delta = 0
playerLv = 0
obstacleLv = 0

gameClear = False

prevCollision = False
ignoreCollision = False

def showClearUI():
  Text(
    "GAME CLEAR",
    scale=4,
    color=color.black,
    origin=(0, 0),
    position=(0, 0.2)
  )
  gameRestart = Button(
    "Restart",
    scale=(0.2, 0.1),
    origin=(0, 0),
    position=(0, -0.3)
  )

def update():
  global speed, friction, knockbackVelocity
  global delta, playerLv, obstacleLv, gameClear, prevCollision, ignoreCollision

  if not gameClear:
    delta = time.dt * speed

    if knockbackVelocity != 0:
      delta += knockbackVelocity * time.dt
      knockbackVelocity = min(0, knockbackVelocity + friction * time.dt)

    camera.z += delta
    player.z += delta

  if not gameClear and obstacleLv == len(obstacles) and camera.z >= 52.:
    gameClear = True
    confetti.spawnConfetti(player.position, 300)
    invoke(showClearUI, delay=1)

  hit = player.intersects()
  if hit.hit and not prevCollision and any(hit.entity == x.entity for x in obstacles):
    prevCollision = True
    if not ignoreCollision and playerLv != emotionsInObstacle[obstacleLv]:
      knockbackVelocity = -10
      prevCollision = False
    elif not ignoreCollision:
      ignoreCollision = True
  if not hit.hit and prevCollision and ignoreCollision:
    obstacleLv += 1
    prevCollision = False
    ignoreCollision = False

if __name__ == "__main__":
  app.run()
