import pygame
from .paddle import Paddle
from .ball import Ball
import time
import random

# Colors
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.winning_score = 5  # default winning score

        # Initialize paddles
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)

        # Initialize ball and pass GameEngine reference for sounds
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, game_engine=self)

        # Scores
        self.player_score = 0
        self.ai_score = 0

        # Font
        self.font = pygame.font.SysFont("Arial", 30)

        # Load sounds
        self.sound_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")

    # Handle player input
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    # Update game state
    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring
        if self.ball.x <= 0:  # AI scores
            self.ai_score += 1
            self.ball.reset()
            self.sound_score.play()
        elif self.ball.x >= self.width:  # Player scores
            self.player_score += 1
            self.ball.reset()
            self.sound_score.play()

        # AI paddle movement
        self.ai.auto_track(self.ball, self.height)

    # Render everything
    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    # Check if game is over and show replay options
    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            # Determine winner
            if self.player_score >= self.winning_score:
                message = "Player Wins!"
            else:
                message = "AI Wins!"

            # Clear screen and show winner
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont("Arial", 50)
            text = font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(self.width//2, self.height//2 - 50))
            screen.blit(text, text_rect)

            # Show replay options
            option_font = pygame.font.SysFont("Arial", 30)
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, opt in enumerate(options):
                opt_text = option_font.render(opt, True, WHITE)
                opt_rect = opt_text.get_rect(center=(self.width//2, self.height//2 + i*40 + 30))
                screen.blit(opt_text, opt_rect)

            pygame.display.flip()

            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            self.winning_score = 3
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 5
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 7
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()

            # Reset game state for replay
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
