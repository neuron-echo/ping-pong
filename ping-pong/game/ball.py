import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, game_engine=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.game_engine = game_engine  # reference to GameEngine for playing sounds

    def move(self):
        # Move the ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.game_engine:
                self.game_engine.sound_wall.play()

    def check_collision(self, player, ai):
        # Get the ball rectangle after moving
        ball_rect = self.rect()

        # Check collision with player paddle
        if ball_rect.colliderect(player.rect()):
            self.velocity_x = abs(self.velocity_x)  # ensure ball moves right
            if self.game_engine:
                self.game_engine.sound_paddle.play()

        # Check collision with AI paddle
        elif ball_rect.colliderect(ai.rect()):
            self.velocity_x = -abs(self.velocity_x)  # ensure ball moves left
            if self.game_engine:
                self.game_engine.sound_paddle.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
