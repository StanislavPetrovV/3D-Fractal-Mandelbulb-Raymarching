from shading import *
from sdf import *
from numba import njit
import cProfile

v_matrix = view_matrix()

@njit(fastmath=True)
def ray_marching(key):
    res = []
    SCALE = key[5]
    REAL_WIDTH = WIDTH / SCALE
    REAL_HEIGHT = HEIGHT / SCALE
    HALF_REAL_WIDTH = REAL_WIDTH // 2
    HALF_REAL_HEIGHT = REAL_HEIGHT // 2
    FOV = math.pi / 4
    Z_DIST = REAL_HEIGHT / math.tan(FOV / 2)
    plane_vec = (HALF_REAL_WIDTH, -HALF_REAL_HEIGHT, -Z_DIST)

    for x in range(int(REAL_WIDTH)):
        for y in range(int(REAL_HEIGHT)):
            ray_dir = normalize_vec3(sub_vecs3((x, -y, 0), plane_vec))
            ray_dir = mul_matrix_vec3(v_matrix, ray_dir)
            depth = 0
            for i in range(MAX_STEPS):
                p = sum_vecs3(cam_pos, mul_vec3_n(ray_dir, depth))
                p = rotate_y_matrix(p, key[3])
                # p = rotate_x_matrix(p, key[4])
                # p = rotate_z_matrix(p, key[5])
                dist, color_num = sdf_scene(p, key)

                if dist < key[1]:
                    color = shading_blinn(p, key, color_num)
                    res.append((color, x * SCALE, y * SCALE))
                    break
                depth += dist
                if depth > MAX_DEPTH:
                    break
    return res
