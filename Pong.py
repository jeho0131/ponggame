import pygame, sys, random, math, time
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Pong Game")
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

#공의 이미지
ball_image = pygame.image.load("ball.png").convert_alpha()

#각 배트의 점수
rscore = 0
lscore = 0

#60초 타이머
mtimer = 0

lor = [0, 1]

#왼쪽 배트의 공을 친 횟수와 막은 횟수
hitlscore = 0
deflscore = 0

#오른쪽 배트의 공을 친 횟수와 막은 횟수
hitrscore = 0
defrscore = 0

#폰트들
font = pygame.font.Font(None, 40)

font2 = pygame.font.SysFont("corbel", 70)
font3 = pygame.font.Font(None, 60)
font4 = pygame.font.Font(None, 30)

sfont1 = pygame.font.Font(None, 500)
sfont2 = pygame.font.Font(None, 300)

tfont = pygame.font.Font(None, 50)

ofont = pygame.font.Font(None, 80)
ofont2 = pygame.font.Font(None, 100)
ofont3 = pygame.font.Font(None, 150)

#배트 구성
class Bat:
    #배트 기초 값
    def __init__(self, ctrls, x, side):
        self.ctrls = ctrls
        self.x = x
        self.y = 260
        self.side = side
        self.lastbop = 0
        self.bopnum = 0
        self.defnum = 0

    #배트의 좌우 이동
    def move(self):
        if pressed_keys[self.ctrls[0]] and self.y > 0:
            self.y -= 10
        if pressed_keys[self.ctrls[1]] and self.y < 520:
            self.y += 10

    #배트 그리기
    def draw(self):
        offset = -self.side * (time.time() < self.lastbop + 0.05) * 30
        pygame.draw.line(screen, (255, 255, 255), (self.x + offset, self.y), (self.x + offset, self.y + 80), 6)

    #배트로 공 치기
    def bop(self):
        if time.time() > self.lastbop + 0.3:
            self.lastbop = time.time()

#공 구성
class Ball:
    #공 기본값
    def __init__(self):
        self.d = (math.pi / 3) * random.random() + (math.pi / 3) + math.pi * random.choice(lor)
        self.speed = 12
        #fast가 1일 경우 속도 2배
        self.fast = random.randint(0, 5)
        #randball이 1일 경우 공이 랜덤으로 튕김
        self.randball = random.randint(0, 10)

        #fast가 1이고 randball이 1이 아니면 속도 2배 
        if self.fast == 1 and self.randball != 1:
            self.speed = 24
        else:
            self.speed = 12

        #공이 움직일 각도
        self.dx = math.sin(self.d) * self.speed
        self.dy = math.cos(self.d) * self.speed
        #공의 현재 좌표
        self.x = 475
        self.y = 275

    #공의 이동
    def move(self):
        self.x += self.dx
        self.y += self.dy

    #공의 튕기기
    def bounce(self):
        #아래나 위에 벽에 닿으면 튕기기
        if (self.y <= 0 and self.dy < 0) or (self.y >= 550 and self.dy > 0):
            #randball이 1이면 실행
            if self.randball == 1:
                #위쪽 벽이면 각도를 -75 ~ 75도로 랜덤 수정 
                if self.y <= 0 and self.dy < 0:
                    self.d = ((5 * math.pi) / 6) * random.random() - ((5 * math.pi) / 12)

                    self.dx = math.sin(self.d) * self.speed
                    self.dy = math.cos(self.d) * self.speed

                #아래쪽 벽이면 각도를 105 ~ 255도로 랜덤 수정
                elif self.y >= 550 and self.dy > 0:
                    self.d = ((5 * math.pi) / 6) * random.random() + ((7 * math.pi) / 12)

                    self.dx = math.sin(self.d) * self.speed
                    self.dy = math.cos(self.d) * self.speed

            #공 튕기기
            else:
                self.dy *= -1
                self.d = math.atan2(self.dx, self.dy)
        
        for bat in bats:
            #공과 배트가 만나면 실행
            if pygame.Rect(bat.x, bat.y, 6, 80).colliderect(int(self.x), int(self.y), 50, 50) and abs(
                    self.dx) / self.dx == bat.side:
                #randball이 1이면 실행
                if self.randball == 1:
                    #왼쪽 벽이면 15 ~ 165도로 랜덤 수정
                    if self.x < 20:
                        self.d = ((5 * math.pi) / 6) * random.random() + (math.pi / 12)

                    #오른쪽 벽이면 195 ~ 345도로 랜덤 수정
                    elif self.x > 940:
                        self.d = ((5 * math.pi) / 6) * random.random() + (math.pi / 12) + math.pi

                #공 튕기기
                else:
                    self.d *= -1
                    self.dx *= -1

                #각도가 마이너스(-)가 되지 않도록 수정
                self.d %= math.pi * 2

                #배트로 공을 칠려고 한 시간이 0.05초이내라면 공이 쳐지고 공의 속도가 더욱 빨라진다
                if time.time() < bat.lastbop + 0.05:
                    if self.speed < 50:
                        self.speed *= 1.5
                        bat.bopnum += 1
                #fast가 1이라면 속도가 공을 막을때 마다 1.3배씩 계속해서 빨라진다
                elif self.fast == 1:
                    self.speed *= 1.3

                #속도가 20전일때 공을 막을때마다 1.1배씩 속도가 빨라진다
                else:
                    if self.speed < 20:
                        self.speed *= 1.1

                #좌표 변경
                self.dx = math.sin(self.d) * self.speed
                self.dy = math.cos(self.d) * self.speed
                bat.defnum += 1

    #공 그리기
    def draw(self):
        screen.blit(ball_image, (int(self.x), int(self.y)))
 
