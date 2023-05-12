import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 512
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Flappy bird')

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 80)


imgBG = pygame.image.load('images/background-day.png')
imgBirdu = pygame.image.load('images/yellowbird-upflap.png')
imgPT = pygame.image.load('images/pipe-green.png')
imgPB = pygame.image.load('images/pipe-greendown.png')


py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 34, 24)

pipes = []
bgs = []
ps = []

pipeSize = 200
pipePos = HEIGHT // 2 

bgs.append(pygame.Rect(0, 0, 288, 512))

lives = 3
scores = 0

state = 'start'
timer = 10

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    for i in range(len(bgs) - 1, -1, -1):
        bg = bgs[i]
        bg.x -= 1

        if bg.right < 0:
            bgs.remove(bg)

        if bgs[len(bgs) - 1].right <= WIDTH:
            bgs.append(pygame.Rect(bgs[len(bgs) - 1].right, 0, 288, 512))

    for i in range(len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe.x -= 3

        if pipe.right < 0:
            pipes.remove(pipe)
            if pipe in ps:
                ps.remove(pipe)

    if state == 'start':
        if click and timer == 0 and len(pipes) == 0:
            state = 'play'
        py += (HEIGHT // 2 - py) * 0.1
        player.y = py

    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0
    
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 52, pipePos - pipeSize // 2))
            pipes.append(pygame.Rect(WIDTH, pipePos + pipeSize // 2, 52, HEIGHT - pipePos + pipeSize // 2))

            pipePos += randint(-100, 100)
            if pipePos < pipeSize:
                pipePos = pipeSize
            elif pipePos > HEIGHT - pipeSize:
                pipePos = HEIGHT - pipeSize

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'
            if pipe.right < player.left and pipe not in ps:
                ps.append(pipe)
                scores += 5

    elif state == 'fall':
        sy, ay = 0, 0
        pipePos = HEIGHT // 2 

        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 60
        else:
            state = 'gameover'
            timer = 120

    else:
        
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py


        if timer == 0:
            play = False



    window.fill(pygame.Color('black'))
    for bg in bgs:
        window.blit(imgBG, bg)


    for pipe in pipes:
        if pipe.y == 0:
            rect = imgPT.get_rect(bottomleft = pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPB.get_rect(topleft = pipe.topleft)
            window.blit(imgPB, rect)
        

    window.blit(imgBirdu, player) #image of bird

    text = font1.render('Scores: ' + str(scores), 1, pygame.Color('green'))
    window.blit(text, (10, 10))

    text = font1.render('Lives: ' + str(lives), 1, pygame.Color('white'))
    window.blit(text, (10, HEIGHT - 30))

    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()