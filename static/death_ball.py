from vpython import *
import random
import time

# Simulasi VPython
scene = canvas(title='Tugas Lima Bola Memantul Menggunakan Keyboard dan Kursor', width=800, height=600, center=vector(0,0,0))

# Warna-warna yang telah ditentukan
colors = [vector(1, 0, 0),  # Merah
          vector(0, 0, 1),  # Biru
          vector(0, 1, 0),  # Hijau
          vector(0.5, 0.5, 0.5),  # Abu-abu
          vector(1, 0.5, 0),  # Oranye
          vector(1, 0, 1)]  # Ungu (digerakkan oleh keyboard)

def random_velocity():
    return vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)

# Buat bola-bola
balls = []
for i in range(6):
    ball = sphere(pos=vector(random.uniform(-4.5, 4.5), random.uniform(-4.5, 4.5), 0),
                  radius=0.5,
                  color=colors[i])
    ball.velocity = random_velocity()
    balls.append(ball)

# Menandai bola ungu yang digerakkan oleh keyboard
purple_ball = balls[5]

# Buat kotak frame
frame_size = 5
box_bottom = box(pos=vector(0, -frame_size, 0), size=vector(10, 0.1, 10), color=color.white)
box_top = box(pos=vector(0, frame_size, 0), size=vector(10, 0.1, 10), color=color.white)
box_left = box(pos=vector(-frame_size, 0, 0), size=vector(0.1, 10, 10), color=color.white)
box_right = box(pos=vector(frame_size, 0, 0), size=vector(0.1, 10, 10), color=color.white)

collision_text = label(pos=vector(0, frame_size + 1, 0), text='Collisions: 0', height=20, color=color.white, box=False)

collision_count = 0

dt = 0.01
kecepatan = 0.1

achievement_status = ""

# Pilihan untuk bola-bola berhenti atau memantul
stop_on_collision = False

def move_purple_ball(evt):
    global collision_count, achievement_status, stop_on_collision
    
    if evt.key == 'up' and purple_ball.pos.y + purple_ball.radius + kecepatan <= frame_size:
        purple_ball.pos.y += kecepatan
    elif evt.key == 'down' and purple_ball.pos.y - purple_ball.radius - kecepatan >= -frame_size:
        purple_ball.pos.y -= kecepatan
    elif evt.key == 'left' and purple_ball.pos.x - purple_ball.radius - kecepatan >= -frame_size:
        purple_ball.pos.x -= kecepatan
    elif evt.key == 'right' and purple_ball.pos.x + purple_ball.radius + kecepatan <= frame_size:
        purple_ball.pos.x += kecepatan

    for ball in balls:
        if ball != purple_ball:
            distance = mag(purple_ball.pos - ball.pos)
            if distance <= purple_ball.radius + ball.radius:
                collision_count += 1
                collision_text.text = f'Collisions: {collision_count}'

                v1 = purple_ball.velocity
                v2 = ball.velocity
                m1 = m2 = 1

                direction = norm(purple_ball.pos - ball.pos)

                v1_parallel = dot(v1, direction) * direction
                v1_perpendicular = v1 - v1_parallel

                v2_parallel = dot(v2, direction) * direction
                v2_perpendicular = v2 - v2_parallel

                if stop_on_collision:
                    purple_ball.velocity = vector(0, 0, 0)  # Menghentikan bola ungu setelah bertabrakan
                else:
                    purple_ball.velocity = v2_parallel + v1_perpendicular

                if stop_on_collision:
                    ball.velocity = vector(0, 0, 0)  # Menghentikan bola yang bertabrakan dengan bola ungu
                else:
                    ball.velocity = v1_parallel + v2_perpendicular

                if collision_count == 50:
                    achievement_status = "Warrior!"
                elif collision_count == 100:
                    achievement_status = "Elite!"
                elif collision_count == 150:
                    achievement_status = "Master!"
                elif collision_count == 200:
                    achievement_status = "Grandmaster!"

                return
    collision_text.text = f'Collisions: {collision_count}'

scene.bind('keydown', move_purple_ball)

achievement_text = label(pos=vector(0, frame_size + 2, 0), text='', height=20, color=color.yellow, box=False)
timer_text = label(pos=vector(0, frame_size + 3, 0), text='Time Left: 60s', height=20, color=color.white, box=False)

def vpython_simulation():
    global collision_count, achievement_status, stop_on_collision
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        time_left = 60 - int(elapsed_time)
        
        if time_left <= 0:
            break
        
        timer_text.text = f'Time Left: {time_left}s'
        
        rate(200)
        for ball in balls:
            if ball != purple_ball:
                ball.pos += ball.velocity * dt
            
                if ball.pos.x - ball.radius < -frame_size:
                    ball.pos.x = -frame_size + ball.radius
                    ball.velocity.x *= -1
                elif ball.pos.x + ball.radius > frame_size:
                    ball.pos.x = frame_size - ball.radius
                    ball.velocity.x *= -1
                
                if ball.pos.y - ball.radius < -frame_size:
                    ball.pos.y = -frame_size + ball.radius
                    ball.velocity.y *= -1
                elif ball.pos.y + ball.radius > frame_size:
                    ball.pos.y = frame_size - ball.radius
                    ball.velocity.y *= -1

            if purple_ball.pos.x - purple_ball.radius < -frame_size:
                purple_ball.pos.x = -frame_size + purple_ball.radius
            elif purple_ball.pos.x + purple_ball.radius > frame_size:
                purple_ball.pos.x = frame_size - purple_ball.radius
            
            if purple_ball.pos.y - purple_ball.radius < -frame_size:
                purple_ball.pos.y = -frame_size + purple_ball.radius
            elif purple_ball.pos.y + purple_ball.radius > frame_size:
                purple_ball.pos.y = frame_size - purple_ball.radius
            
            for other_ball in balls:
                if other_ball != ball:
                    distance = mag(ball.pos - other_ball.pos)
                    if distance <= ball.radius + other_ball.radius:
                        overlap = ball.radius + other_ball.radius - distance
                        direction = norm(ball.pos - other_ball.pos)
                        ball.pos += direction * overlap / 2
                        other_ball.pos -= direction * overlap / 2

                        v1 = ball.velocity
                        v2 = other_ball.velocity
                        m1 = m2 = 1

                        if stop_on_collision:
                            ball.velocity = vector(0, 0, 0)  # Menghentikan bola yang bertabrakan
                            other_ball.velocity = vector(0, 0, 0)  # Menghentikan bola yang bertabrakan
                        else:
                            ball.velocity = v1 - 2 * m2 / (m1 + m2) * dot(v1 - v2, ball.pos - other_ball.pos) / mag(ball.pos - other_ball.pos)**2 * (ball.pos - other_ball.pos)
                            other_ball.velocity = v2 - 2 * m1 / (m1 + m2) * dot(v2 - v1, other_ball.pos - ball.pos) / mag(other_ball.pos - ball.pos)**2 * (other_ball.pos - ball.pos)

    # Timer habis, beri apresiasi
    if collision_count >= 200:
        achievement_status = "Grandmaster!"
    elif collision_count >= 150:
        achievement_status = "Master!"
    elif collision_count >= 100:
        achievement_status = "Elite!"
    elif collision_count >= 50:
        achievement_status = "Warrior!"
    else:
        achievement_status = "Beginner"
    
    achievement_text.text = f'Time\'s up! Achievement: {achievement_status}'
    timer_text.text = 'Time Left: 0s'

vpython_simulation()