#시작 또는 재 시작할 때 준비 시간
def start():
    screen.fill((0,0,0))
    stxt = sfont1.render("3", True, (255, 255, 255))
    screen.blit(stxt, (int(screen.get_width() / 2 - stxt.get_width() / 2), int(screen.get_height() / 2 - stxt.get_height() / 2)))
    pygame.display.update()
    time.sleep(1)
    
    screen.fill((0,0,0))
    stxt = sfont1.render("2", True, (255,255,255))
    screen.blit(stxt, (int(screen.get_width() / 2 - stxt.get_width() / 2), int(screen.get_height() / 2 - stxt.get_height() / 2)))
    pygame.display.update()
    time.sleep(1)
    
    screen.fill((0,0,0))
    stxt = sfont1.render("1", True, (255,255,255))
    screen.blit(stxt, (int(screen.get_width() / 2 - stxt.get_width() / 2), int(screen.get_height() / 2 - stxt.get_height() / 2)))
    pygame.display.update()
    time.sleep(1)

    screen.fill((0,0,0))
    stxt = sfont2.render("START", True, (255,255,255))
    screen.blit(stxt, (int(screen.get_width() / 2 - stxt.get_width() / 2), int(screen.get_height() / 2 - stxt.get_height() / 2)))
    pygame.display.update()
    time.sleep(0.5)

#한 게임 플레이 타임이 60초가 지날때 서로의 승패를 정해주는 함수
def timeout():
    global rscore
    global lscore
    
    screen.fill((0,0,0))
    otxt = ofont3.render("TIME OUT", True, (255,255,255))
    screen.blit(otxt, (int(screen.get_width() / 2 - otxt.get_width() / 2), int(screen.get_height() / 2 - otxt.get_height() / 2)))
    pygame.display.update()
    time.sleep(2)

    screen.fill((0,0,0))
    otxt = ofont2.render("LEFT", True, (255,0,0))
    screen.blit(otxt, (int(screen.get_width() / 4 - otxt.get_width() / 2), int(screen.get_height() / 16)))
    otxt = ofont2.render("RIGHT", True, (255,0,0))
    screen.blit(otxt, (int(screen.get_width() * 3 / 4 - otxt.get_width() / 2), int(screen.get_height() / 16)))
    pygame.display.update()
    time.sleep(1)

    otxt = ofont2.render("hit", True, (255,255,255))
    screen.blit(otxt, (50, int(screen.get_height() / 4)))
    otxt = ofont.render(str(hitlscore), True, (255,255,255))
    screen.blit(otxt, (int(screen.get_width() / 4 - otxt.get_width() / 2), int(screen.get_height() / 4)))
    otxt = ofont.render(str(hitrscore), True, (255,255,255))
    screen.blit(otxt, (int(screen.get_width() * 3 / 4 - otxt.get_width() / 2), int(screen.get_height() / 4)))
    pygame.display.update()
    time.sleep(1)

    otxt = ofont2.render("def", True, (255,255,255))
    screen.blit(otxt, (50, int(screen.get_height() / 2)))
    otxt = ofont.render(str(deflscore), True, (255,255,255))
    screen.blit(otxt, (int(screen.get_width() / 4 - otxt.get_width() / 2), int(screen.get_height() / 2)))
    otxt = ofont.render(str(defrscore), True, (255,255,255))
    screen.blit(otxt, (int(screen.get_width() * 3 / 4 - otxt.get_width() / 2), int(screen.get_height() / 2)))
    pygame.display.update()
    time.sleep(1)
    
    rpscore = hitrscore * 10 + defrscore * 5
    lpscore = hitlscore * 10 + deflscore * 5
    
    if rpscore > lpscore:
        otxt = ofont2.render("LOSE", True, (255,0,0))
        screen.blit(otxt, (int(screen.get_width() / 4 - otxt.get_width() / 2), int(screen.get_height() * 3 / 4)))
        otxt = ofont2.render("WIN", True, (255,215,0))
        screen.blit(otxt, (int(screen.get_width() * 3 / 4 - otxt.get_width() / 2), int(screen.get_height() * 3 / 4)))
        rscore += 1

    elif rpscore < lpscore:
        otxt = ofont2.render("WIN", True, (255,215,0))
        screen.blit(otxt, (int(screen.get_width() / 4 - otxt.get_width() / 2), int(screen.get_height() * 3 / 4)))
        otxt = ofont2.render("LOSE", True, (255,0,0))
        screen.blit(otxt, (int(screen.get_width() * 3 / 4 - otxt.get_width() / 2), int(screen.get_height() * 3 / 4)))
        lscore += 1

    elif rpscore == lpscore:
        otxt = ofont2.render("SAME", True, (255,255,255))
        screen.blit(otxt, (int(screen.get_width() / 4 - otxt.get_width() / 2), int(screen.get_height() * 3 / 4)))
        otxt = ofont2.render("SAME", True, (255,255,255))
        screen.blit(otxt, (int(screen.get_width() * 3 / 4 - otxt.get_width() / 2), int(screen.get_height() * 3 / 4)))
        
    pygame.display.update()
    time.sleep(2)
    bats[0].y = 200
    bats[1].y = 200
    
    reset()
    start()
    
