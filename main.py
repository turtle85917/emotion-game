from ursina import *

app = Ursina()

camera.position = (8, 7, -17)
camera.rotation = (23, -37, 0)

ground = Entity(model="cube", color=color.azure, texture="assets/textures/grass.png", scale=(5, 0.3, 80))
ground.position = (0, -0.15, 30)
ground.texture_scale = (1, 10)

obstacles:list[Entity] = []
obstacleCount = 5
for i in range(obstacleCount):
  obstacles.append(Entity(
    model="cube",
    texture="assets/textures/bricks.png",
    scale=(5, 3, 0.2),
    collider="box"
  ))
  obstacles[-1].position = (0, 1.5, i * 10 + 10)

def update():
  camera.z += time.dt * 3

if __name__ == "__main__":
  app.run()
