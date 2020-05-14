from functions import *
from shading import *
from sdf import *
from numba import njit

# oc = ro - sph.xyz;
# b = dot(oc, rd);
# c = dot(oc, oc) - sph.w * sph.w;
# h = b * b - c;
# if (h < 0.0) return vec2(-1.0);
# h = sqrt(h);
# return -b + vec2(-h, h);

# @njit(fastmath=True)
def is_sphere(sph, ro, rd):
    oc = sub_vecs3(ro, (sph[0], sph[1], sph[2]))
    b = dot_vecs3(oc, rd)
    c = dot_vecs3(oc, oc) - sph[3] ** 2
    h = b ** 2 - c
    if h < 0.0:
        return (-1.0, -1.0)
    h = math.sqrt(h)
    return sum_vec2_n((-h, h), -b)


# map( in vec3 p, out vec4 resColor )
# {
# vec3
# w = p;
# m = dot(w, w);
# trap = vec4(abs(w), m);
# dz = 1.0;
#
# for (int i=0; i < 4; i++)
# {
# m2 = m * m;
# m4 = m2 * m2;
# dz = 8.0 * sqrt(m4 * m2 * m) * dz + 1.0;
#
# x = w.x;
# x2 = x * x;
# x4 = x2 * x2;
# y = w.y;
# y2 = y * y;
# y4 = y2 * y2;
# z = w.z;
# z2 = z * z;
# z4 = z2 * z2;
# k3 = x2 + z2;
# k2 = inversesqrt(k3 * k3 * k3 * k3 * k3 * k3 * k3);
# k1 = x4 + y4 + z4 - 6.0 * y2 * z2 - 6.0 * x2 * y2 + 2.0 * z2 * x2;
# k4 = x2 - y2 + z2;
#
# w.x = p.x + 64.0 * x * y * z * (x2 - z2) * k4 * (x4 - 6.0 * x2 * z2 + z4) * k1 * k2;
# w.y = p.y + -16.0 * y2 * k3 * k4 * k4 + k1 * k1;
# w.z = p.z + -8.0 * y * k4 * (x4 * x4 - 28.0 * x4 * x2 * z2 + 70.0 * x4 * z4 - 28.0 * x2 * z2 * z4 + z4 * z4) * k1 * k2;
#
# dz = 8.0 * pow(sqrt(m), 7.0) * dz + 1.0;
#
# r = length(w);
# b = 8.0 * acos(w.y / r);
# a = 8.0 * atan(w.x, w.z);
# w = p + pow(r, 8.0) * vec3(sin(b) * sin(a), cos(b), sin(b) * cos(a));
#
# trap = min(trap, vec4(abs(w), m));
#
# m = dot(w, w);
# if (m > 256.0)
# break;
#  }
# resColor = vec4(m, trap.yzw);
#
# return 0.25 * log(m) * sqrt(m) / dz;

# @njit(fastmath=True)
def map_(p):
    w = p
    m = dot_vecs3(w, w)
    trap = (*abs_vec3(w), m)
    dz = 1.0

    for i in range(4):
        m2 = m * m
        m4 = m2 * m2
        dz = 8.0 * math.sqrt(m4 * m2 * m) * dz + 1.0

        x = w[0]
        x2 = x * x
        x4 = x2 * x2
        y = w[1]
        y2 = y * y
        y4 = y2 * y2
        z = w[2]
        z2 = z * z
        z4 = z2 * z2

        k3 = x2 + z2
        k2 = 1.0 / math.sqrt(k3 ** 7)
        k1 = x4 + y4 + z4 - 6.0 * y2 * z2 - 6.0 * x2 * y2 + 2.0 * z2 * x2
        k4 = x2 - y2 + z2

        w0 = p[0] + 64.0 * x * y * z * (x2 - z2) * k4 * (x4 - 6.0 * x2 * z2 + z4) * k1 * k2
        w1 = p[1] + -16.0 * y2 * k3 * k4 * k4 + k1 * k1
        w2 = p[2] + -8.0 * y * k4 * (
                x4 * x4 - 28.0 * x4 * x2 * z2 + 70.0 * x4 * z4 - 28.0 * x2 * z2 * z4 + z4 * z4) * k1 * k2
        w = (w0, w1, w2)

        dz = 8.0 * pow(math.sqrt(m), 7.0) * dz + 1.0
        r = length_vec3(w)
        b = 8.0 * math.acos(w[1] / r)
        a = 8.0 * math.atan(w[0] / w[2])
        w = sum_vecs3(p, mul_vec3_n((math.sin(b) * math.sin(a), math.cos(b), math.sin(b) * math.cos(a)), pow(r, 8.0)))

        tmp = (*abs_vec3(w), m)
        trap0 = min(trap[0], tmp[0])
        trap1 = min(trap[1], tmp[1])
        trap2 = min(trap[2], tmp[2])
        trap3 = min(trap[3], tmp[3])
        trap = (trap0, trap1, trap2, trap3)

        m = dot_vecs3(w, w)
        if m > 256.0:
            break

    color = (m, trap[1], trap[2]) #, trap[3])
    print(p, color)
    return (0.25 * math.log(m) * math.sqrt(m) / dz), color


print(map_((10.5, 10.1, 10.6)))


# float intersect( in vec3 ro, in vec3 rd, out vec4 rescol, in float px )
# {
#     float res = -1.0;
# // bounding sphere
# vec2 dis = isphere(vec4(0.0, 0.0, 0.0, 1.25), ro, rd);
# if (dis.y < 0.0)
# return -1.0;
# dis.x = max(dis.x, 0.0);
# dis.y = min(dis.y, 10.0);
#
# // raymarch fractal distance field
# vec4 trap;
# float t = dis.x;
# for (int i=0; i < 128; i++)
#     {
#     vec3 pos = ro + rd * t;
#     float th = 0.25 * px * t;
#     float h = map(pos, trap);
#     if (t > dis.y | | h < th)
#     break;
#     t += h;
#     }
#     if (t < dis.y)
#     {
#     rescol = trap;
#     res = t;
#     }
# return res;

# @njit(fastmath=True)
def intersect(ray_dir, px):
    res = -1.0
    dis = is_sphere((0.0, 0.0, 0.0, 1.25), cam_pos, ray_dir)
    if dis[1] < 0.0:
        return -1.0
    tmp0 = max(dis[0], 0.0)
    tmp1 = min(dis[1], 10.0)
    dis = (tmp0, tmp1)

    depth =dis[0]
    for i in range(MAX_STEPS):
        p = sum_vecs3(cam_pos, mul_vec3_n(ray_dir, depth))
        th = 0.25 * px * depth
        dist, trap = map_(p)
        if depth > dis[1] or dist < th:
            break
        depth += dist
        if depth < dis[1]:
            res = depth
            color = trap
            # return res, color
            return color



v_matrix = view_matrix()

# @njit(fastmath=True)
def ray_marching_fractal(key):
    res = []
    px = 2.0 / (HEIGHT * 1.5)
    plane_vec = (HALF_REAL_WIDTH, -HALF_REAL_HEIGHT, -Z_DIST)
    for x in range(REAL_WIDTH):
        for y in range(REAL_HEIGHT):
            ray_dir = normalize_vec3(sub_vecs3((x, -y, 0), plane_vec))
            ray_dir = mul_matrix_vec3(v_matrix, ray_dir)

            color = intersect(ray_dir, px)
            res.append((color, x * SCALE, y * SCALE))
    return res