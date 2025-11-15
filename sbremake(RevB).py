import pygame
import random
import sys

global screen, clock, running, phase_num
global s_img_ne, s_img_ns, s_img_nw, s_img_se, s_img_sw, s_img_we, s_img_hn, s_img_hs, s_img_hw, s_img_he, s_img_tn, s_img_ts, s_img_tw, s_img_te
global f_img
global b_img
global snd_move, snd_bite, snd_grow, snd_hit

global score, hiscore
global sc_tick, timer_mill

global player, prey, wall

NORTH = 1
WEST = 2
EAST = 3
SOUTH = 4

S_N = 1
S_W = 2
S_E = 3

N_S = 4
N_W = 5
N_E = 6

W_N = 7
W_E = 8
W_S = 9

E_N = 10
E_W = 11
E_S = 12

SCALER = 10

class snake:
    global s_img_ne, s_img_ns, s_img_nw, s_img_se, s_img_sw, s_img_we, s_img_hn, s_img_hs, s_img_hw, s_img_he, s_img_tn, s_img_ts, s_img_tw, s_img_te
    def __init__(self, x, y):
        self.length = 5
        self.x = x
        self.y = y
        self.heading = NORTH
        self.body = [ [self.x, self.y + 1, S_N], [self.x, self.y + 2, S_N], [self.x, self.y + 3, S_N], [self.x, self.y + 4, S_N] ]
        self.grow_count = 0

    def move(self):
        if self.heading == NORTH:
            self.y -= 1
            self.body.insert(0, [self.x, self.y + 1, S_N])
        elif self.heading == WEST:
            self.x -= 1
            self.body.insert(0, [self.x + 1, self.y, E_W])
        elif self.heading == EAST:
            self.x += 1
            self.body.insert(0, [self.x - 1, self.y, W_E])
        elif self.heading == SOUTH:
            self.y += 1
            self.body.insert(0, [self.x, self.y - 1, N_S])
        else:
            pass

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def move_forward(self):
        self.move()
        self.body.pop()

    def grow_forward(self):
        self.move()
        self.length += 1
        if self.grow_count > 0:
            self.grow_count -= 1

    def turn_left(self):
        if self.heading == NORTH:
            self.heading = WEST
            self.x -= 1
            self.body.insert(0, [self.x + 1, self.y, S_W])
        elif self.heading == WEST:
            self.heading = SOUTH
            self.y += 1
            self.body.insert(0, [self.x, self.y - 1, E_S])
        elif self.heading == SOUTH:
            self.heading = EAST
            self.x += 1
            self.body.insert(0, [self.x - 1, self.y, N_E])
        elif self.heading == EAST:
            self.heading = NORTH
            self.y -= 1
            self.body.insert(0, [self.x, self.y + 1, W_N])
        else:
            pass

    def move_left(self):
        self.turn_left()
        self.body.pop()

    def grow_left(self):
        self.turn_left()
        self.length += 1
        if self.grow_count > 0:
            self.grow_count -= 1

    def turn_right(self):
        if self.heading == NORTH:
            self.heading = EAST
            self.x += 1
            self.body.insert(0, [self.x - 1, self.y, S_E])
        elif self.heading == WEST:
            self.heading = NORTH
            self.y -= 1
            self.body.insert(0, [self.x, self.y + 1, E_N])
        elif self.heading == SOUTH:
            self.heading = WEST
            self.x -= 1
            self.body.insert(0, [self.x + 1, self.y, N_W])
        elif self.heading == EAST:
            self.heading = SOUTH
            self.y += 1
            self.body.insert(0, [self.x, self.y - 1, W_S])
        else:
            pass

    def move_right(self):
        self.turn_right()
        self.body.pop()

    def grow_right(self):
        self.turn_right()
        self.length += 1
        if self.grow_count > 0:
            self.grow_count -= 1

    def set_grow_count(self, count):
        self.grow_count = count

    def is_growing(self):
        if self.grow_count > 0:
            return True
        else:
            return False

    def does_this_eat_fruit(self, x, y):
        if self.x == x and self.y == y:
            return True
        else:
            return False

    def does_this_bite_itself(self):
        for body in self.body:
            if self.x == body[0] and self.y == body[1]:
                return True
        return False

    def draw(self, screen):
        if self.heading == NORTH:
            head = s_img_hn
        elif self.heading == WEST:
            head = s_img_hw
        elif self.heading == EAST:
            head = s_img_he
        elif self.heading == SOUTH:
            head = s_img_hs
        else:
            head = None
        screen.blit(head, (self.x * SCALER, self.y * SCALER))
        for i, body in enumerate(self.body):
            if i == self.length-2:
                if body[2] == S_N or body[2] == W_N or body[2] == E_N:
                    seg = s_img_ts
                elif body[2] == N_S or body[2] == W_S or body[2] == E_S:
                    seg = s_img_tn
                elif body[2] == N_W or body[2] == E_W or body[2] == S_W:
                    seg = s_img_te
                elif body[2] == N_E or body[2] == W_E or body[2] == S_E:
                    seg = s_img_tw
                else:
                    print("draw #1: %d" % body[2])
            else:
                if body[2] == S_N or body[2] == N_S:
                    seg = s_img_ns
                elif body[2] == W_E or body[2] == E_W:
                    seg = s_img_we
                elif body[2] == S_E or body[2] == E_S:
                    seg = s_img_se
                elif body[2] == W_S or body[2] == S_W:
                    seg = s_img_sw
                elif body[2] == W_N or body[2] == N_W:
                    seg = s_img_nw
                elif body[2] == E_N or body[2] == N_E:
                    seg = s_img_ne
                else:
                    #seg = None
                    print("draw #2: %d" % body[2])
            screen.blit(seg, ( body[0] * SCALER, body[1] * SCALER))

