import pgzrun
from pgzero.builtins import *  # Работает и без этого импорта, но IDE будет подчеркивать кучу ошибок.
from pgzero.actor import Actor
from random import randint, choice


TITLE = "Тестовое Python Base (Анастасия)"
WIDTH = 500
HEIGHT = 400
FPS = 30


# ---- Состояния игры ----
game_state = "menu"  # menu / game / win / gameover
mouse_pos = (0, 0)   # текущая позиция мыши


# ---- Настройки звука ----
music_on = False


# ---- Кнопки меню ----
buttons = [
    ("играть", Rect((WIDTH/2-90, 90), (180, 50)), "start"),
    ("музыка вкл/выкл", Rect((WIDTH/2-90, 160), (180, 50)), "music"),
    ("выход",       Rect((WIDTH/2-90, 230), (180, 50)), "exit"),
]


# ---- Создание кошек ----
def make_enemy(tracks):
    # выбираем случайную дорогу
    track = choice(tracks)
    # создаем кошку в случайном месте на этой дороге
    enemy = Actor("cat/0", (30+120*track, randint(100,400)))
    # сохраняем за кошкой дорогу
    enemy.track = track
    # удаляем дорогу из списка
    tracks.remove(track)
    # задаем кошке случайную скорость
    enemy.speed = randint(3, 6)
    enemy.time = 0
    return enemy, tracks

tracks = [1, 2, 3]
enemies = []
for i in range(3):
    enemy, tracks = make_enemy(tracks)
    enemies.append(enemy)


# ---- Загрузка изображений ----
#bg = Actor("bg1_darker")
hero = Actor("mouse/0", center=(30, HEIGHT/2))
hero.time = 0
cheese = Actor("cheese_half")
cheese.pos = (WIDTH-30, HEIGHT/2)


def draw():

    if game_state == "menu":
        screen.blit("background", (0, 0))
        # ---- Рисуем кнопки ----
        for text, rect, action in buttons:
            hover = rect.collidepoint(mouse_pos)
            color = (100, 220, 255) if not hover else (255, 215, 0)
            screen.draw.filled_rect(rect, (10, 10, 20))
            screen.draw.rect(rect, color)
            screen.draw.text(text, center=rect.center, fontsize=26, color=color)

    elif game_state == "game":
        screen.surface.fill("lavenderblush")
        for enemy in enemies:
            enemy.draw()
        cheese.draw()
        hero.draw()

# ---- Победа и поражение ----
    if game_state == "gameover":
        screen.draw.text("GAME OVER\nТы накормил кошку :)",
                         fontsize=40,
                         center=(WIDTH//2, HEIGHT//2),
                         color="darkred")

    if game_state == "win":
        #screen.clear()
        #hero.draw()
        cheese.draw()
        screen.draw.text("YOU WIN\nТы накормил мышку :)",
                         fontsize=40,
                         center=(WIDTH//2, HEIGHT//2),
                         color="seagreen")


# ---- Взаимодействия с кнопками ----
def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos


def on_mouse_down(pos):
    global game_state, music_on

    if game_state == "menu":
        for text, rect, action in buttons:
            if rect.collidepoint(pos):
                if action == "start": game_state = "game"
                if action == "music": music_on = not music_on
                if music_on:
                    music.play("music")
                else:
                    music.stop()
                if action == "exit": exit()


def update(dt): # dt - это время, прошедшее между кадрами
    global tracks, game_state, enemy

    if game_state == "game":
# ---- Анимация персонажей ----
        hero.time = hero.time + dt
        if hero.time > 0.1:
            hero.time = 0
            number = int(hero.image.split('/')[-1])
            hero.image = f'mouse/{(number + 1) % 4}'

        enemy.time = enemy.time + dt
        if enemy.time > 0.1:
            enemy.time = 0
            number = int(enemy.image.split('/')[-1])
            enemy.image = f'cat/{(number + 1) % 9}'


# ---- Движение мышки ----
        if keyboard.UP:
            hero.y -= 5
        elif keyboard.DOWN:
            hero.y += 5
        if keyboard.LEFT:
           if hero.x > 50:
               hero.x -= 5
        if keyboard.RIGHT:
            if hero.x < WIDTH - 50:
                hero.x += 5

# ---- Движение кошки ----
        for enemy in enemies:
            enemy.y -= enemy.speed
            # кошка исчезла, если ее нижняя часть меньше 0
            if enemy.bottom < 0:
            # добавляем дорогу кошки обратно в дороги
                tracks.append(enemy.track)
                # создаем новую дорогу для кошки
                enemy.track = choice(tracks)
                tracks.remove(enemy.track)
                # меняем положение
                enemy.x = 30+120*enemy.track
                enemy.top = 400

# ---- Столкновения ----
        if hero.colliderect(cheese):
            game_state = "win"
            #enemy.speed = 0
            if music_on:
                sounds.win.play()
        if hero.collidelist(enemies) != -1:
            game_state = "gameover"
            #enemy.speed = 0
            if music_on:
                sounds.lose.play()


# ---- Запуск музыки ----
def init_sounds():
    sounds.win.set_volume(0.6) # громкость (0.0–1.0)
    sounds.lose.set_volume(0.6)

    if music_on:
        try:
            music.play("music")
            music.set_volume(0.3)
        except:
            print("Нет файла с музыкой")


pgzrun.go()


