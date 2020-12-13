import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# просто цвета для блоков, каждый массив - оттенки одного цвета
colors_list = [[(80, 255, 80), (57, 255, 33), (19, 242, 8), (16, 199, 0), (27, 131, 0)],
               [(162, 255, 255), (110, 255, 255), (16, 243, 239), (11, 191, 178), (8, 134, 140)],
               [(121, 135, 255), (63, 62, 255), (21, 16, 250), (8, 12, 159), (8, 8, 115)],
               [(255, 117, 255), (255, 12, 255), (234, 0, 203), (214, 0, 181), (132, 0, 107)],
               [(255, 110, 88), (255, 29, 22), (255, 0, 0), (228, 0, 0), (150, 0, 0)]]
# выбираем один случайный цвет для блоков
color_list = random.choice(colors_list)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("arkanoid")
clock = pygame.time.Clock()


# класс для ракетки
class Board(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0

    def update(self):
        # движение по нажатию
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx -= 1
        elif keystate[pygame.K_RIGHT]:
            self.speedx += 1
        elif self.speedx > 0:
            self.speedx -= .25
        elif self.speedx < 0:
            self.speedx += .25
        self.rect.x += self.speedx

        # останавка ракетки на краях экрана
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = int(-self.speedx * .25)
        elif self.rect.left < 0:
            self.rect.left = 0
            self.speedx = int(-self.speedx * .25)


# класс для мячика
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.radius = 5
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 40
        self.speedx = random.choice([4, -4])
        self.speedy = 5

    def update(self):
        # отбиваем мяч от края экрана
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
        elif self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.top < 0:
            self.speedy = -self.speedy

        # если игрок не отбил мяч, удаляем его
        if self.rect.top > HEIGHT:
            self.kill()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def collide(self, hit):
        # определяем в какую сторону блока/ракетки ударился мяч
        if self.speedx > 0:
            dx = self.rect.right - hit.rect.left
        else:
            dx = hit.rect.right - self.rect.left
        if self.speedy > 0:
            dy = self.rect.bottom - hit.rect.top
        else:
            dy = hit.rect.bottom - self.rect.top

        if dx == dy:
            self.speedx, self.speedy = -self.speedx, -self.speedy
        elif dx > dy:
            self.reflect('y')
        elif dy > dx:
            self.reflect('x')

    def reflect(self, side):
        # отражаем мяч и меняем его траекторию с шансом 40%
        chance = random.random()
        if side == 'x':
            self.speedx = -self.speedx
            if chance < .2 and (3 <= self.speedy < 6 or -6 < self.speedy <= -3) \
                    and (3 < self.speedx <= 6 or -6 <= self.speedx <= -3):
                if self.speedy > 0:
                    self.speedy += 1
                else:
                    self.speedy += -1
                if self.speedx > 0:
                    self.speedx -= 1
                else:
                    self.speedx -= -1
            elif chance > .8 and (3 < self.speedy <= 6 or -6 <= self.speedy < -3) \
                    and (3 <= self.speedx < 6 or -6 < self.speedx <= -3):
                if self.speedy > 0:
                    self.speedy -= 1
                else:
                    self.speedy -= -1
                if self.speedx > 0:
                    self.speedx += 1
                else:
                    self.speedx += -1
        elif side == 'y':
            self.speedy = -self.speedy
            if chance < .2 and (3 <= self.speedx < 6 or -6 < self.speedx <= -3) \
                    and (3 < self.speedy <= 6 or -6 < self.speedy <= -3):
                if self.speedx > 0:
                    self.speedx += 1
                else:
                    self.speedx += -1
                if self.speedy > 0:
                    self.speedy -= 1
                else:
                    self.speedy -= -1
            elif chance > .8 and (3 < self.speedx <= 6 or -6 <= self.speedx < -3) \
                    and (3 <= self.speedy < 6 or -6 <= self.speedy < -3):
                if self.speedx > 0:
                    self.speedx -= 1
                else:
                    self.speedx -= -1
                if self.speedy > 0:
                    self.speedy += 1
                else:
                    self.speedy += -1


# класс для блока
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 15))
        self.image.fill(random.choice(color_list))
        self.rect = self.image.get_rect()
        self.rect.x = 92 + (9 + self.rect.width) * x
        self.rect.y = 70 + (9 + self.rect.height) * y


# создаем группы и добавляем в них спрайты мяча и ракетки
all_sprites = pygame.sprite.Group()
board = pygame.sprite.GroupSingle(Board())
ball = Ball()
all_sprites.add(ball)

# генерируем блоки
blocks = pygame.sprite.Group()
for x in range(16):
    for y in range(8):
        block = Block(x, y)
        all_sprites.add(block)
        blocks.add(block)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    board.update()

    # обработка столкновения мяча с блоками
    hits = pygame.sprite.spritecollide(ball, blocks, True)
    if hits:
        for hit in hits:
            ball.collide(hit)

    # обработка столкновения мяча с ракеткой
    hits = pygame.sprite.spritecollide(ball, board, False)
    if hits:
        for hit in hits:
            ball.collide(hit)

    # если мяч ушел с экрана игра заканчивается((
    if not ball.alive():
        running = False

    # отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)
    board.draw(screen)

    pygame.display.flip()

pygame.quit()