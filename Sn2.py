import pygame
from pygame.locals import *
import time
import random

size = 40
length = 1

class Apple:
    """Class to create Apple."""
    def __init__(self, parent_screen):
        self.apple_img = pygame.image.load('Resources/apple.jpg').convert()
        self.ps = parent_screen
        self.x = size*3
        self.y = size*3

    def draw(self): 
        self.ps.blit(self.apple_img, (self.x, self.y))
        pygame.display.flip()

    """Creating apple object at random location"""
    def move(self):
        self.x = random.randint(1, 20) * size
        self.y = random.randint(1, 10) * size

"""_____________________________________________________________________________________________________________________________________________________________"""

class Snake:
    """Class to create Snake."""
    def __init__(self, parent_screen, length, direction ='right'):
        self.length = length
        self.ps = parent_screen
        # Loading block image.
        self.block = pygame.image.load("Resources/block.jpg").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = direction

    def draw(self):
        for i in range(self.length):
            self.ps.blit(self.block, (self.x[i], self.y[i])) # Positioning the block in the background.
        pygame.display.flip()  # Updates the entire screen.

    """Increasing length of snake"""
    def incr_length(self):
        self.length += 1
        self.x.append(size)
        self.y.append(size)

    """Defining movements for snake"""
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'

    """Defining how snake crawls"""
    def crawl(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        self.draw()

    def random_start(self):
        self.x = [size * random.randint(1, 20)] * self.length
        self.y = [size * random.randint(1, 10)] * self.length

"""_____________________________________________________________________________________________________________________________________________________________"""

class Snake_game:
    """Class to create game."""
    def __init__(self):
        pygame.init()  # Pygame is initiated as to initialize the whole module.
        pygame.mixer.init()
        pygame.mixer.music.load("Resources/bg_music_1.mp3")
        pygame.mixer.music.play()
        # Creating Window.
        self.surface = pygame.display.set_mode((1000, 600))
        # Filling Background with image.
        self.background()
        self.snake = Snake(self.surface, length)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    """Defining collision criteria"""
    def collision(self, x1, y1, x2, y2):
            if x1 >= x2 and x1 < x2 + size:
                if y1 >= y2 and y1 < y2 + size:
                    #print(x1, x2, y1, y2)
                    return True
            return False
    
    def background(self):
        bg = pygame.image.load("Resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def run(self):
        self.background()
        self.snake.crawl()
        self.apple.draw()
        self.disp_score()
        pygame.display.flip()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("Resources/Sound_crunch.wav")
            pygame.mixer.Sound.play(sound)
            self.snake.incr_length()
            self.apple.move()

        for i in range(1, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                raise Exception("Game Over")

        if self.snake.x[0] == self.surface.get_size()[0] or self.snake.y[0] == self.surface.get_size()[1]\
                or self.snake.x[0] == 0 or self.snake.y[0] == 0:
            raise Exception("Hit by the Wall")

    def game_over(self, e):
        self.background()
        font = pygame.font.SysFont('arial', 20, True, True)
        msg1 = font.render(f" {e}. Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(msg1, (420, 290))
        msg2 = font.render(f"Press Enter to Replay. Press Esc to Exit", True, (255, 255, 255))
        self.surface.blit(msg2, (350, 315))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def disp_score(self):
        font = pygame.font.SysFont('arial', 22, True, True)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (900,20))

    """Function to play"""
    def play(self):
        flag = True
        pause = False
        while flag:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        flag = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                        self.snake.length = length
                        self.snake.random_start()
                        random.choice([self.snake.move_right(), self.snake.move_down()])
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                     flag = False
            try:
                if not pause:
                    self.run()
            except Exception as e:
                sound = pygame.mixer.Sound("Resources/1_snake_game_resources_crash.mp3")
                pygame.mixer.Sound.play(sound)
                self.game_over(e)
                pause = True
            time.sleep(0.05)
"""_____________________________________________________________________________________________________________________________________________________________"""

if __name__ == "__main__":
     game = Snake_game()
     game.play()


