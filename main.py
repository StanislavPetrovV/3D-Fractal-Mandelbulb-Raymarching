import pygame
import os
import sys
import tkinter as tk
from ray_marching import *
from time import time
from settings import *
import control
from multiprocessing import Pool


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{(tk.Tk().winfo_screenwidth() - WIDTH) // 2},' \
                                         f'{(tk.Tk().winfo_screenheight() - HEIGHT) // 4}'
    pygame.init()
    pygame.display.set_caption('Ray marching')
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    control = control.Control()

    # fps = []
    start = time()
    game = True
    for i in range(10):
    # while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print(sum(fps) / len(fps))
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
        control.pressed_keys()
        sc.fill(DARKGRAY)

        # t = time() * 0.25
        for color,x,y in ray_marching(control.key):
            pygame.draw.rect(sc, color, (x, y, control.key[5], control.key[5]))

        pygame.display.flip()
        clock.tick()
        # fps.append(int(clock.get_fps()))
    # print(sum(fps) / len(fps))
    print(time() - start)
    pygame.quit()
    sys.exit()
