import pygame
from constants import WIDTH, HEIGHT

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load images into a list
        self.frames = [
            pygame.image.load("images/BirdUp.png"),
            pygame.image.load("images/BirdSide.png"),
            pygame.image.load("images/BirdDown.png")
        ]

        # Track animaion state 
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.centery = HEIGHT//2 - 50
        self.vy = 0
        self.angle = 0
        self.moving = False
        self.alive = True

        # Animation speed
        self.animation_speed = 0.15

        # Rotate variable
        self.rotation = 0

    '''def apply_rotation(self):
        if self.rotation > -70:
            self.rotation -= 1.5'''

    def update(self):
        if self.rect.top < 5:
            self.rect.top = 5
        elif self.rect.bottom > 550:
            self.rect.bottom = 550
            self.vy = 0

        if self.alive:
            # Increase frame counter
            self.current_frame += self.animation_speed

            # Loop back to frame 0 once you've exeeded the number of images
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

            # Update active image
            self.image = self.frames[int(self.current_frame)]

            if self.moving:
                if self.rotation > -70:
                    self.rotation -= 1.5

                self.image = pygame.transform.rotozoom(self.frames[int(self.current_frame)], self.rotation, 1)

                self.rect = self.image.get_rect(center=self.rect.center)
        elif not self.alive:
            self.rect.y += 5
            if self.rect.bottom > 550:
                self.rect.bottom = 548

class Grass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Ground.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.centery = 700

class GreenTopPipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/GreenTopPipe.png")
        self.rect = self.image.get_rect()
        self.moving = False
        if not self.moving:
            self.rect.centerx = WIDTH-100
        else:
            self.rect.centerx = WIDTH+50
        self.rect.centery = -50
        self.pipe_speed = 10

    def update(self, speed):
        self.rect.x -= self.pipe_speed + speed

        if self.rect.x < -35:
            self.kill()

class GreenBotPipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/GreenBottomPipe.png")
        self.rect = self.image.get_rect()
        self.moving = False
        if not self.moving:
            self.rect.centerx = WIDTH-100
        else:
            self.rect.centerx = WIDTH+50
        self.rect.centery = 550
        self.pipe_speed = 10

    def update(self, speed):
        self.rect.x -= self.pipe_speed + speed

        if self.rect.x < -35:
            self.kill()

class RedTopPipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/RedTopPipe.png")
        self.rect = self.image.get_rect()
        self.moving = False
        if not self.moving:
            self.rect.centerx = WIDTH-100
        else:
            self.rect.centerx = WIDTH+50
        self.rect.centery = -50
        self.pipe_speed = 15

    def update(self, speed):
        self.rect.x -= self.pipe_speed + speed

        if self.rect.x < -35:
            self.kill()


class RedBotPipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/RedBottomPipe.png")
        self.rect = self.image.get_rect()
        self.moving = False
        if not self.moving:
            self.rect.centerx = WIDTH-100
        else:
            self.rect.centerx = WIDTH+50
        self.rect.centery = 550
        self.pipe_speed = 15

    def update(self, speed):
        self.rect.x -= self.pipe_speed + speed
        if self.rect.x < -35:
            self.kill()