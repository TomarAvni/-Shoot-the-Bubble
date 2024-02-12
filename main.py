import pygame
import sys
import random

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player:
    def __init__(self, x, y, radius=10, speed=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.move_left_pressed = False
        self.move_right_pressed = False

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)


class Bullet:
    def __init__(self, x, y, radius=10  , color=RED, speed=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Bubble:
    def __init__(self, x, y, radius=30, speed=2) :
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)


class Game:
    def __init__(self, width=1000, height=800):
        self.width = width
        self.height = height
        self.player = Player(width // 2, height - 20)
        self.bullets = []
        self.bubbles = []
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left_pressed = True
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.move_left_pressed = False
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right_pressed = False

    def shoot(self):
        self.bullets.append(Bullet(self.player.x, self.player.y - self.player.radius))

    def generate_bubbles(self):
        if random.randint(0, 100 ) < 2:
            bubble_x = random.randint(0, self.width)
            self.bubbles.append(Bubble(bubble_x, 0))

    def update_objects(self):
        for bullet in self.bullets:
            bullet.move()

        for bubble in self.bubbles:
            bubble.move()

        for bubble in self.bubbles:
            for bullet in self.bullets:
                if pygame.Rect(bubble.x - bubble.radius, bubble.y - bubble.radius, bubble.radius * 2, bubble.radius * 2).collidepoint(bullet.x, bullet.y):
                    self.bubbles.remove(bubble)
                    self.bullets.remove(bullet)
                    self.score += 1

        if len(self.bubbles) >= 20:
            self.game_over = True

    def draw_objects(self, screen):
        self.player.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
        for bubble in self.bubbles:
            bubble.draw(screen)

    def display_score(self, screen, font):
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        screen.blit(score_text, (10, 10))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Shoot the Falling Bubbles")
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("monospace", 24)

        while not self.game_over:
            screen.fill(BLACK)
            self.handle_events()
            self.generate_bubbles()
            self.update_objects()
            self.draw_objects(screen)
            self.display_score(screen, font)
            pygame.display.flip()
            clock.tick(60)
            if self.player.move_left_pressed:
                self.player.move_left()
            if self.player.move_right_pressed:
                self.player.move_right()


if __name__ == "__main__":
    game = Game(width=1100, height=800)
    game.run()
