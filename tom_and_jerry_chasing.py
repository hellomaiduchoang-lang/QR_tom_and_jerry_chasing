import pygame
import sys
import random
from collections import deque

pygame.init()
pygame.mixer.init()

# ======================
# MUSIC
# ======================

pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound("sounds/eat.wav")
eat_sound.set_volume(0.2)

lucky_sound = pygame.mixer.Sound("sounds/lucky.wav")
hit_sound = pygame.mixer.Sound("sounds/hit.wav")

# ======================
# SETTINGS
# ======================

TILE = 28
MAP_W = 35
MAP_H = 25

WIDTH = MAP_W*TILE
HEIGHT = MAP_H*TILE+60

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tom & Jerry Maze")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None,30)
bigfont = pygame.font.SysFont(None,70)

# ======================
# IMAGES
# ======================

title_img = pygame.image.load("images/title.png")

jerry_img = pygame.transform.scale(
pygame.image.load("images/jerry.png"),(TILE,TILE))

lucky_img = pygame.transform.scale(
pygame.image.load("images/lucky.png"),(TILE,TILE))

tom_imgs=[
pygame.transform.scale(pygame.image.load("images/tom1.png"),(TILE,TILE)),
pygame.transform.scale(pygame.image.load("images/tom2.png"),(TILE,TILE)),
pygame.transform.scale(pygame.image.load("images/tom3.png"),(TILE,TILE)),
pygame.transform.scale(pygame.image.load("images/tom4.png"),(TILE,TILE))
]

win_img = pygame.image.load("images/win.png")
gameover_img = pygame.image.load("images/gameover.png")

# ======================
# MAPS
# ======================

MAP1=[
"###################################",
"#.............#...................#",
"#.#####.#####.#.#####.#####.#####.#",
"#.#...........#.....#...........#.#",
"#.#.#########.#####.#########.#.#.#",
"#.#.#.......................#.#.#.#",
"#...#.########.#####.######.#...#.#",
"###.#........#.....#......#.###.#.#",
"#...########.#.###.######.#.....#.#",
"#...........#...#.........#.....#.#",
"#.#########.###.#########.#.#####.#",
"#...........#.............#.......#",
"#.#########.#####.###############.#",
"#.#.............#...............#.#",
"#.#.###########.#.#############.#.#",
"#.#.............#...............#.#",
"#.#############.###############.#.#",
"#...............................#.#",
"#.#############.###############.#.#",
"#.............#.................#.#",
"#.###########.#.###############.#.#",
"#.............#.................#.#",
"#.#############.###############.#.#",
"#...............................#.#",
"###################################"
]

MAP2=[row[::-1] for row in MAP1]
MAP3=[row for row in MAP1]
MAP4=[row for row in MAP1]

MAPS=[MAP1,MAP2,MAP3,MAP4]

# ======================
# FUNCTIONS
# ======================

def is_wall(x,y):
    if x<0 or y<0 or x>=MAP_W or y>=MAP_H:
        return True
    return maze[y][x]=="#"


def bfs(start,target):

    queue=deque([start])
    visited={start:None}

    while queue:

        x,y=queue.popleft()

        if (x,y)==target:
            break

        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:

            nx=x+dx
            ny=y+dy

            if (nx,ny) not in visited and not is_wall(nx,ny):

                visited[(nx,ny)]=(x,y)
                queue.append((nx,ny))

    if target not in visited:
        return None

    path=[]
    cur=target

    while cur!=start:
        path.append(cur)
        cur=visited[cur]

    path.reverse()
    return path


def spawn_lucky():

    while True:

        x=random.randint(1,MAP_W-2)
        y=random.randint(1,MAP_H-2)

        if not is_wall(x,y):
            return(x,y)

# ======================
# START SCREEN
# ======================

