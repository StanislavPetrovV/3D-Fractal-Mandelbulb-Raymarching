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

    with Pool(processes=4) as pool:
        start = time()
        game = True
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = False
            control.pressed_keys()
            sc.fill(DARKGRAY)

            res_0 = pool.apply_async(ray_marching, (control.key, 0))
            res_1 = pool.apply_async(ray_marching, (control.key, 1))
            res_2 = pool.apply_async(ray_marching, (control.key, 2))
            res_3 = pool.apply_async(ray_marching, (control.key, 3))

            result = res_0.get() + res_1.get() + res_2.get() + res_3.get()

            side = control.key[5] * 2
            for color, x, y in result:
                pygame.draw.rect(sc, color, (x, y, control.key[5], side))

            pygame.display.flip()
            clock.tick()
    print(time() - start)
    pygame.quit()
    sys.exit()