#게임 값을 리셋
def reset():
    global ball
    
    for bat in bats:
        bat.bopnum = 0
        bat.defnum = 0

    ball = Ball()

#공 생성                      
ball = Ball()
#배트 생성
bats = [Bat([K_w, K_s], 10, -1), Bat([K_UP, K_DOWN], 984, 1)]

#시작 함수
start()

#타이머 시작
mtimer = time.time()

while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

        if event.type == KEYDOWN:
            #q를 누르면 왼쪽 배트가 공을 칠려고 시도
            if event.key == K_q:
                bats[0].bop()
            #shift를 누르면 오른쪽 배트가 공을 칠려고 시도
            if event.key == K_RSHIFT:
                bats[1].bop()
                
    pressed_keys = pygame.key.get_pressed()

    #화면 초기화
    screen.fill((0, 0, 0))

    #화면에 배경 그리기
    pygame.draw.line(screen, (255, 255, 255), (int(screen.get_width() / 2), 0),
                     (int(screen.get_width() / 2), screen.get_height()), 3)
    pygame.draw.circle(screen, (255, 255, 255), (int(screen.get_width() / 2), int(screen.get_height() / 2)), 50, 3)

    #배트 움직이기
    for bat in bats:
        bat.move()
        bat.draw()

    #공이 왼쪽으로 넘어갈시 공, 시간 초기화 오른쪽 배트 득점
    if ball.x < -50:
        reset()
        mtimer = time.time()
        rscore += 1

    #공이 오른쪽으로 넘어갈시 공, 시간 초기화 왼쪽 배트 득점
    if ball.x > 1000:
        reset()
        mtimer = time.time()
        lscore += 1

    #한 게임에 시간이 60초가 지났을경우 timeout 함수 실행
    if int(60 - (time.time() - mtimer)) <= 50:
        timeout()
        mtimer = time.time()

    #공을 움직이고 튕기기
    ball.move()
    ball.draw()
    ball.bounce()

    #배트가 공을 친 횟수, 공을 막은 횟수를 업데이트
    hitlscore = bats[0].bopnum
    hitrscore = bats[1].bopnum
    deflscore = bats[0].defnum
    defrscore = bats[1].defnum

    #각 배트의 점수를 화면에 그리기
    txt = font.render(str(lscore), True, (255, 255, 255))
    screen.blit(txt, (20, 20))
    txt = font.render(str(rscore), True, (255, 255, 255))
    screen.blit(txt, (980 - txt.get_width(), 20))

    #남은 시간 화면에 그리기
    mcount = int(60-(time.time()-mtimer))
    timetxt = font.render(str(mcount), True, (255,0,0))
    screen.blit(timetxt, (int(screen.get_width() / 2 - timetxt.get_width() / 2), 25))

    #두 배트 중에서 10점이 넘긴 배트가 있을경우 실행
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
        screen.blit(txt, (int(screen.get_width() / 2 - txt.get_width() / 2), int(screen.get_height() - 50)))
        
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            pressed_keys = pygame.key.get_pressed()
            #space를 누르면 다시 실행
            if pressed_keys[K_SPACE]:
                reset()
                rscore = 0
                lscore = 0
                
                bats[0].y = 200
                bats[1].y = 200
                
                start()
                mtimer = time.time()
                break
            pygame.display.update()

    pygame.display.update()
