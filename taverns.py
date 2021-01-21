import pygame as pg
from blank_box import *
from support_functions import *

class Taverns:
    def __init__(self, filename):
        self.filename = filename
        self.taverns = {
            #Name , output value, N coord HEX, E coord Hex, N coord Dec, E coord Dec
            #0:  ["Unnamed Tavern", "0", "00", "00", "00", "00"],
            1:  [" Scarlet Bard", "44h", "00", "00", "00", "00"],
            2:  ["  Sinister Inn", "45h", "00", "00", "00", "00"],
            3:  ["Dragon's Breath", "46h", "00", "00", "00", "00"],
            4:  [" Ask Y'Mother", "47h", "00", "00", "00", "00"],
            5:  [" Archmage Inn", "48h", "00", "00", "00", "00"],
            6:  [" Skull Tavern", "49h", "00", "00", "00", "00"],
            7:  [" Drawn Blade", "4Ah", "00", "00", "00", "00"]
        }            


    def write(self):
        with open(self.filename, 'a') as outfile:
            for tavern in self.taverns.values():
                outfile.write('db  ')
                outfile.write(f'{tavern[2]}, ')
                outfile.write(f'{tavern[3]}, ')
                outfile.write(f'{tavern[1]}')
                outfile.write(f'      ; {tavern[0]} Coords + Identifier')
                outfile.write('\n')

            outfile.write('\n')
            outfile.write('default_inn:')
            outfile.write('\n')
            outfile.write('db 0FFh,0FFh,0')


    def configure(self, x):
        
        print(x)
        font = pg.font.Font('freesansbold.ttf', 16)
        doneInn = False
        innValue = 1
        #innText = font.render(INNS[innValue][0], True, RED, BLACK)
        text = font.render(self.taverns[innValue][0], True, RED, BLACK)
        blank_box(2)
        configText = font.render("Configure Tavern", True, RED, BLACK)
        screen.blit(configText, (1020, 256))
        t0Text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0Text, (1010, 310))
        #for inx, tavern in INNS.items():
        for inx, tavern in self.taverns.items():
            tText = font.render(f'{tavern[0]}', True, RED, BLACK)
            if (tavern[2] == '00' and tavern[3] == '00'):
                coords_txt = "Unassigned"
            else:
                coords_txt = f"N: {tavern[4]}   E: {tavern[5]}"
            tCoords = font.render(coords_txt, True, RED, BLACK)
            screen.blit(tText, (1002, (300+(inx*50))))
            screen.blit(tCoords, (1010, (320+(inx*50))))
        while not doneInn:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        if innValue == 1:
                            innValue = 7
                        else:
                            innValue -= 1
                    elif event.key == pg.K_x:
                        if innValue == 7:
                            innValue = 1
                        else:
                            innValue += 1
                    elif event.key == pg.K_c:
                        # confirm
                        #update north coordinate
                        #if innValue != 0:   # Don't update coords for default tavern!
                        self.taverns[innValue][2] = dec2hexAll(getNorth(x))
                        self.taverns[innValue][3] = dec2hexAll(getEast(x))
                        self.taverns[innValue][4] = getNorth(x)
                        self.taverns[innValue][5] = getEast(x)
                        print(self.taverns[innValue][0])
                        print(self.taverns[innValue][2])
                        print(self.taverns[innValue][3])
                        doneInn = True
            blank_box(1)
            text = font.render(self.taverns[innValue][0], True, RED, BLACK)
            screen.blit(text, (1020, 157))
            pg.display.update()
        blank_box(2)
        blank_box(3)
        configText = font.render("  City Editor", True, RED, BLACK)
        screen.blit(configText, (1020, 256))
        t0Text = font.render("Tavern Updated", True, RED, BLACK)
        screen.blit(t0Text, (1010, 310))
        pg.display.update()
