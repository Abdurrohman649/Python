import pygame
import time
import random
import os

pygame.init()

# Цвета
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (169, 169, 169)

# Разрешение экрана
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by ChatGPT')

# Настройки игры
snake_block = 20
initial_snake_speed = 10
speed_increase = 1
level_up_score = 5
background_color = blue

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 35)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("comicsansms", 45)

# Звуки
eat_sound = pygame.mixer.Sound("eat_sound.wav")
collision_sound = pygame.mixer.Sound("collision_sound.wav")
game_over_sound = pygame.mixer.Sound("game_over_sound.wav")

# Системы рекордов
highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0


def save_highscore(score):
    global high_score
    if score > high_score:
        high_score = score
        with open(highscore_file, "w") as f:
            f.write(str(high_score))


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])


def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_offset])


def game_over_screen(score):
    dis.fill(blue)
    message("You Lost! Press Q-Quit or C-Play Again", red)
    message(f"High Score: {high_score}", gray, 40)
    your_score(score)
    pygame.display.update()
    game_over_sound.play()


def main_menu():
    dis.fill(blue)
    message("Welcome to Snake Game!", yellow, -50)
    message("Press P to Play", green)
    message("Press Q to Quit", red, 50)
    pygame.display.update()


def settings_screen():
    global snake_block, initial_snake_speed, background_color

    dis.fill(blue)
    message("Settings", yellow, -50)
    message(f"Speed: {initial_snake_speed}", green)
    message(f"Block Size: {snake_block}", green, 50)
    message("Press A to Increase Speed, D to Decrease", red, 100)
    message("Press W to Increase Block Size, S to Decrease", red, 150)
    message("Press B to Change Background Color", red, 200)
    message("Press P to Play", green, 250)
    pygame.display.update()


def preview_settings():
    dis.fill(blue)
    message("Preview Settings", yellow, -50)
    message(f"Speed: {initial_snake_speed}", green)
    message(f"Block Size: {snake_block}", green, 50)
    message(f"Background Color: {background_color}", green, 100)
    pygame.display.update()
    time.sleep(2)


def gameLoop():
    global snake_block, initial_snake_speed, background_color, high_score

    game_over = False
    game_close = False

    # Начальные координаты змейки
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Положение еды
    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    # Начальный уровень сложности
    snake_speed = initial_snake_speed
    score = 0

    while not game_over:

        while game_close:
            game_over_screen(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_a:  # Увеличить скорость
                    initial_snake_speed += 1
                    preview_settings()
                elif event.key == pygame.K_d:  # Уменьшить скорость
                    initial_snake_speed = max(1, initial_snake_speed - 1)
                    preview_settings()
                elif event.key == pygame.K_w:  # Увеличить размер блока
                    snake_block += 5
                    preview_settings()
                elif event.key == pygame.K_s:  # Уменьшить размер блока
                    snake_block = max(10, snake_block - 5)
                    preview_settings()
                elif event.key == pygame.K_b:  # Изменить цвет фона
                    background_color = random.choice([blue, green, red, yellow, gray])
                    preview_settings()

        # Проверка на выход за границы
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(background_color)

        # Рисуем еду
        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])

        # Добавляем голову змейки
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        # Обновляем экран
        pygame.display.update()

        # Проверка на съеденную еду
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 1
            snake_speed += speed_increase
            eat_sound.play()

        if score % level_up_score == 0 and score != 0:
            message("Level Up!", green, 100)
            pygame.display.update()
            time.sleep(1)

        # Если счет больше рекорда, сохраняем его
        save_highscore(score)

        # Устанавливаем скорость игры
        clock = pygame.time.Clock()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


# Основной цикл
while True:
    main_menu()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                settings_screen()
                gameLoop()
            elif event.key == pygame.K_q:
                pygame.quit()
                quit()
