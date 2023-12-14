import pygame
import sys

# Инициализация Pygame
pygame.init()

# Инициализация звука стрельбы
shooting_sound = pygame.mixer.Sound("55.mp3") 
 
# Получение размеров экрана
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Дарбанов Бекбо")

# Загрузка изображения фона
background_image = pygame.image.load("152.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Определение цветов
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Определение игрового объекта - игрока
player_width = 99
player_height = 100
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 10
player_speed = 10 

# Загрузка и масштабирование изображения игрока
player_image = pygame.image.load("2.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Определение пули
bullet_width = 5
bullet_height = 20
bullet_color = red
bullet_speed = 7
bullets = []

# Определение врагов
enemy_width = 90
enemy_height = 90
enemy_speed = 3
enemies = []

# Загрузка и масштабирование изображения врага
enemy_image = pygame.image.load("787.png")
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

# Счет и шрифт для отображения
score = 0
font = pygame.font.Font(None, 36)

# Функция отрисовки игрока
def draw_player(x, y):
    screen.blit(player_image, (x, y))

# Функция отрисовки пуль
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, bullet)

# Функция отрисовки врагов
def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

# Отображение счета на экране
def draw_score(score):
    score_text = font.render("Score: " + str(score), True, red)
    screen.blit(score_text, (10, 10))

# Проверка столкновения врагов с игроком
def check_collision(enemies, player_x, player_y, player_width, player_height):
    for enemy in enemies:
        if (
            player_x < enemy.x + enemy.width
            and player_x + player_width > enemy.x
            and player_y < enemy.y + enemy.height
            and player_y + player_height > enemy.y
        ):
            return True
    return False

# Проверка столкновения пуль с врагами
def check_bullet_collision(bullets, enemies):
    global score
    bullets_to_remove = []

    for bullet in bullets:
        for enemy in enemies:
            if (
                bullet.x < enemy.x + enemy.width
                and bullet.x + bullet.width > enemy.x
                and bullet.y < enemy.y + enemy.height
                and bullet.y + bullet.height > enemy.y
            ):
                bullets_to_remove.append(bullet)
                enemies.remove(enemy)
                score += 1

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Обработка стрельбы при нажатии пробела
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.mixer.Sound.play(shooting_sound)
            bullet_x = player_x + (player_width - bullet_width) // 2
            bullet_y = player_y
            bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Движение пуль вверх
    for bullet in bullets:
        bullet.y -= bullet_speed

    # Движение врагов вниз
    for enemy in enemies:
        enemy.y += enemy_speed

    # Генерация нового врага
    if pygame.time.get_ticks() % 50 == 0:
        enemy_x = pygame.time.get_ticks() % screen_width
        enemy_y = 0
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

    # Проверка столкновения врагов с игроком
    if check_collision(enemies, player_x, player_y, player_width, player_height):
        pygame.quit()
        sys.exit()

    # Проверка столкновения пуль с врагами
    check_bullet_collision(bullets, enemies)

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка экрана
    draw_player(player_x, player_y)
    draw_bullets(bullets)
    draw_enemies(enemies)
    draw_score(score)

    # Обновление экрана
    pygame.display.flip()

    # Задержка для контроля частоты обновления экрана
    pygame.time.Clock().tick(60)