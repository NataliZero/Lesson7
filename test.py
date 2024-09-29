import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
width, height = 300, 600
block_size = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Тетрис')

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Фигуры тетромино
tetromino_shapes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

# Создание сетки
game_grid = [[0 for _ in range(10)] for _ in range(20)]  # Изменено имя на game_grid


# Класс для блоков тетромино
class Tetromino:
    def __init__(self):
        self.shape = random.choice(tetromino_shapes)
        self.color = random.choice([RED, GREEN, BLUE])
        self.x = 3
        self.y = 0

    def rotate(self):
        # Вращение фигуры по часовой стрелке
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


# Проверка столкновений
def check_collision(grid, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell and (tetromino.y + y >= len(grid) or tetromino.x + x < 0 or tetromino.x + x >= len(grid[0]) or
                         grid[tetromino.y + y][tetromino.x + x]):
                return True
    return False


# Добавление тетромино в сетку
def merge_tetromino(grid, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color


# Удаление заполненных строк
def remove_full_rows(grid):
    rows_to_remove = [i for i, row in enumerate(grid) if all(row)]
    for i in rows_to_remove:
        del grid[i]
        grid.insert(0, [0 for _ in range(10)])
    return len(rows_to_remove)


# Основной игровой цикл
def game():
    clock = pygame.time.Clock()
    tetromino = Tetromino()
    running = True
    speed = 500  # Скорость падения
    last_move = pygame.time.get_ticks()

    while running:
        screen.fill(BLACK)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обработка клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetromino.x -= 1
                    if check_collision(game_grid, tetromino):  # Проверка на столкновение
                        tetromino.x += 1
                if event.key == pygame.K_RIGHT:
                    tetromino.x += 1
                    if check_collision(game_grid, tetromino):  # Проверка на столкновение
                        tetromino.x -= 1
                if event.key == pygame.K_DOWN:
                    tetromino.y += 1
                    if check_collision(game_grid, tetromino):  # Проверка на столкновение
                        tetromino.y -= 1
                if event.key == pygame.K_UP:
                    tetromino.rotate()
                    if check_collision(game_grid, tetromino):  # Проверка на столкновение
                        tetromino.rotate()  # Отменяем вращение при столкновении

        # Падение тетромино по таймеру
        if pygame.time.get_ticks() - last_move > speed:
            tetromino.y += 1
            if check_collision(game_grid, tetromino):
                tetromino.y -= 1
                merge_tetromino(game_grid, tetromino)
                remove_full_rows(game_grid)
                tetromino = Tetromino()
                if check_collision(game_grid, tetromino):
                    running = False  # Игра окончена
            last_move = pygame.time.get_ticks()

        # Рисуем сетку и тетромино
        for y, row in enumerate(game_grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * block_size, y * block_size, block_size, block_size))

        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, tetromino.color, (
                    (tetromino.x + x) * block_size, (tetromino.y + y) * block_size, block_size, block_size))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    game()
