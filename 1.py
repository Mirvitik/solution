import pygame
import os
import sys

clock = pygame.time.Clock()
pygame.init()
WIDTH, HEIGHT = size = 500, 500
screen = pygame.display.set_mode(size)
hero_sprite = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


FPS = 50
c_x = 0
c_y = 0


def terminate():
    pygame.quit()
    sys.exit()


class Grass(pygame.sprite.Sprite):
    image = load_image('grass.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.transform.scale(Grass.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += c_x
        self.rect.y += c_y


class Hero(pygame.sprite.Sprite):
    image = load_image('mar.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.image = pygame.transform.scale(Hero.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Box(pygame.sprite.Sprite):
    image = load_image('box.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.image = pygame.transform.scale(Box.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += c_x
        self.rect.y += c_y


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    pygame.display.set_caption('Введите имя файла')
    screen.fill(pygame.Color('black'))
    running = True
    try:
        l = load_level(input('Введите имя файла с уровнем: '))
    except Exception as e:
        print('Такого файла нет в папке data')
        sys.exit()
    pygame.display.set_caption('Перемещение героя')
    start_screen()
    for y in range(len(l)):
        for x in range(len(l[y])):
            if l[y][x] == '.' or l[y][x] == '@':
                Grass(all_sprites, x * 50, y * 50)
            if l[y][x] == '@':
                player = Hero(hero_sprite, x * 50, y * 50)
            if l[y][x] == '#':
                Box(all_sprites, x * 50, y * 50)
    while running:
        all_sprites.update()
        hero_sprite.update()
        c_x = 0
        c_y = 0
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_UP]:
                c_y = 50
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                c_y = -50
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                c_x = 50
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                c_x = -50
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        hero_sprite.draw(screen)
        pygame.display.flip()
    pygame.quit()
