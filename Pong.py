import pygame, sys, random, math, time
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Pong Game")
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

ball_image = pygame.image.load("ball.png").convert_alpha()

rscore = 0
lscore = 0
lor = [0, 1]
mtimer = 0

font = pygame.font.Font(None, 40)

font2 = pygame.font.SysFont("corbel", 70)
font3 = pygame.font.Font(None, 60)
font4 = pygame.font.Font(None, 30)

sfont1 = pygame.font.Font(None, 500)
sfont2 = pygame.font.Font(None, 300)

tfont = pygame.font.Font(None, 50)

class Bat:
    def __init__(self, ctrls, x, side):
        self.ctrls = ctrls
        self.x = x
        self.y = 260
        self.side = side
        self.lastbop = 0

    def move(self):
        if pressed_keys[self.ctrls[0]] and self.y > 0:
            self.y -= 10
        if pressed_keys[self.ctrls[1]] and self.y < 520:
            self.y += 10

    def draw(self):
        offset = -self.side * (time.time() < self.lastbop + 0.05) * 30
        pygame.draw.line(screen, (255, 255, 255), (self.x + offset, self.y), (self.x + offset, self.y + 80), 6)

    def bop(self):
        if time.time() > self.lastbop + 0.3:
            self.lastbop = time.time()

class Ball:
    def __init__(self):
        self.d = (math.pi / 3) * random.random() + (math.pi / 3) + math.pi * random.choice(lor)
        self.speed = 12
        self.fast = random.randint(0, 5)
        self.randball = random.randint(0, 1)

        if self.fast == 1 and self.randball != 1:
            self.speed = 24
        else:
            self.speed = 12

        self.dx = math.sin(self.d) * self.speed
        self.dy = math.cos(self.d) * self.speed
        self.x = 475
        self.y = 275

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self):
        if (self.y <= 0 and self.dy < 0) or (self.y >= 550 and self.dy > 0):
            if self.randball == 1:
                if self.y <= 0 and self.dy < 0:
                    self.d = ((2 * math.pi) / 3) * random.random() - ((5 * math.pi) / 12)

                    self.dx = math.sin(self.d) * self.speed
                    self.dy = math.cos(self.d) * self.speed

                elif self.y >= 550 and self.dy > 0:
                    self.d = ((2 * math.pi) / 3) * random.random() + ((7 * math.pi) / 12)

                    self.dx = math.sin(self.d) * self.speed
                    self.dy = math.cos(self.d) * self.speed

            else:
                self.dy *= -1
                self.d = math.atan2(self.dx, self.dy)

        for bat in bats:
            if pygame.Rect(bat.x, bat.y, 6, 80).colliderect(int(self.x), int(self.y), 50, 50) and abs(
                    self.dx) / self.dx == bat.side:
                if self.randball == 1:
                    if self.x < 20:
                        self.d = ((2 * math.pi) / 3) * random.random() + (math.pi / 12)
                        
                    elif self.x > 940:
                        self.d = ((2 * math.pi) / 3) * random.random() + (math.pi / 12) + math.pi

                else:
                    self.d *= -1
                self.dx *= -1
                    
                self.d %= math.pi * 2

                if time.time() < bat.lastbop + 0.05:
                    if self.speed < 20:
                        self.speed *= 1.5

                elif self.fast == 1:
                    self.speed *= 1.3

                else:
                    if self.speed < 20:
                        self.speed *= 1.1

                self.dx = math.sin(self.d) * self.speed
                self.dy = math.cos(self.d) * self.speed

    def draw(self):
        screen.blit(ball_image, (int(self.x), int(self.y)))

def start():
    screen.fill((0,0,0))
    stxt = sfont1.render("3", True, (255, 255, 255))
    screen.blit(stxt, (400,150))
    pygame.display.update()
    time.sleep(1)
    
    screen.fill((0,0,0))
    stxt = sfont1.render("2", True, (255,255,255))
    screen.blit(stxt, (400,150))
    pygame.display.update()
    time.sleep(1)
    
    screen.fill((0,0,0))
    stxt = sfont1.render("1", True, (255,255,255))
    screen.blit(stxt, (400,150))
    pygame.display.update()
    time.sleep(1)

    screen.fill((0,0,0))
    stxt = sfont2.render("START", True, (255,255,255))
    screen.blit(stxt, (180, 180))
    pygame.display.update()
    time.sleep(0.5)

ball = Ball()
bats = [Bat([K_w, K_s], 10, -1), Bat([K_UP, K_DOWN], 984, 1)]

start()

mtimer = time.time()

while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()
            
        if event.type == KEYDOWN:
            if event.key == K_q:
                bats[0].bop()
            if event.key == K_RSHIFT:
                bats[1].bop()
                
    pressed_keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    pygame.draw.line(screen, (255, 255, 255), (int(screen.get_width() / 2), 0),
                     (int(screen.get_width() / 2), screen.get_height()), 3)
    pygame.draw.circle(screen, (255, 255, 255), (int(screen.get_width() / 2), int(screen.get_height() / 2)), 50, 3)

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

    txt = font.render(str(lscore), True, (255, 255, 255))
    screen.blit(txt, (20, 20))
    txt = font.render(str(rscore), True, (255, 255, 255))
    screen.blit(txt, (980 - txt.get_width(), 20))

    mcount = round(60-(time.time()-mtimer))
    timetxt = font.render(str(mcount), True, (255,0,0))
    screen.blit(timetxt, (screen.get_width() * 24 / 50, 25))

    if rscore > 9 or lscore > 9:
        screen.fill((0, 0, 0))

        txt = font2.render("score", True, (255, 0, 0))
        screen.blit(txt, (int(screen.get_width() / 4 - txt.get_width() / 2), int(screen.get_height() / 4)))
        screen.blit(txt, (int(screen.get_width() * 3 / 4 - txt.get_width() / 2), int(screen.get_height() / 4)))

        txt = font3.render(str(lscore), True, (255, 255, 255))
        screen.blit(txt, (int(screen.get_width() / 4 - txt.get_width() / 2), int(screen.get_height() / 2)))

        txt = font3.render(str(rscore), True, (255, 255, 255))
        screen.blit(txt, (int(screen.get_width() * 3 / 4 - txt.get_width() / 2), int(screen.get_height() / 2)))

        txt = font4.render("Press Space to restart", True, (255, 255, 255))
        screen.blit(txt, (int(screen.get_width() * 2 / 5), int(screen.get_height() - 50)))

        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                lscore = 0
                rscore = 0
                bats[0].y = 200
                bats[1].y = 200
                ball = Ball()
                start()
                break
            pygame.display.update()

    pygame.display.update()
