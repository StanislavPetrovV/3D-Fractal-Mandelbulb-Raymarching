from functions import *
import numpy as np
import math


# @njit(fastmath=True)
# def sdf_scene(p, key):
#     # Return format: tuple(dist, color_number)
#     p = sub_vec3_n(mod_vec3_n(p, 2), 0.5 * 2)
#     return sdf_sphere(p, 0.3, (0.0, 0.0, 0.0, 0.0)), 0


@njit(fastmath=True)
def sdf_scene(p, key):
    # Return format: tuple(dist, color_number)
    obj0 = (scaling_sdf(sdf_mandelbrot, p, key[0]), 0)
    return obj0


@njit(fastmath=True)
def mapping_sdf(p, key):
    displacement = math.sin(key[3] * p[0]) * math.sin(key[3] * p[1]) * math.sin(key[3] * p[2]) * 0.25
    return displacement


@njit(fastmath=True)
def scaling_sdf(sdf, p, scale):
    p = div_vec3_n(p, scale)
    d = sdf(p)
    return d * scale


@njit(fastmath=True)
def soft_min(a, b):
    k = 0.8
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h ** 3 * k * (1.0 / 6.0)


@njit(fastmath=True)
def sdf_mandelbrot(p):
    zn = p
    hit = 0.0
    r = 8.0
    d = 2.0
    for i in range(8):
        rad = length_vec3(zn)
        if rad > 2.0:
            hit = 0.5 * math.log(rad) * rad / d
        else:
            th = math.atan(length_vec2((zn[0], zn[1])) / zn[2])
            phi = math.atan2(zn[1], zn[0])
            rado = pow(rad, 8.0)
            d = pow(rad, 7.0) * 7.0 * d + 1.0
            sint = math.sin(th * r)
            zn0 = rado * sint * math.cos(phi * r)
            zn1 = rado * sint * math.sin(phi * r)
            zn2 = rado * math.cos(th * r)
            zn = (zn0, zn1, zn2)
            zn = sum_vecs3(zn, p)
    return hit


@njit(fastmath=True)
def sdf_plane(p):
    return p[1] + 3.7



@njit(fastmath=True)
def sdf_sphere(p, radius=0.3, delta=(0.0, 0.0, 0.0)):
    return math.sqrt((p[0] + delta[0]) ** 2 + (p[1] + delta[1]) ** 2 + (p[2] + delta[2]) ** 2) - radius


@njit(fastmath=True)
def sdf_octahedron(p):
    p = (abs(p[0]), abs(p[1]), abs(p[2]))
    return (p[0] + p[1] + p[2] - 0.1) * 0.57735027


@njit(fastmath=True, cache=True)
def sdf_torus(p): #, time):
    # p = sum_vecs3(p, (0., -time * 2., -time))
    # p = sub_vec3_n(mod_vec3_n(p, 8), 0.5 * 8)
    tmp1 = length_vec2((p[0], p[1]))
    return length_vec2((tmp1 - 0.6, p[2])) - 0.2


@njit(fastmath=True)
def sdf_cube(p, d=(0,0,0)):
    b, r = (0.4, 0.4, 0.4), 0.4
    q = (abs(p[0] + d[0]) - b[0], abs(p[1] + d[1]) - b[1], abs(p[2] + d[2]) - b[2])
    return max((q[0], q[1], q[2], 0)) + min(max(q[0], max(q[1], q[2])), 0)