import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
DARK_GREEN = (0, 150, 0)

# Настройки окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка | Парное программирование")
clock = pygame.time.Clock()

# Шрифты для счета
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Функция для отображения счета
def display_score(score):
    value = score_font.render("Очки: " + str(score), True, BLACK)
    screen.blit(value, [10, 10])

# Функция для отрисовки змейки (списка сегментов)
def draw_snake(segment_size, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, DARK_GREEN, [segment[0], segment[1], segment_size, segment_size])

# Функция вывода сообщения (например, "Game Over")
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])

# --- ОСНОВНАЯ ФУНКЦИЯ ИГРЫ ---
def game_loop():
    # Начальные координаты змейки (центр экрана)
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    # Шаг движения
    x_change = 0
    y_change = 0

    # Тело змейки
    snake_list = []
    snake_length = 1

    # Позиция еды
    food_x = round(random.randrange(0, SCREEN_WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE

    game_over = False
    game_close = False

    # Главный цикл
    while not game_over:

        # Экран "Game Over" (ожидание нажатия)
        while game_close == True:
            screen.fill(WHITE)
            message("Ты проиграл! Нажми C-Играть или Q-Выйти", RED)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop() # Рестарт

        # Обработка нажатий клавиш (движение)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0: # Нельзя пойти вправо, если идешь влево
                    x_change = -CELL_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = CELL_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -CELL_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = CELL_SIZE
                    x_change = 0

        # Проверка столкновения со стенами
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True

        # Движение головы
        x += x_change
        y += y_change

        # Отрисовка фона
        screen.fill(BLUE)

        # Отрисовка еды
        pygame.draw.rect(screen, RED, [food_x, food_y, CELL_SIZE, CELL_SIZE])

        # Логика роста змейки
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка удара о собственный хвост
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Отрисовка змейки
        draw_snake(CELL_SIZE, snake_list)

        # Отображение счета
        display_score(snake_length - 1)

        # Обновление экрана
        pygame.display.update()

        # Проверка съедания еды
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            snake_length += 1

        # Скорость игры (чем меньше число, тем медленнее)
        clock.tick(10)

    # Выход из игры
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()