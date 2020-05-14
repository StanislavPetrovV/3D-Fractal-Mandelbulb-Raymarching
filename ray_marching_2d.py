import pygame
import os
import sys
from math import sin, cos, sqrt, pi, atan2
from pygame import Vector2
import tkinter as tk
import numpy as np

WIDTH = 1600
HEIGHT = 900
DARKGRAY = (15, 15, 15)
DARKGREEN = (6, 91, 9)
BLUE = (0, 0, 255)
GRAY = (90, 90, 90)
RED = (255, 0, 0)
YELLOW = (200, 200, 0)

MAX_STEPS = 0
EPSILON = 0.001
MAX_DEPTH = WIDTH

p = Vector2(WIDTH // 2, HEIGHT - 50)
angle = -pi / 2
cx1, cy1, cr1 = WIDTH // 2, HEIGHT // 2, 100
cx2, cy2, cr2 = 0, 0, 500
length = 0
depth = 0

os.environ['SDL_VIDEO_WINDOW_POS'] = f'{(tk.Tk().winfo_screenwidth() - WIDTH) // 2},' \
                                     f'{(tk.Tk().winfo_screenheight() - HEIGHT) // 4}'
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


def sdf_scene(vec):
    obj1 = (sqrt((vec.x - cx1) ** 2 + (vec.y - cy1) ** 2) - cr1, 1)
    obj2 = (sqrt((vec.x - cx2) ** 2 + (vec.y - cy2) ** 2) - cr2, 2)
    return min(obj1, obj2)
    # return obj1

def sphere_intercest_1(x, y):
    angle = atan2((cy1 - y), (cx1 - x))
    return cx1 - cr1 * cos(angle), cy1 - cr1 * sin(angle)


def sphere_intercest_2(x, y):
    angle = atan2((cy2 - y), (cx2 - x))
    return cx2 - cr2 * cos(angle), cy2 - cr2 * sin(angle)

sphere_intercest = {1: sphere_intercest_1, 2: sphere_intercest_2}


game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p.y -= 3
    if keys[pygame.K_s]:
        p.y += 3
    if keys[pygame.K_a]:
        p.x -= 3
    if keys[pygame.K_d]:
        p.x += 3
    if keys[pygame.K_LEFT]:
        angle -= 0.01
    if keys[pygame.K_RIGHT]:
        angle += 0.01
    if keys[pygame.K_UP]:
        MAX_STEPS += 0.03
    if keys[pygame.K_DOWN]:
        MAX_STEPS -= 0.03
    sc.fill(DARKGRAY)

    c = cos(angle)
    s = sin(angle)
    pygame.draw.line(sc, DARKGREEN, (p.x, p.y), (int(p.x + depth * c), int(p.y + depth * s)), 2)
    pygame.draw.circle(sc, GRAY, (cx1, cy1), cr1)

    pygame.draw.circle(sc, GRAY, (cx2, cy2), cr2)

    ray = Vector2(c, s)
    depth = 0
    for i in range(int(MAX_STEPS)):
        pos = Vector2(p.xy + depth * ray)
        dist, sphere_num = sdf_scene(pos)
        depth += dist
        if dist < EPSILON or depth > MAX_DEPTH:
            break
        pygame.draw.circle(sc, GRAY, (int(pos.x), int(pos.y)), max(int(dist), 1), 1)
        pygame.draw.circle(sc, BLUE, (int(pos.x), int(pos.y)), 3)
        pygame.draw.line(sc, RED, (int(pos.x), int(pos.y)), sphere_intercest[sphere_num](pos.x, pos.y), 2)



    pygame.draw.circle(sc, YELLOW, (int(p.x + depth * c), int(p.y + depth * s)), 5)
    pygame.draw.circle(sc, BLUE, (int(p.x), int(p.y)), 10)

    pygame.display.flip()
    clock.tick(60)