class fruit:
    global f_img
    def __init__(self):
        self.x = 0
        self.y = 0

    def random_drop(self, s:snake):
        while True:
            fx = random.randrange(1, 59)
            fy = random.randrange(1, 59)
            cross_flag = False
            for body in s.body:
                if body[0] == fx and body[1] == fy:
                    cross_flag = True
                    break
            if cross_flag == False:
                break
        self.x = fx
        self.y = fy

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def draw(self, screen):
        screen.blit(f_img, (self.x * SCALER, self.y * SCALER))

class block:
    global b_img
    def __init__(self):
        self.pos = []
    
    def make_bound_block(self):
        for i in range(0, 60):
            self.pos.append((i, 0))
            self.pos.append((i, 59))
            self.pos.append((0, i))
            self.pos.append((59, i))
    
    def does_this_hit(self, x, y):
        if (x, y) in self.pos:
            return True
        return False

    def draw(self, screen):
        for (x, y) in self.pos:
            screen.blit(b_img, (x * SCALER, y * SCALER))

def game_init():

    global phase_num, screen, clock, score, hiscore, running, sc_tick, timer_mill
    global player, prey, wall
    global s_img_ne, s_img_ns, s_img_nw, s_img_se, s_img_sw, s_img_we, s_img_hn, s_img_hs, s_img_hw, s_img_he, s_img_tn, s_img_ts, s_img_tw, s_img_te
    global f_img
    global b_img
    global snd_move, snd_bite, snd_grow, snd_hit

    screen_width = 800
    screen_height = 600

    pygame.init()
    pygame.font.init()

    pygame.display.set_caption("SNAKE BYTE Remake")
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    score_font = pygame.font.Font(None, 30)

    running = True
    phase_num = 1

    s_img_ne = pygame.image.load("images/ne.png")
    s_img_ns = pygame.image.load("images/ns.png")
    s_img_nw = pygame.image.load("images/nw.png")
    s_img_se = pygame.image.load("images/se.png")
    s_img_sw = pygame.image.load("images/sw.png")
    s_img_we = pygame.image.load("images/we.png")
    s_img_hn = pygame.image.load("images/hn.png")
    s_img_hs = pygame.image.load("images/hs.png")
    s_img_hw = pygame.image.load("images/hw.png")
    s_img_he = pygame.image.load("images/he.png")
    s_img_tn = pygame.image.load("images/tn.png")
    s_img_ts = pygame.image.load("images/ts.png")
    s_img_tw = pygame.image.load("images/tw.png")
    s_img_te = pygame.image.load("images/te.png")    

    f_img = pygame.image.load("images/fruit.png")

    b_img = pygame.image.load("images/block2.png")

    snd_move = pygame.mixer.Sound("sound/sharp.mp3")
    snd_bite = pygame.mixer.Sound("sound/chippy.mp3")
    snd_grow = pygame.mixer.Sound("sound/harsh.mp3")
    snd_hit = pygame.mixer.Sound("sound/movinghit.mp3")

    score = hiscore = 0
    sc_tick = 5
    timer_mill = 200