def start_screen():

    while True:

        screen.blit(pygame.transform.scale(title_img,(WIDTH,HEIGHT)),(0,0))

        text=font.render("PRESS SPACE TO START",True,(255,255,255))
        screen.blit(text,(WIDTH//2-120,HEIGHT-80))

        pygame.display.flip()

        for e in pygame.event.get():

            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    return

# ======================
# GAME OVER
# ======================

def game_over_screen(score):

    while True:

        screen.blit(pygame.transform.scale(gameover_img,(WIDTH,HEIGHT)),(0,0))

        t2=font.render("Score: "+str(score),True,(255,255,255))
        t3=font.render("Press R to Restart",True,(255,255,255))

        screen.blit(t2,(WIDTH//2-60,HEIGHT-120))
        screen.blit(t3,(WIDTH//2-120,HEIGHT-80))

        pygame.display.flip()

        for e in pygame.event.get():

            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r:
                    return

# ======================
# WIN SCREEN
# ======================

def win_screen(score):

    while True:

        screen.blit(pygame.transform.scale(win_img,(WIDTH,HEIGHT)),(0,0))

        t2=font.render("Score: "+str(score),True,(255,255,255))
        t3=font.render("Press R to Play Again",True,(255,255,255))

        screen.blit(t2,(WIDTH//2-60,HEIGHT-120))
        screen.blit(t3,(WIDTH//2-120,HEIGHT-80))

        pygame.display.flip()

        for e in pygame.event.get():

            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r:
                    return

# ======================
# RESET GAME
# ======================

def reset_game():

    global maze,player_x,player_y
    global toms,dots,lucky
    global lives,score
    global extra_toms,extra_timer
    global jerry_speed,speed_timer,invincible_timer,clone,clone_timer

    maze=random.choice(MAPS)

    player_x=(MAP_W//2)*TILE
    player_y=(MAP_H//2)*TILE

    lives=2
    score=0

    jerry_speed=4

    speed_timer=0
    invincible_timer=0
    clone=None
    clone_timer=0

    dots=[]

    for y,row in enumerate(maze):
        for x,col in enumerate(row):
            if col==".":
                dots.append((x,y))

    lucky=spawn_lucky()

    toms=[
    {"x":1,"y":1,"img":random.choice(tom_imgs)},
    {"x":MAP_W-2,"y":MAP_H-2,"img":random.choice(tom_imgs)}
    ]

    extra_toms=[]
    extra_timer=0

# ======================
# START GAME
# ======================

start_screen()
reset_game()

tom_delay=15
tom_counter=0

# ======================
# GAME LOOP
# ======================

while True:

    clock.tick(60)

    for e in pygame.event.get():

        if e.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys=pygame.key.get_pressed()

    move_x=0
    move_y=0

    if keys[pygame.K_LEFT]: move_x=-jerry_speed
    if keys[pygame.K_RIGHT]: move_x=jerry_speed
    if keys[pygame.K_UP]: move_y=-jerry_speed
    if keys[pygame.K_DOWN]: move_y=jerry_speed

    new_x=player_x+move_x
    gx=new_x//TILE
    gy=player_y//TILE

    if not is_wall(gx,gy):
        player_x=new_x

    new_y=player_y+move_y
    gx=player_x//TILE
    gy=new_y//TILE

    if not is_wall(gx,gy):
        player_y=new_y

    gx=player_x//TILE
    gy=player_y//TILE

    # EAT DOT
    if (gx,gy) in dots:

        dots.remove((gx,gy))
        score+=10
        eat_sound.play()

        if len(dots)==0:

            win_screen(score)
            reset_game()
            continue

    # LUCKY
    if (gx,gy)==lucky:

        lucky_sound.play()

        r=random.randint(1,100)

        if r<=50:

            for i in range(len(toms)):
                extra_toms.append({
                "x":random.randint(1,MAP_W-2),
                "y":random.randint(1,MAP_H-2),
                "img":random.choice(tom_imgs)
                })

            extra_timer=pygame.time.get_ticks()+20000

        elif r<=65:

            jerry_speed=8
            speed_timer=pygame.time.get_ticks()+10000

        elif r<=70:

            lives+=1

        elif r<=80:

            clone=(gx,gy)
            clone_timer=pygame.time.get_ticks()+20000

        else:

            invincible_timer=pygame.time.get_ticks()+5000

        lucky=spawn_lucky()

    if speed_timer!=0 and pygame.time.get_ticks()>speed_timer:
        jerry_speed=4
        speed_timer=0

    if clone_timer!=0 and pygame.time.get_ticks()>clone_timer:
        clone=None
        clone_timer=0

    if extra_timer!=0 and pygame.time.get_ticks()>extra_timer:
        extra_toms=[]
        extra_timer=0

    all_toms=toms+extra_toms

    tom_counter+=1

    if tom_counter>tom_delay:

        tom_counter=0

        for tom in all_toms:

            target=(gx,gy)

            if clone:
                target=clone

            path=bfs((tom["x"],tom["y"]),target)

            if path:
                tom["x"],tom["y"]=path[0]

    # COLLISION
    for tom in all_toms:

        if tom["x"]==gx and tom["y"]==gy and pygame.time.get_ticks()>invincible_timer:

            hit_sound.play()

            lives-=1

            player_x=(MAP_W//2)*TILE
            player_y=(MAP_H//2)*TILE

            if lives<=0:

                game_over_screen(score)
                reset_game()

    # DRAW
    screen.fill((0,0,0))

    for y,row in enumerate(maze):
        for x,col in enumerate(row):

            if col=="#":
                pygame.draw.rect(screen,(0,0,255),(x*TILE,y*TILE,TILE,TILE))

    for d in dots:

        pygame.draw.circle(screen,(255,255,255),
        (d[0]*TILE+TILE//2,d[1]*TILE+TILE//2),4)

    screen.blit(lucky_img,(lucky[0]*TILE,lucky[1]*TILE))

    if clone:
        screen.blit(jerry_img,(clone[0]*TILE,clone[1]*TILE))

    for tom in all_toms:
        screen.blit(tom["img"],(tom["x"]*TILE,tom["y"]*TILE))

    screen.blit(jerry_img,(player_x,player_y))

    score_text=font.render("Score:"+str(score),True,(255,255,255))
    life_text=font.render("Lives:"+str(lives),True,(255,255,255))

    screen.blit(score_text,(10,HEIGHT-50))
    screen.blit(life_text,(200,HEIGHT-50))

    pygame.display.flip()
