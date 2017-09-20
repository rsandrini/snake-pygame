from pygame.math import Vector2
from pygame.locals import *
import random
import pygame
import time


class Player:
    positions = []
    step = 32
    direction = 0
    score = 0

    def __init__(self, length):
        self.length = length - 1
        for i in range(0, length):
            self.positions.append(Vector2(self.positions[-1].x + self.step, self.step)
                                  if self.positions else Vector2(self.step, self.step))

    def get_next_position(self):
        if self.direction == 0:
            return Vector2(self.positions[-1].x + self.step, self.positions[-1].y)
        if self.direction == 1:
            return Vector2(self.positions[-1].x - self.step, self.positions[-1].y)
        if self.direction == 2:
            return Vector2(self.positions[-1].x, self.positions[-1].y - self.step)
        if self.direction == 3:
            return Vector2(self.positions[-1].x, self.positions[-1].y + self.step)

    def update(self):
        self.positions.pop(0)
        self.positions.append(self.get_next_position())

    def move_right(self):
        if self.direction == 1:
            return
        self.direction = 0

    def move_left(self):
        if self.direction == 0:
            return
        self.direction = 1

    def move_up(self):
        if self.direction == 3:
            return
        self.direction = 2

    def move_down(self):
        if self.direction == 2:
            return
        self.direction = 3

    def add_score(self, life_position):
        self.score += 1
        self.positions.append(life_position)

    def draw(self, surface, image):
        for position in self.positions:
            surface.blit(image, (position.x, position.y))


class App:

    windowWidth = 800
    windowHeight = 600
    game_over = False
    map_bounds = Vector2(768, 576)
    player = 0
    debug = False

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._image_life = None
        self._image_debug = None
        self._life_position = Vector2()
        self.player = Player(8)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight),
                                                     pygame.HWSURFACE)

        pygame.display.set_caption('Pygame snake')
        self._running = True
        self._image_surf = pygame.image.load("pygame.png").convert()
        self._image_life = pygame.image.load("pygame_life.png").convert()
        self._image_debug = pygame.image.load("pygame_debug.png").convert()
        self.new_life()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def new_life(self):
        self._life_position = Vector2(random.choice(range(self.player.step, int(self.map_bounds.x),
                                                          self.player.step)),
                                      random.choice(range(self.player.step, int(self.map_bounds.y),
                                                          self.player.step)))
        if self._life_position in self.player.positions:
            self.new_life()

    def draw_life(self, surface, image):
        surface.blit(image, (self._life_position.x, self._life_position.y))

    def draw_debug(self, surface, image):
        if self.debug:
            next = self.player.get_next_position()
            surface.blit(image, (next.x, next.y))

    def check_life_collision(self):
        if self.player.get_next_position() == self._life_position:
            self.player.add_score(self._life_position)
            self.new_life()
        if self._life_position == self.player.positions[-1]:
            self.player.add_score(self.player.get_next_position())
            self.new_life()

    def on_loop(self):
        self.player.update()
        self.check_map_bounds()
        self.check_life_collision()
        self.check_snake_collision()

    def check_map_bounds(self):
        # to pass for other side
        if self.player.positions[-1].x < self.player.step:
            self.player.positions[-1].x = self.map_bounds.x - self.player.step
        if self.player.positions[-1].x >= self.map_bounds.x:
            self.player.positions[-1].x = self.player.step

        if self.player.positions[-1].y < self.player.step:
            self.player.positions[-1].y = self.map_bounds.y - self.player.step
        if self.player.positions[-1].y >= self.map_bounds.y:
            self.player.positions[-1].y = self.player.step

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf, self._image_surf)
        self.draw_life(self._display_surf, self._image_life)
        self.draw_debug(self._display_surf, self._image_debug)
        pygame.display.flip()

    def check_snake_collision(self):
        if self.player.get_next_position() in self.player.positions:
            self.game_over = True

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init():
            self._running = False

        while not self.game_over:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.player.move_right()

            elif keys[K_LEFT]:
                self.player.move_left()

            elif keys[K_UP]:
                self.player.move_up()

            elif keys[K_DOWN]:
                self.player.move_down()

            if keys[K_ESCAPE]:
                self._running = False
                break

            self.on_loop()
            self.on_render()
            if self.debug:
                time.sleep(50.0 / 250.0)
            else:
                time.sleep(50.0 / 1000.0)

        if not self._running:
            self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
