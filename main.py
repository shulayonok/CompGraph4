import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter


def round(num):
    if num > 0:
        num = int(num + 0.5)
    else:
        num = int(num - 0.5)
    return num


def drawing(p0, p1, p2, t):
    x = p0[0] * (1 - t) ** 2 + 2 * p1[0] * (1 - t) * t + p2[0] * t ** 2
    y = p0[1] * (1 - t) ** 2 + 2 * p1[1] * (1 - t) * t + p2[1] * t ** 2
    return [x, y]


# Кадры, изображения и размер
N = 512
num_frames = 500
frames = []
fig = plt.figure()
img = np.zeros((N, N, 3), dtype=np.uint8)

# Цвет
background_color = np.zeros((N, N, 3), dtype=np.uint8)
background_color[:, :, :3] = 255
lines_color = [153, 0, 51]
img[0:N, 0:N] = background_color

# Радиус
R = 100

rad = R
dr, x_prev, y_prev = 0, 0, 0
not_static = True
static = True
for p in range(num_frames):
    control_points = []
    if dr == 99 and p <= 100:
        not_static = False
    if dr == -99 and p >= 250:
        not_static = True
    img[0:N, 0:N] = background_color
    # Угол
    alpha = 0
    for j in range(0, 360):
        # Координаты
        x = N / 2 + (rad + dr) * np.cos(alpha)
        y = N / 2 + (rad + dr) * np.sin(alpha)
        if j % 5 == 0:
            if static:
                x = N / 2 + R * np.cos(alpha)
                y = N / 2 + R * np.sin(alpha)
                control_points.append([x, y, 1])
                static = False
            else:
                dr *= -1
                control_points.append([x, y, 0])
                static = True
        alpha += np.pi / 180
    i = 0
    amount = len(control_points)
    while True:
        if i == 0:
            control_points[i][0] = 0.5 * (control_points[amount - 1][0] + control_points[1][0])
            control_points[i][1] = 0.5 * (control_points[amount - 1][1] + control_points[1][1])
        if i == amount - 1:
            break
        if control_points[i][2] == 1:
            control_points[i][0] = 0.5 * (control_points[i - 1][0] + control_points[i + 1][0])
            control_points[i][1] = 0.5 * (control_points[i - 1][1] + control_points[i + 1][1])
        i += 1
    # Отображаем то, что получилось
    for k in range(0, amount - 1, 2):
        T = 0.0
        while T <= 1.0:
            point = drawing(control_points[k], control_points[k + 1], control_points[(k + 2) % amount], T)
            img[round(point[0]), round(point[1])] = lines_color
            T += 0.01
    if not_static:
        dr += 1
    else:
        dr -= 1
    static = True
    im = plt.imshow(img)
    frames.append([im])

print('Frames creation finished.')

# gif animation creation
ani = animation.ArtistAnimation(fig, frames, interval=40, blit=True, repeat_delay=0)
writer = PillowWriter(fps=30)
ani.save("Bezier.gif", writer=writer)

plt.show()
