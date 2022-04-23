import pygame

#I made a change

#Game Settings
fps = 150
clock = pygame.time.Clock()
screen_width = 500
screen_height = 700

#Colors
red, green, blue = (255, 0, 0), (0, 100, 20), (0, 0, 55)

#Variables
left_side = 0
right_side = screen_width
top_side = 0
bottom_side = screen_height

#Initialize Pygame
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Pong x Space Invades")


class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        if self.vx >= 2:
            self.vx = 2
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen, red, [self.x, self.y], 5)

    def bounce(self):
        if self.x > right_side or self.x < left_side:
            self.vx = -self.vx
            if self.x > right_side - 5:
                self.x = right_side
            elif self.x < left_side + 5:
                self.x = left_side
        if self.y >= bottom_side or self.y <= top_side:
            self.vy = -self.vy
        if player1.y + player1.height > self.y > player1.y and player1.x < self.x < player1.x + player1.width:
            self.vy = -self.vy
            self.vx += player1.vx / 2


class Player:
    def __init__(self, width, height, x, y, vx, vy):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def draw_player(self):
        pygame.draw.rect(screen, blue, pygame.Rect(self.x, self.y, self.width, self.height))

    def calc_accel(self, v):
        if -0.1 < self.vx < 0.1:
            self.vx = 0
        if v == 0:
            if self.vx > 0:
                self.vx -= 0.1
            elif self.vx < 0:
                self.vx += 0.1
        else:
            self.vx += v

    def move_player(self):
        if self.x < left_side:
            self.x = left_side
            self.vx = 0
        elif self.x > right_side - self.width:
            self.x = right_side - self.width
            self.vx = 0
        else:
            self.x += self.vx


class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, green, pygame.Rect(self.x, self.y, self.width, self.height))

    def hit(self):
        for ball in balls:
            #Hit under side
            if self.x + 2 < ball.x < self.x + self.width - 2 and self.y + self.height > ball.y > self.y + self.height - 5:
                print("Hit under")
                ball.vy = -ball.vy
                return True
            #Hit left side
            if self.x + self.width - 5 < ball.x < self.x + self.width and self.y < ball.y < self.y + self.height:
                print("Hit right")
                ball.vx = -ball.vx
                return True
            #Hit right side
            if self.x < ball.x < self.x + 5 and self.y < ball.y < self.y + self.height:
                print("Hit left")
                ball.vx = -ball.vx
                return True
            #Hit top side
            if self.x + 2 < ball.x < self.x + self.width - 2 and self.y < ball.y < self.y + 5:
                print("Hit top")
                ball.vy = -ball.vy
                return True
            else:
                return False


#Create stuff
player1 = Player(60, 10, 250, 640, 0, 0)
balls = [Ball(200, 400, 1, 1)]
blocks = []
for iy in range(2):
    for ix in range(20):
        blocks.append(Block(ix*20, iy*20 + 500, 20, 20))

#Main loop 123
run = True
while run:
    clock.tick(fps)
    screen.fill((0, 0, 0))

    # Player | Draw, send key input, calculate acceleration and move player
    player1.draw_player()
    keys = pygame.key.get_pressed()
    player1.calc_accel((keys[pygame.K_d] - keys[pygame.K_a]) / 10)
    player1.move_player()

    #Balls | Go through all balls, draw, bounce and move
    for ball in balls:
        ball.move()
        ball.draw()
        ball.bounce()

    #Blocks | Go through all blocks, draw and check if hit by ball
    for i, block in enumerate(blocks):
        block.draw()
        if block.hit():
            del blocks[i]

    #Uppdate display after all drawing is done
    pygame.display.update()

    #Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(100, 100, 1, 1))
