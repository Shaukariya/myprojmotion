import numpy as np
import pygame as pg
import sys


# Initialize pygame
pg.init()
pg.font.init()
clock = pg.time.Clock()

# Define functions for angles in degrees
def sin(x):
    return np.sin(x * (np.pi / 180))
def cos(x):
    return np.cos(x * (np.pi / 180))


# Define gravity
g = 9.81
# Define default velocity
v = 18

# Create text input boxes
input_box1 = pg.Rect(100, 10, 140, 32)
active1 = False
text1 = ''
done1 = False

input_box2 = pg.Rect(100, 50, 140, 32)
active2 = False
text2 = '9.81'
done2 = False

input_box3 = pg.Rect(100, 90, 140, 64)
active3 = False
text3 = '18'
done3 = False

# Screen dimensions
screen_width = 1200
screen_height = 675

# Initial angle (the angle of the given cannon image was approximately 23.5190522325 degrees, so to get the exact angle, we would need subtract this angle from the input)
theta = -23.5190522325

# Other variables
fired = False
t = 0  # Time elapsed since firing

# Calculate the theoretical maximum range
max_range = v**2 / g

# Scaling factor for velocity based on the screen width
scale_x = screen_width / max_range
scale_y = screen_height / (max_range * 0.5)

# Set up display
screen = pg.display.set_mode((screen_width, screen_height))
my_font = pg.font.SysFont('Comic Sans MS', 30)

# Load images
bg = pg.image.load("g2.jpg")
mario = pg.transform.scale(bg, (1200, 675))
cannonball = pg.image.load("cannonball.gif")
cannon = pg.image.load("cannon.png")
cannon = pg.transform.scale(cannon, (int(screen_width * 0.2), int(screen_height * 0.2)))
cannonball = pg.transform.scale(cannonball, (int(screen_width * 0.05), int(screen_height * 0.1)))
mario = pg.image.load("Sprite.png")
mario = pg.transform.scale(mario, (80, 150))

# Rotate image
def rotate_image(image, angle):
    return pg.transform.rotate(image, angle)

# Initial target position
a, b = np.random.randint(100, screen_width-100), np.random.randint(150, screen_height-100)
hit = False
lives = 3
shots = 5

