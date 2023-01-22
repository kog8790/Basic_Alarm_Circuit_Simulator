import sys
import os
import pygame
from pygame.locals import KEYDOWN, K_q
pygame.init()
#Gets resolution of desktop to scale program accordingly
[(DESKRES_X, DESKRES_Y)] = pygame.display.get_desktop_sizes()
print(DESKRES_X, DESKRES_Y)

#To Do's
#Switch: blit, class, function
#Short: blit, function
#convert line and common to functions with x y parameters to be called
#Create drop down menu for resistor selection
#Duplicate resReading for common side of circuit
# Constants:
#Sets screensize of program as a percentage of desktop resolution size
SCREENSIZE = WIDTH, HEIGHT = DESKRES_X * .55, DESKRES_X * .55 * .875
print(SCREENSIZE)
#Sets the name of the program and logo in the top bar of the program window
pygame.display.set_caption('Resistance In Alarm Circuit Simulator')
RICC_icon = pygame.image.load(os.path.join('Resistance Calculator Assets', 'RICC_logo.png'))
pygame.display.set_icon(RICC_icon)
#Const colors
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
O_WHITE = (240, 240, 226)
RED = (255, 0, 0)
#Circuit states initialization
series = True
parallel = False
CLOSED = True
OPEN = False
#All images and fonts to be loaded in GUI
RICC_BG = pygame.image.load(os.path.join('Resistance Calculator Assets', 'RICC_V1_BG.png'))
switches_closed = pygame.image.load(os.path.join('Resistance Calculator Assets', 'RICC_BG_SW1_SW2_CLOSED.png'))
sw1_closed = pygame.image.load(os.path.join('Resistance Calculator Assets', 'RICC_BG_SW1_CLOSED.png'))
sw2_closed = pygame.image.load(os.path.join('Resistance Calculator Assets', 'RICC_BG_SW2_CLOSED.png'))
RICC_BG = pygame.transform.scale(RICC_BG, (SCREENSIZE))
font = pygame.font.SysFont('arialbold', 34)
#Const x,y cordinates for circuit begin/end line and common x2
screen1_x = WIDTH * 0.28
screen1_y = HEIGHT * 0.174
screen2_x = WIDTH * 0.55
screen2_y = HEIGHT * 0.174
cir1Ls_term = [WIDTH * 0.274, HEIGHT * 0.311]
cir1Cs_term = [WIDTH * 0.476, HEIGHT * 0.311]
cir1SwLs_term = [WIDTH * 0.279, HEIGHT * 0.737]
cir1SwCs_term = [WIDTH * 0.482, HEIGHT * 0.737]
cir2Ls_term = [WIDTH * 0.715, HEIGHT * 0.311]
cir2Cs_term = [WIDTH * 0.517, HEIGHT * 0.311]
cir2SwLs_term = [WIDTH * 0.721, HEIGHT * 0.737]
cir2SwCs_term = [WIDTH * 0.522, HEIGHT * 0.737]
#display for open circuit
O_C_res_reading = "    i"


border = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

# Resistors
class resistor:
    def __init__(self, ohm, orient, x, y):
        self.ohm = ohm
        self.orient = orient
        self.x = x
        self.y = y
        self.resistor_image = pygame.image.load(os.path.join('Resistance Calculator Assets', 'RICC_10k.png'))
        self.image_size = [WIDTH * .017, HEIGHT * 0.19]
        self.resistor_image = pygame.transform.scale(self.resistor_image, self.image_size)
        if orient == parallel:
            self.image_size = [WIDTH * .015, HEIGHT * 0.23]
            self.resistor_image = pygame.transform.scale(self.resistor_image, self.image_size)
            self.resistor_image = pygame.transform.rotate(self.resistor_image, 90)
        _VARS['surf'].blit(self.resistor_image, (self.x, self.y))

        if (self.ohm == "1k"):
            self.ohm = 998
        elif (self.ohm == "2k"):
            self.ohm = 2004
        elif (self.ohm == "10k"):
            self.ohm = 9989

    def setxy(self, x, y):
        self.x, self.y = x, y
        _VARS['surf'].blit(self.resistor_image, (self.x, self.y))

    def getxy(self):
        return self.x, self.y
    
