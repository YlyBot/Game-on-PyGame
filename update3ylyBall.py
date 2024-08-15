import pygame as pg
import sys
import math
import random

pg.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Game')

speed = 0.03
radius = 140
angle = 0

center_x, center_y = width // 2, height // 2

obj_radius = 12
obj_surface = pg.Surface((obj_radius * 2, obj_radius * 2), pg.SRCALPHA)
pg.draw.circle(obj_surface, (255, 255, 255), (obj_radius, obj_radius), obj_radius)
obj_rect = obj_surface.get_rect(center=(center_x, center_y))

class RectObject:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.x = random.randint(120, width - 180)
        self.y = -self.height
        self.speed = random.randint(3, 6)

    def move(self):
        self.y += self.speed

    def paint(self, screen):
        pg.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def offsite(self):
        return self.y > height

    def caught(self, player_rect):
        return player_rect.colliderect(pg.Rect(self.x, self.y, self.width, self.height))

class BallObject:
    def __init__(self):
        self.radius = 10
        self.x = random.randint(120, width - 180)
        self.y = -self.radius
        self.speed = random.randint(3, 6)

    def move(self):
        self.y += self.speed


    def draw(self, screen):
        pg.draw.circle(screen, (0, 180, 0), (self.x, self.y), self.radius)

    def offsite(self):
        return self.y > height

    def caught(self, player_rect):
        circle_center = (self.x, self.y)
        closest_x = max(player_rect.left, min(circle_center[0], player_rect.right))
        closest_y = max(player_rect.top, min(circle_center[1], player_rect.bottom))
        distance_x = circle_center[0] - closest_x
        distance_y = circle_center[1] - closest_y
        return (distance_x ** 2 + distance_y ** 2) <= self.radius ** 2

def reset_game():
    global rect_objects, ball_objects, score, game_over, angle, move_right, move_left, chanceBall, chanceRect, max_score
    rect_objects = []
    ball_objects = []
    max_score = [0]
    score = 0
    game_over = False
    angle = 0
    move_right = False
    move_left = False
    chanceBall = 0.01
    chanceRect = 0.04

def chances(score):
    global chanceBall, chanceRect
    if score >= 16:
        chanceBall = 0.09
    elif score >= 11:
        chanceBall = 0.06
        chanceRect = 0.015
    elif score >= 6:
        chanceBall = 0.05
        chanceRect = 0.02



rect_objects = []
ball_objects = []

clock = pg.time.Clock()

score = 0
max_score = [0]

font = pg.font.SysFont("bahnschrift", 36)
fontLose = pg.font.SysFont("bahnschrift", 60)
fontMaxScore = pg.font.SysFont('bahnschrift', 40)
restartFont = pg.font.SysFont('bahnschrift', 30)

chanceBall = 0.01
chanceRect = 0.04

move_right = False
move_left = False

game_over = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                move_right = True
                move_left = False
            elif event.key == pg.K_a:
                move_left = True
                move_right = False
        elif event.type == pg.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if restart_button_rect.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        if move_right:
            angle += speed
            if angle >= math.pi * 2:
                angle -= math.pi * 2
        if move_left:
            angle -= speed
            if angle < 0:
                angle += 2 * math.pi

        x = center_x + radius * math.cos(angle) - obj_rect.width / 2
        y = center_y + radius * math.sin(angle) - obj_rect.height / 2

        obj_rect.topleft = (x, y)

        screen.fill((255, 255, 255))
        pg.draw.circle(screen, (24, 229, 244), (center_x, center_y), 160, 40)
        screen.blit(obj_surface, obj_rect)

        if random.random() < chanceRect:
            rect_objects.append(RectObject())

        if random.random() < chanceBall:
            ball_objects.append(BallObject())

        for rect_obj in rect_objects[:]:
            rect_obj.move()
            rect_obj.paint(screen)
            if rect_obj.offsite():
                rect_objects.remove(rect_obj)
            elif rect_obj.caught(obj_rect):
                score += 1
                max_score.append(score)
                rect_objects.remove(rect_obj)

        for ball_obj in ball_objects[:]:
            ball_obj.move()
            ball_obj.draw(screen)
            if ball_obj.offsite():
                ball_objects.remove(ball_obj)
            elif ball_obj.caught(obj_rect):
                score -= 5
                max_score.append(score)
                ball_objects.remove(ball_obj)

        chances(score)

        if score < 0:
            game_over = True

        if score > 26:
            best = pg.font.SysFont('bahnschrift', 30)
            bester = best.render('Вы побили рекорд Создателя!', True, 'black')
            screen.blit(bester,(width // 4,height // 1.2))

        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    else:
        screen.fill((0, 0, 0))
        score_lose = fontLose.render("ВЫ ПРОИГРАЛИ", True, (255, 0, 0))
        score_maxi = fontMaxScore.render(f'Ваш максимальный счет - {max(max_score)}', True, (255, 0, 0))
        restart_button = restartFont.render('Рестарт', True, (255, 255, 255))
        restart_button_rect = restart_button.get_rect(center=(width // 2, height // 1.5))
        screen.blit(score_maxi, (width // 4.2, height // 2))
        screen.blit(score_lose, (width // 4, height // 4))
        screen.blit(restart_button, restart_button_rect.topleft)

    pg.display.flip()
    clock.tick(60)
