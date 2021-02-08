import pygame, sys, random,math
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Pong Game")
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()

ball_image = pygame.image.load("ball.png").convert_alpha()

rscore = 0
lscore = 0
lor = [0,1]

font = pygame.font.Font(None,40)

class Bat:
    def __init__(self,ctrls,x,side):
        self.ctrls = ctrls
        self.x = x
        self.y = 260
        self.side = side

    def move(self):
        if pressed_keys[self.ctrls[0]] and self.y > 0:
            self.y -= 10
        if pressed_keys[self.ctrls[1]] and self.y < 520:
            self.y += 10

    def draw(self):
        pygame.draw.line(screen,(255,255,255),(self.x,self.y),(self.x,self.y+80),6)

class Ball:
    def __init__(self):
        d = (math.pi/3)*random.random()+(math.pi/3)+math.pi*random.choice(lor)
        self.fast = random.randint(0,5)
        self.randball = random.randint(0,10)
        
        if self.fast == 1 and self.randball != 1:
            self.dx = math.sin(d)*24
        else:
            self.dx = math.sin(d)*12
        self.dy = math.cos(d)*12
        self.x = 475
        self.y = 275

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self):
        if self.y <= 0 or self.y >= 550:
            if self.randball == 1:
                d = (math.pi/3)*random.random()+(math.pi/3)+math.pi*random.choice(lor)
                self.dy = math.cos(d)*12
            else:
                self.dy *= -1

        for bat in bats:
            if pygame.Rect(bat.x,bat.y,6,80).colliderect(self.x,self.y,50,50) and abs(self.dx)/self.dx == bat.side:
                if self.randball == 1:
                    d = (math.pi/3)*random.random()+(math.pi/3)+math.pi*random.choice(lor)
                    self.dx = math.sin(d)*12
                self.dx *= -1

    def draw(self):
        screen.blit(ball_image,(self.x, self.y))

ball = Ball()
bats = [Bat([K_w,K_s], 10, -1), Bat([K_UP,K_DOWN], 984, 1)]

while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()
    pressed_keys = pygame.key.get_pressed()

    screen.fill((0,0,0))

    pygame.draw.line(screen, (255,255,255), (screen.get_width()/2,0), (screen.get_width()/2,screen.get_height()),3)
    pygame.draw.circle(screen, (255,255,255), (int(screen.get_width()/2), int(screen.get_height()/2)), 50, 3)

    for bat in bats:
        bat.move()
        bat.draw()

    if ball.x < -50:
        ball = Ball()
        rscore += 1

    if ball.x > 1000:
        ball = Ball()
        lscore += 1

    ball.move()
    ball.draw()
    ball.bounce()

    txt = font.render(str(lscore), True, (255,255,255))
    screen.blit(txt,(20,20))
    txt = font.render(str(rscore), True, (255,255,255))
    screen.blit(txt,(980-txt.get_width(),20))

    pygame.display.update()
