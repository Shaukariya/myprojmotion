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
class Player(pg.sprite.Sprite):
    
    def __init__(self, center_pos, image):
        super().__init__() 
        self.image = image
        self.rect = self.image.get_rect(center = center_pos)

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

# Initial angle
theta = -23.5190522325
base_angle = 23.5190522325
prev_theta = theta

# Other variables
fired = False
t = 0  # Time elapsed since firing

# Calculate the theoretical maximum range (is wrong should be theta + 23)
max_range = v**2/ g

# Scaling factor based on the screen width
scale_x = screen_width / max_range
scale_y = screen_height / (max_range * sin(base_angle))

# Set up display
screen = pg.display.set_mode((screen_width, screen_height))
my_font = pg.font.SysFont('Comic Sans MS', 30)

# Load images
bg = pg.image.load("myprojmotion/g.jpg")
cannonball = pg.image.load("myprojmotion/cannonball.gif")
cannon = pg.image.load("myprojmotion/cannon.png")
cannon = pg.transform.scale(cannon, (int(screen_width * 0.2), int(screen_height * 0.2)))
cannonball = pg.transform.scale(cannonball, (int(screen_width * 0.05), int(screen_height * 0.1)))
mario = pg.image.load("myprojmotion/Sprite.png")
mario = pg.transform.scale(mario, (80, 150))


# Rotate image
def rotate_image(image, angle):
    return pg.transform.rotate(image, angle)
a,b = np.random.randint(0, screen_width), np.random.randint(0, screen_height)
# Running loop
running = True
while running:
    screen.blit(bg, (0, 0))  # Draw background first
    sprite = Player((np.random.randint(100, screen_width-150), np.random.randint(100, screen_height-80)), mario)
    screen.blit(mario, (a,b))
    hit = False

    # Render text
    txtsrf3 = my_font.render('θ = ' + text1, True, (0, 0, 0))
    txtsrf4 = my_font.render('g = ' + text2, True, (0, 0, 0))
    txtsrf5 = my_font.render('v = ' + text3 + ' m/s', True, (0, 0, 0))
    txtsrf6 = my_font.render('time: ' + str(round(t, 2)) + ' s', True, (0, 0, 0))
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
                        theta = prev_theta
                    else:
                        try:
                            prev_theta = theta
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

            elif event.key == pg.K_RIGHT:
                text1 = ''
                theta += 1
            elif event.key == pg.K_LEFT:
                text1 = ''
                if theta > -23.5190522325:
                    theta -= 1
                else:
                    txtsrf1 = my_font.render('Angle can\'t be further decreased', False, (0, 0, 0))
            if hit:
                txtsrf7 = my_font.render('Hit!', False, (0, 0, 0))  # Render text for hit

    if fired:
        
        t += clock.get_time() / 1000  # Convert milliseconds to seconds
        vx = v * cos(theta + 23.5190522325)
        vy = -v * sin(theta + 23.5190522325)  # vy is negative because y increases downward in pygame
        x = 100 + (vx * t * scale_x)
        y = screen_height - 140 + (vy * t + 0.5 * g * t**2) * scale_y
        if x in range(a-40, a+40) and y in range(b-75, b+75):
            hit = True 
        if y >= screen_height:  # Check if cannonball hits the ground
            fired = False
            x = 290 + 70 * cos(theta + 23.5190522325)
            y = screen_height - 140 - 40 * sin(theta + 23.5190522325)
            a,b = np.random.randint(0, screen_width), np.random.randint(0, screen_height)
    else:
        x = 100 + 70 * cos(theta + 23.5190522325)
        y = screen_height - 140 - 40 * sin(theta + 23.5190522325)
        vx = 0
        vy = 0
    
        
    # Blit the text
    screen.blit(txtsrf3, (100, 0))
    screen.blit(txtsrf4, (100, 40))
    screen.blit(txtsrf5, (100, 80))
    screen.blit(txtsrf6, (700, 40))

    # Blit the input boxes
    pg.draw.rect(screen, 'black', input_box1, -1)
    pg.draw.rect(screen, 'black', input_box2, -1)
    pg.draw.rect(screen, 'black', input_box3, -1)

    rotated_image = rotate_image(cannon, theta)
    rect = rotated_image.get_rect(center=(-32, screen_height - 170))
    screen.blit(rotated_image, rect.center)
    screen.blit(cannonball, (x, y))

    if active1 == False:
        txtsrf2 = my_font.render('θ = ' + str(theta + 23.5190522325), False, (0, 0, 0))
    else:
        txtsrf2 = my_font.render('', False, (0, 0, 0))
    screen.blit(txtsrf2, (100, 0))

    if 'txtsrf7' in locals():
        screen.blit(txtsrf7, (50, 500))
    

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()

