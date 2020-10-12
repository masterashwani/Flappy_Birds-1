import pygame
import sys
import random

from pygame.locals import *

pygame.init()

width = 1250
height = 714
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

# images
background = pygame.image.load("images/background.png").convert_alpha()
bird = pygame.image.load("images/bird.png").convert_alpha()
pipe = pygame.image.load("images/pipe.png").convert_alpha()
rotatedPipe = pygame.image.load("images/rotated_pipe.png").convert_alpha()

# Game Caption
pygame.display.set_caption("Flappy Bird")
# sounds
point = pygame.mixer.Sound("sounds/sfx_point.wav")
hit = pygame.mixer.Sound("sounds/sfx_hit.wav")
#bgmusic
pygame.mixer.music.load("sounds/bgmusic.mp3") 
pygame.mixer.music.play(-1)


class Game:
    def __init__(self):
        self.gameOn = True
        self.birdX = 100
        self.birdY = 100
        self.pipesX = [width, width + 200, width + 400, width + 600, width + 800, width + 1000, width + 1200]
        self.lowerPipeY = [self.randomPipe(), self.randomPipe(), self.randomPipe(), self.randomPipe(),
                           self.randomPipe(), self.randomPipe(), self.randomPipe()]
        self.upperPipeY = [self.randomRotatedPipe(), self.randomRotatedPipe(), self.randomRotatedPipe(),
                           self.randomRotatedPipe(), self.randomRotatedPipe(), self.randomRotatedPipe(), self.randomRotatedPipe()]
        self.gravity = 0
        self.pipeVel = 0
        self.flap = 0
        self.score = 0
        self.rotateAngle = 0
        self.isGameOver = False
        self.playSound = True
        self.speed_accelerating = 5

        try:
            self.highest_score = int(self.gethighestscore())
        except:
            self.highest_score = 0

    def movingPipe(self):
        for i in range(0, 7):
            self.pipesX[i] += -self.pipeVel

        for i in range(0, 7):
            if (self.pipesX[i] < -50):
                self.pipesX[i] = width + 100
                self.lowerPipeY[i] = self.randomPipe()
                self.upperPipeY[i] = self.randomRotatedPipe()

    def randomPipe(self):
        return random.randrange(int(height / 2) + 50, height - 200)

    def randomRotatedPipe(self):
        return random.randrange(-int(height / 2) + 100, -100)

    def flapping(self):
        self.birdY += self.gravity
        if (self.isGameOver == False):
            self.flap -= 1
            self.birdY -= self.flap

    def isCollide(self):
        for i in range(0, 7):
            if (self.birdX >= self.pipesX[i] and self.birdX <= (self.pipesX[i] + pipe.get_width())
                    and ((self.birdY + bird.get_height() - 15) >= self.lowerPipeY[i] or
                         (self.birdY) <= self.upperPipeY[i] + rotatedPipe.get_height() - 15)):
                return True

            elif (self.birdX == self.pipesX[i] and (
                    self.birdY <= self.lowerPipeY[i] and self.birdY >= self.upperPipeY[i])):
                if (self.isGameOver == False):
                    self.score += 1
                    pygame.mixer.Sound.play(point)
                    #accelerating speed of game
                    self.speed_accelerating += 0.001

        if (self.birdY <= 0):
            return True

        elif (self.birdY + bird.get_height() >= height):
            self.gravity = 0
            return True

        return False

    def gethighestscore(self):
        with open("Highest Score.txt", "r") as f:
            return f.read()

    def gameOver(self):
        if (self.isCollide()):
            self.isGameOver = True
            self.screenText("Game Over!", (255, 255, 255), 450, 300, 84, "Fixedsys", bold=True)
            self.screenText("Press Enter To Play Again", (255, 255, 255), 400, 600, 48, "Fixedsys", bold=True)
            self.screenText("Highest Score : ", (0, 0, 0), 440, 425, 48, "Fixedsys", bold=True)
            self.screenText(str(self.highest_score), (0, 0, 0), 750, 425, 48, "Fixedsys", bold=True)
            self.screenText("Your Score : ", (0, 0, 0), 440, 475, 48, "Fixedsys", bold=True)
            self.screenText(str(self.score), (0, 0, 0), 750, 475, 48, "Fixedsys", bold=True)
            self.pipeVel = 0
            self.flap = 0
            self.rotateAngle = -90
            if (self.playSound):
                pygame.mixer.Sound.play(hit)
                self.playSound = False

    def screenText(self, text, color, x, y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x, y))

    def mainGame(self):
        while self.gameOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if (self.isGameOver == False):
                            self.pipeVel = 5
                            self.gravity = 10
                            self.flap = 20
                            self.rotateAngle = 15

                    if event.key == K_RETURN:
                        newGame = Game()
                        newGame.mainGame()

                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.rotateAngle = 0
                        # blitting images
            screen.blit(background, (0, 0))

            for i in range(0, 7):
                # lower  Pipe
                screen.blit(pipe, (self.pipesX[i], self.lowerPipeY[i]))
                # upper pipe
                screen.blit(rotatedPipe, (self.pipesX[i], self.upperPipeY[i]))

            screen.blit(pygame.transform.rotozoom(bird, self.rotateAngle, 1), (self.birdX, self.birdY))

            # moving pipe
            self.movingPipe()
            # flapping
            self.flapping()
            # game over
            self.gameOver()
            # displaying score
            self.screenText(str(self.score), (255, 255, 255), 600, 50, 68, "Fixedsys", bold=True)
            #checking highest score
            if self.highest_score < self.score:
                self.highest_score = self.score
            with open("Highest Score.txt", "w") as f:
                f.write(str(self.highest_score))

            pygame.display.update()
            clock.tick(fps)


flappyBird = Game()
flappyBird.mainGame()
