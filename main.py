import pgzrun
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
    ("выход", Rect((WIDTH/2-90, 230), (180, 50)), "exit"),
]

# ---- Классы ----
class Hero(Actor):
    def __init__(self, image, pos, speed):
        super().__init__(image, pos)
        self.speed = speed
        self.time = 0

    def update(self, dt):
        # анимация
        self.time += dt
        if self.time > 0.1:
            self.time = 0
            number = int(self.image.split('/')[-1])
            self.image = f'mouse/{(number + 1) % 4}'

        # управление
        if keyboard.UP:
            self.y -= self.speed
        elif keyboard.DOWN:
            self.y += self.speed
        if keyboard.LEFT and self.x > 50:
            self.x -= self.speed
        if keyboard.RIGHT and self.x < WIDTH - 50:
            self.x += self.speed


class Enemy(Actor):
    def __init__(self, image, pos, track, speed):
        super().__init__(image, pos)
        self.track = track
        self.speed = speed
        self.time = 0

    def update(self, dt):
        # анимация
        self.time += dt
        if self.time > 0.1:
            self.time = 0
            number = int(self.image.split('/')[-1])
            self.image = f'cat/{(number + 1) % 9}'

        # движение
        self.y -= self.speed
        if self.bottom < 0:
            # возвращаемся вниз на новую "дорогу"
            tracks.append(self.track)
            self.track = choice(tracks)
            tracks.remove(self.track)
            self.x = 30 + 120 * self.track
            self.top = 400


# ---- Создание объектов ----
tracks = [1, 2, 3]
enemies = []
for i in range(3):
    track = choice(tracks)
    tracks.remove(track)
    e = Enemy("cat/0", (30 + 120 * track, randint(100, 400)), track, randint(3, 6))
    enemies.append(e)

cheese = Actor("cheese_half")
cheese.pos = (WIDTH-30, HEIGHT/2)

hero = Hero("mouse/0", (30, HEIGHT/2), 5)


# ---- Функции ----
def draw():
    if game_state == "menu":
        screen.blit("background", (0, 0))
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

    if game_state == "gameover":
        screen.draw.text("GAME OVER\nТы накормил кошку :)",
                         fontsize=40,
                         center=(WIDTH//2, HEIGHT//2),
                         color="darkred")

    if game_state == "win":
        cheese.draw()
        screen.draw.text("YOU WIN\nТы накормил мышку :)",
                         fontsize=40,
                         center=(WIDTH//2, HEIGHT//2),
                         color="seagreen")


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


def update(dt):
    global game_state
    if game_state == "game":
        hero.update(dt)
        for enemy in enemies:
            enemy.update(dt)

        # столкновения
        if hero.colliderect(cheese):
            game_state = "win"
            if music_on:
                sounds.win.play()
        if hero.collidelist(enemies) != -1:
            game_state = "gameover"
            if music_on:
                sounds.lose.play()


# ---- Звук ----
def init_sounds():
    sounds.win.set_volume(0.6)
    sounds.lose.set_volume(0.6)
    if music_on:
        try:
            music.play("music")
            music.set_volume(0.3)
        except:
            print("Нет файла с музыкой")


pgzrun.go()