def title():

    global screen, clock, score, hiscore, phase_num

    screen.fill("black")

    title_font = pygame.font.Font(None, 40)
    title_text = title_font.render('SNAKE BYTE Remake', True, (255, 255, 155))
    title_text_rect = title_text.get_rect(center = (400, 300))

    in_title = True
    pstart_font = pygame.font.Font(None, 28)
    pstart_text = pstart_font.render('Press any to start', True, (255, 255, 55))
    pstart_text_rect = pstart_text.get_rect(center = (400, 540))

    screen.blit(title_text, title_text_rect)
    screen.blit(pstart_text, pstart_text_rect)

    score = 0

    while in_title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_title = False
                phase_num = 255
            elif event.type == pygame.KEYDOWN:
                in_title = False
                phase_num = 3
        pygame.display.flip()
        clock.tick(60)


def gameover():
    global screen, clock, phase_num
    global score, sc_tick, timer_mill

    in_gameover = True

    pgameover_font = pygame.font.Font(None, 28)
    pgameover_text = pgameover_font.render('Game Over', True, (255, 255, 55))
    pgameover_text_rect = pgameover_text.get_rect(center = (300, 240))

    ppsk_font = pygame.font.Font(None, 20)
    ppsk_text = ppsk_font.render('Press Space key to restart', True, (255, 255, 155))
    ppsk_text_rect = ppsk_text.get_rect(center = (300, 360))

    score = 0
    sc_tick = 5
    timer_mill = 200

    while in_gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_gameover = False
                phase_num = 255
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_gameover = False
                    phase_num = 1
        screen.blit(pgameover_text, pgameover_text_rect)
        screen.blit(ppsk_text, ppsk_text_rect)
        pygame.display.flip()
        clock.tick(60)


def stage():
    global phase_num, screen, clock, score, hiscore, sc_tick, timer_mill
    global player, prey, wall
    global snd_move, snd_bite, snd_grow, snd_hit

    player = snake(30,30)
    prey = fruit()
    wall = block()

    hiscore_font = pygame.font.Font(None, 22)
    hiscore_text = hiscore_font.render(f'Hi-Score: {hiscore}', True, (255, 255, 200))
    hiscore_rect = hiscore_text.get_rect(center = (680, 80))

    score_font = pygame.font.Font(None, 22)
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 200))
    score_rect = score_text.get_rect(center = (680, 40))

    wall.make_bound_block()
    prey.random_drop(player)
    in_pause = False
    in_stage = True

    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT, timer_mill)

    inkey = 0
    while in_stage:
        #inkey = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_stage = False
                phase_num = 255
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    inkey = 1
                elif event.key == pygame.K_RIGHT:
                    inkey = 2
                elif event.key == pygame.K_ESCAPE:
                    in_pause = True
                    while in_pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                in_pause = False
            elif event.type == TIMEREVENT:
                if inkey == 1:
                    if player.is_growing() == True:
                        player.grow_left()
                        snd_grow.play()
                    else:
                        player.move_left()
                        snd_move.play()
                    inkey = 0
                elif inkey == 2:
                    if player.is_growing() == True:
                        player.grow_right()
                        snd_grow.play()
                    else:
                        player.move_right()
                        snd_move.play()
                    inkey = 0
                else:
                    if player.is_growing() == True:
                        player.grow_forward()
                        snd_grow.play()
                    else:     
                        player.move_forward()
                        snd_move.play()
                    inkey = 0
        if player.does_this_eat_fruit(prey.get_x(), prey.get_y()):
            score += 10
            snd_bite.play()
            prey.random_drop(player)
            player.set_grow_count(5)
            sc_tick += 1
            if sc_tick > 60:
                sc_tick = 60
            timer_mill -= 10
            if timer_mill < 50:
                timer_mill = 50
            pygame.time.set_timer(TIMEREVENT, timer_mill)
        screen.fill("black")
        score_text = score_font.render(f'Score: {score}', True, (255, 255, 200))
        if score > hiscore:
            hiscore = score
            hiscore_text = hiscore_font.render(f'Hi-Score: {hiscore}', True, (255, 255, 200))
        screen.blit(hiscore_text, hiscore_rect)
        screen.blit(score_text, score_rect)
        wall.draw(screen)
        prey.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        if wall.does_this_hit(player.get_x(), player.get_y()):
            snd_hit.play()
            if score > hiscore:
                hiscore = score
            in_stage = False
            phase_num = 0
            pygame.time.set_timer(TIMEREVENT, 0)
        if player.does_this_bite_itself() == True:
            snd_hit.play()
            if score > hiscore:
                hiscore = score
            in_stage = False
            phase_num = 0
            pygame.time.set_timer(TIMEREVENT, 0)
        clock.tick(60)


def main():

    global phase_num, running

    game_init()
    while running:
        if phase_num == 0:
            gameover()
        elif phase_num == 1:
            title()
        elif phase_num == 2:
            pass
        elif phase_num == 3:
            stage()
        elif phase_num == 4:
            running = False
        else:
            running = False
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
