from settings import *
from sdf import *
from functions import *


@njit(fastmath=True)
def normal(p, key):
    d, _ = sdf_scene(p, key)
    d0, _ = sdf_scene((p[0] - EPSILON, p[1], p[2]), key)
    d1, _ = sdf_scene((p[0], p[1] - EPSILON, p[2]), key)
    d2, _ = sdf_scene((p[0], p[1], p[2] - EPSILON), key)
    vec3 = ((d - d0 + 0.00001), (d - d1), (d - d2))
    return normalize_vec3(vec3)


# diff_color = (1.0, 0.55, 0.04) # orange
# diff_color = (0.18, 0.35, 1.0) # blue
# diff_color = (1.0, 0.42, 0.89) # rose
# diff_color = (0.0, 0.42, 0.1) # green
# diff_color = (0.65, 0.17, 0.17)  # metallic red
# diff_color = (0.86, 0.85, 0.8) # milk
# diff_color = (0.83, 0.68, 0.21) # gold


@njit(fastmath=True)
def shading_blinn(p, key, color_num):
    power = 10
    diff_color = (1.0, 0.55, 0.04)
    light_pos = (4.0, 30.0, 20.0)

    spec_color = (0.7, 0.7, 0.7)

    N = normal(p, key)
    # N = normal_0(p)  # , angle)

    light = rotate_y(light_pos, -key[3])
    light = rotate_x(light, -key[4])
    # light = light_pos

    vec = sub_vecs3(light, N)
    L = normalize_vec3(vec)
    vec = sub_vecs3(cam_pos, p)
    V = normalize_vec3(vec)
    vec = sum_vecs3(L, V)
    H = normalize_vec3(vec)

    dot_NL = max(dot_vecs3(N, L), 0)
    dot_NH = max(dot_vecs3(N, H), 0)

    pow_NH = pow(dot_NH, power)

    diff = mul_vec3_n(diff_color, dot_NL)
    spec = mul_vec3_n(spec_color, pow_NH)

    color = (min(diff[0] + spec[0], 1), min(diff[1] + spec[1], 1), min(diff[2] + spec[2], 1))
    return mul_vec3_n(color, 255)


@njit(fastmath=True)
def shading_minnaert(p, key, color_num):
    k = 0.99
    if color_num == 0:
        diff_color = (0.18, 0.35, 1.0)
        light_pos = (0.0, 0.0, 20.0)
    else:
        diff_color = (0.6, 0.6, 0.6)
        light_pos = (20.0, 0.0, 0.0)

    N = normal(p, key)

    light = rotate_y(light_pos, -key[3])
    light = rotate_y(light, -key[4])
    # light = light_pos
    vec = sub_vecs3(light, N)
    L = normalize_vec3(vec)
    vec = sub_vecs3(cam_pos, p)
    V = normalize_vec3(vec)

    dot_NL = max(dot_vecs3(N, L), 0)
    dot_NV = max(dot_vecs3(N, V), 0)
    d1 = pow(dot_NL, 1.0 + k)
    d2 = pow(1.0 - dot_NV, 1.0 - k)

    color = mul_vec3_n(mul_vec3_n(diff_color, d1), d2)
    return mul_vec3_n(color, 255)


@njit(fastmath=True)
def shading_wrap(p, key, color_num):
    if color_num == 0:
        diff_color = (0.86, 0.85, 0.88)
        light_pos = rotate_y_matrix((0.0, 0.0, 20.0), key[3])
    elif color_num == 1:
        diff_color = (0.5, 0.5, 0.5)
        light_pos = (20.0, 0.0, 0.0)
    elif color_num == 2:
        diff_color = (0.93, 0.79, 0.54)
        light_pos = (-20.0, 0.0, 0.0)
    elif color_num == 3:
        diff_color = (0.42, 0.57, 0.84)
        light_pos = (0.0, 0.0, 20.0)
    else:
        diff_color = (0.65, 0.17, 0.17)
        light_pos = (0.0, 0.0, -20.0)
    factor = 0.5
    N = normal(p, key)

    # light = rotate_y(light_pos, key[3])

    light = light_pos
    vec = sub_vecs3(light, N)
    L = normalize_vec3(vec)

    dot_NL = dot_vecs3(N, L)
    diff = mul_vec3_n(diff_color, max(dot_NL + factor, 0) / (1.0 + factor))
    return mul_vec3_n(diff, 255)