class switch:
    def __init__(self, O_C, x, y, WIDTH, HEIGHT):
        self.O_C = O_C
        self.x = x
        self.y = y
        self.WIDTH = WIDTH * 0.045
        self.HEIGHT = HEIGHT * 0.070
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)

    def getxy(self):
        return self.x, self.y

class short_circuit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.short_image = pygame.image.load(os.path.join('Resistance Calculator Assets', 'short_circuit.png'))
        self.image_size = [WIDTH * .105, HEIGHT * 0.109]
        self.short_image = pygame.transform.scale(self.short_image, self.image_size)
        _VARS['surf'].blit(self.short_image, (self.x, self.y))

    def setxy(self, x, y):
        self.x, self.y = x, y
        _VARS['surf'].blit(self.short_image, (self.x, self.y))

    def getxy(self):
        return self.x, self.y     




# GLOBAL VAR, Using a Dictionary.
_VARS = {'surf': False}

# This is the main game loop, it constantly runs until you press the Q KEY
# or close the window.
# CAUTION: This will run as fast as your computer allows,
# if you need to seet a specific FPS look at tick methods.

def main():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    is_running = True
    # The loop proper, things inside this loop will
    # be called over and over until you exit the window
    clock = pygame.time.Clock()
    
    s1 = switch(OPEN, WIDTH * 0.353, HEIGHT * 0.830, WIDTH * 0.045, HEIGHT * 0.070)
    s2 = switch(OPEN, WIDTH * 0.596, HEIGHT * 0.830, WIDTH * 0.045, HEIGHT * 0.070)
    r1 = resistor("10k", series, 10, 10)
    r2 = resistor("10k", parallel, 10, 200)
    sh1 = short_circuit(WIDTH * 0.315, HEIGHT * 0.0001)
    sh2 = short_circuit(WIDTH * 0.575, HEIGHT * 0.0001)
    r1_selected = False
    r2_selected = False
    s1_activated = False
    s2_activated = False
    sh1_short = False
    sh2_short = False

    while is_running:
        _VARS['surf'].blit(RICC_BG, (0,0))
        r1_x, r1_y = r1.getxy()
        r2_x, r2_y = r2.getxy()
        #s1_x, s1_y = s1.getxy()
        #s2_x, s2_y = s2.getxy()
        # Resistance Reading
        def resReading(x, y, line_term, com_term, sw_line, sw_com, switch, short):
            rValue = O_C_res_reading
            #short circuit defining characteristics
            if short == True:
                switch.O_C = CLOSED
                pygame.draw.line(_VARS['surf'], GREY, sw_line, sw_com, 3)
                #Resistance calculation and behavior of resistors in circuit
            if r1_x + WIDTH * 0.006 >= line_term[0] and r1_x + WIDTH * 0.006 <= line_term[0] + WIDTH * 0.008:
                if r1_y > line_term[1] - r1.image_size[1] / 4 and r1_y < sw_line[1] + r1.image_size[1] / 5:
                    if r2_x + WIDTH * 0.0005 >= line_term[0] and r2_x + WIDTH * 0.0005 <= line_term[0] + WIDTH * 0.008:
                        if r2_y > line_term[1] and r2_y < sw_line[1]:
                            if r2_y > r1_y + r1.image_size[1] * 0.54:
                                if switch.O_C == CLOSED:
                                    rValue = r1.ohm
                                else:
                                    rValue = r1.ohm + r2.ohm
                            elif r2_y < r1_y + r1.image_size[1] * 0.54:
                                if switch.O_C == CLOSED:
                                    rValue = r2.ohm/2
                                else:
                                    rValue = r2.ohm
                        elif switch.O_C == CLOSED:
                            rValue = r1.ohm
                        else:
                            rValue = O_C_res_reading
                    elif switch.O_C == CLOSED:
                        rValue = r1.ohm
                    else:
                        rValue = O_C_res_reading
                elif r2_x + WIDTH * 0.0007 >= line_term[0] and r2_x + WIDTH * 0.0005 <= line_term[0] + WIDTH * 0.008:
                        if r2_y > line_term[1] and r2_y < sw_line[1]:
                            if switch.O_C == CLOSED:
                                rValue = 0.0
                            else:
                                rValue = r2.ohm
                        elif switch.O_C == CLOSED:
                            rValue = 0.0
                        else:
                            rValue = O_C_res_reading
                elif switch.O_C == CLOSED:
                    rValue = 0.0
                else:
                    rValue = O_C_res_reading

            elif r1_x + WIDTH * 0.006 >= com_term[0] and r1_x + WIDTH * 0.006 <= com_term[0] + WIDTH * 0.008:
                if r1_y > line_term[1] - r1.image_size[1] / 4 and r1_y < sw_line[1] + r1.image_size[1] / 5:
                    if r2_x + WIDTH * 0.0005 >= line_term[0] and r2_x + WIDTH * 0.0005 <= line_term[0] + WIDTH * 0.008:
                        if r2_y > line_term[1] and r2_y < sw_line[1]:
                            if r2_y > r1_y + r1.image_size[1] * 0.54:
                                if switch.O_C == CLOSED:
                                    rValue = r1.ohm
                                else:
                                    rValue = r1.ohm + r2.ohm
                            elif r2_y < r1_y + r1.image_size[1] * 0.54:
                                if switch.O_C == CLOSED:
                                    rValue = r2.ohm/2
                                else:
                                    rValue = r2.ohm
                        elif switch.O_C == CLOSED:
                            rValue = r1.ohm
                        else:
                            rValue = O_C_res_reading
                    elif switch.O_C == CLOSED:
                        rValue = r1.ohm
                    else:
                        rValue = O_C_res_reading
                elif r2_x + WIDTH * 0.0005 >= line_term[0] and r2_x + WIDTH * 0.0005 <= line_term[0] + WIDTH * 0.008:
                        if r2_y > line_term[1] and r2_y < sw_line[1]:
                            if switch.O_C == CLOSED:
                                rValue = 0.0
                            else:
                                rValue = r2.ohm
                else:
                    rValue = O_C_res_reading

            elif r2_x + WIDTH * 0.0005 >= line_term[0] and r2_x + WIDTH * 0.0005 <= line_term[0] + WIDTH * 0.008:
                if r2_y > line_term[1] and r2_y < sw_line[1]:
                    if r1_x + WIDTH * 0.007 >= com_term[0] and r1_x + WIDTH * 0.005 <= com_term[0] + WIDTH * 0.006:
                        if r1_y > line_term[1] - r1.image_size[1] / 4 and r1_y < sw_line[1] + r1.image_size[1] / 5:
                            if r2_y > r1_y + r1.image_size[1] * 0.54:
                                if switch.O_C == CLOSED:
                                    rValue = r1.ohm
                                else:
                                    rValue = r1.ohm + r2.ohm
                            elif r2_y < r1_y + r1.image_size[1] * 0.54:
                                if switch.O_C == CLOSED:
                                    rValue = r2.ohm/2
                            else:
                                rValue = r2.ohm
                        elif switch.O_C == CLOSED:
                            rValue = 0.0
                        else:
                            rValue = r2.ohm
                    elif switch.O_C == CLOSED:
                        rValue = 0.0
                    else:
                        rValue = r2.ohm
                elif switch.O_C == CLOSED:
                    rValue = 0.0
                else:
                    rValue = O_C_res_reading
            elif switch.O_C == CLOSED:
                    rValue = 0.0
            res = font.render(str(rValue) + " Ohms", True, (0,0,0))
            #Alarm state print message defining characteristics
            if rValue == O_C_res_reading:
                alarm_state = "TRBL OPEN"
            elif rValue >= 4875.0 and rValue <= 5175.5 or rValue >= 19675.0 and rValue <= 21135.0:
                alarm_state = "   ALARM"
            elif rValue >= 9715.0 and rValue <= 10175.0:
                alarm_state = "  SECURED"
            elif rValue == 0.0:
                alarm_state = "TRBL SHORT"
            else:
                alarm_state = "TRBL UNDEFINED"
            if alarm_state == "ALARM":
                message = font.render(alarm_state, True, (255, 0, 0))
            else:
                message = font.render(alarm_state, True, (0, 0, 255))
            _VARS['surf'].blit(res, (x, y))
            _VARS['surf'].blit(message, (x, y * 1.5))
            
        if not r1_selected:
            r1.setxy(r1_x, r1_y)
        if not r2_selected:   
           r2.setxy(r2_x, r2_y)
        
        if s1_activated == True:
            s1.O_C = CLOSED
            pygame.draw.line(_VARS['surf'], BLACK, cir1SwLs_term, cir1SwCs_term, 5)
            pygame.draw.circle(_VARS['surf'], RED, (WIDTH * 0.378, HEIGHT * 0.881), 13.5)
        else:
            s1.O_C = OPEN
                
        if s2_activated == True:
            s2.O_C = CLOSED
            pygame.draw.line(_VARS['surf'], BLACK, cir2SwLs_term, cir2SwCs_term, 5)
            pygame.draw.circle(_VARS['surf'], RED, (WIDTH * 0.620, HEIGHT * 0.881), 13.5)
        else:
            s2.O_C = OPEN

        sh1.setxy(sh1.x, sh1.y)
        sh2.setxy(sh2.x, sh2.y)
            
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
            
            #Mouse event handling
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if s1.rect.collidepoint(event.pos):
                    if s1_activated == False:
                        s1_activated = True
                    else:
                        s1_activated = False
                elif s2.rect.collidepoint(event.pos):
                    if s2_activated == False:
                        s2_activated = True
                    else:
                        s2_activated = False

                if sh1.short_image.get_rect(topleft=sh1.getxy()).collidepoint(event.pos):
                    if sh1_short == False:
                        sh1_short = True
                    else:
                        sh1_short = False

                elif sh2.short_image.get_rect(topleft=sh2.getxy()).collidepoint(event.pos):
                    if sh2_short == False:
                        sh2_short = True
                    else:
                        sh2_short = False

                if r1.resistor_image.get_rect(topleft=r1.getxy()).collidepoint(event.pos):
                    r1_selected = True
                    selected_offset_x = r1.resistor_image.get_rect(topleft=r1.getxy()).x - event.pos[0]
                    selected_offset_y = r1.resistor_image.get_rect(topleft=r1.getxy()).y - event.pos[1]
               
                elif r2.resistor_image.get_rect(topleft=r2.getxy()).collidepoint(event.pos):
                    r2_selected = True
                    selected_offset_x = r2.resistor_image.get_rect(topleft=r2.getxy()).x - event.pos[0]
                    selected_offset_y = r2.resistor_image.get_rect(topleft=r2.getxy()).y - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                r1_selected = False
                r2_selected = False

            elif event.type == pygame.MOUSEMOTION:
                if r1_selected:
                    r1.setxy(event.pos[0] + selected_offset_x, event.pos[1] + selected_offset_y)
                if r2_selected:
                    r2.setxy(event.pos[0] + selected_offset_x, event.pos[1] + selected_offset_y)
        
        resReading(screen1_x, screen1_y, cir1Ls_term, cir1Cs_term, cir1SwLs_term, cir1SwCs_term, s1, sh1_short)
        resReading(screen2_x, screen2_y, cir2Cs_term, cir2Ls_term, cir2SwCs_term, cir2SwLs_term, s2, sh2_short)
        clock.tick(30)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