# Running loop
running = True
while running:
    screen.blit(bg, (0, 0))  # Draw background first
    screen.blit(mario, (a, b))

    # Render text
    txtsrf3 = my_font.render('θ = ' + text1, True, (255, 255, 255))
    txtsrf4 = my_font.render('g = ' + text2, True, (255, 255, 255))
    txtsrf5 = my_font.render('v = ' + text3 + ' m/s', True, (255, 255, 255))
    txtsrf6 = my_font.render('time: ' + str(round(t, 2)) + ' s', True, (255, 255, 255))
    txtsrf8 = my_font.render('lives: ' + str(lives), True, (255, 255, 255))
    txtsrf9 = my_font.render('shots:  ' + str(shots), True, (255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos):
                active1 = not active1
            else:
                active1 = False

            if input_box2.collidepoint(event.pos):
                active2 = not active2
                if active2:
                    text2 = ''
            else:
                active2 = False
                if text2 == '':
                    text2 = '9.81'

            if input_box3.collidepoint(event.pos):
                active3 = not active3
                if active3:
                    text3 = ''
            else:
                active3 = False
                if text3 == '':
                    text3 = '18'

        elif event.type == pg.KEYDOWN:
            if active1:
                if event.key == pg.K_RETURN:
                    if text1 == '':
                        theta = -23.5190522325
                    else:
                        try:
                            theta = float(text1) - 23.5190522325
                        except ValueError:
                            text1 = ''
                elif event.key == pg.K_BACKSPACE:
                    text1 = text1[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode == '.':
                        text1 += event.unicode

            if active2:
                if event.key == pg.K_RETURN:
                    try:
                        g = float(text2)
                    except ValueError:
                        text2 = '9.81'
                elif event.key == pg.K_BACKSPACE:
                    text2 = text2[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode == '.':
                        text2 += event.unicode

            if active3:
                if event.key == pg.K_RETURN:
                    try:
                        v = float(text3)
                    except ValueError:
                        text3 = '18'
                elif event.key == pg.K_BACKSPACE:
                    text3 = text3[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode == '.':
                        text3 += event.unicode

            if event.key == pg.K_SPACE:
                fired = True
                t = 0  # Reset time when firing

            elif event.key == pg.K_RIGHT and not fired:
                text1 = ''
                theta += 1
            elif event.key == pg.K_LEFT and not fired:
                text1 = ''
                if theta > -23.5190522325:
                    theta -= 1
                else:
                    txtsrf1 = my_font.render('Angle can\'t be further decreased', False, (255, 255, 255))

    if fired:
        
        t += clock.get_time() / 1000  # Convert milliseconds to seconds
        vx = v * cos(theta + 23.5190522325)
        vy = -v * sin(theta + 23.5190522325)  # vy is negative because y increases downward in pygame
        x = 100 + (vx * t * scale_x)
        y = screen_height - 140 + (vy * t + 0.5 * g * t**2) * scale_y
        if a-40 <= x <= a+40 and b-80 <= y <= b+80:
            hit = True 
        if y >= screen_height:  # Check if cannonball hits the ground
            fired = False
            shots -= 1
            if hit:
                lives-=1
            x = 100 + 70 * cos(theta + 23.5190522325)
            y = screen_height - 140 - 40 * sin(theta + 23.5190522325)
            a, b = np.random.randint(100, screen_width-100), np.random.randint(150, screen_height-150)
    else:
        x = 100 + 70 * cos(theta + 23.5190522325)
        y = screen_height - 140 - 40 * sin(theta + 23.5190522325)
        vx = 0
        vy = 0
        hit = False

    if hit:
        
        txtsrf7 = my_font.render('Hit!', False, (255, 255, 255))
    else:
        txtsrf7 = my_font.render('', False, (255, 255, 255))
    if lives == 0:
        txtsrf10 = my_font.render('You Win!', False, (255, 255, 255))
        txtsrf11 = my_font.render('Game Over!', False, (255, 255, 255))
        screen.blit(txtsrf10, (400, 300))
        screen.blit(txtsrf11, (400, 350))
        pg.display.flip()
        pg.time.wait(500)
        running = False
        
    elif shots == 0 and lives !=0:
        txtsrf10 = my_font.render('You Lose!', False, (255, 255, 255))
        txtsrf11 = my_font.render('Game Over!', False, (255, 255, 255))
        screen.blit(txtsrf10, (400, 300))
        screen.blit(txtsrf11, (400, 350))
        pg.display.flip()
        pg.time.wait(500)
        running = False
    else:
        txtsrf10 = my_font.render('', False, (255, 255, 255))
        txtsrf11 = my_font.render('', False, (255, 255, 255))
        
        

    # Blit the text
    screen.blit(txtsrf3, (100, 0))
    screen.blit(txtsrf4, (100, 40))
    screen.blit(txtsrf5, (100, 80))
    screen.blit(txtsrf6, (700, 40))
    screen.blit(txtsrf7, (50, 500))
    screen.blit(txtsrf8, (700, 80))
    screen.blit(txtsrf9, (700, 120))
    screen.blit(txtsrf10, (400, 300))
    screen.blit(txtsrf11, (400, 350))

    # Blit the input boxes
    pg.draw.rect(screen, 'black', input_box1, -1)
    pg.draw.rect(screen, 'black', input_box2, -1)
    pg.draw.rect(screen, 'black', input_box3, -1)

    rotated_image = rotate_image(cannon, theta)
    rect = rotated_image.get_rect(center=(-32, screen_height - 170))
    screen.blit(rotated_image, rect.center)
    screen.blit(cannonball, (x, y))

    if not active1:
        txtsrf2 = my_font.render('θ = ' + str(theta + 23.5190522325), False, (255, 255, 255))
    else:
        txtsrf2 = my_font.render('', False, (255, 255, 255))
    screen.blit(txtsrf2, (100, 0))
    if lives !=0 or (shots!=0 and lives==0):
        pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()
