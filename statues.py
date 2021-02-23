import pygame as pg
from blank_box import *
from support_functions import *
from MonsterList import *

class Statues:
    def __init__(self, filename):
        self.filename = filename
        self.statues = {
            #Name , Monster Type (hex), Monster Type Dec, N coord HEX, E coord Hex, N coord Dec, E coord Dec, direction
            #0:  ["Statue 0", "00", "00", "00", "00", "00", "00", "0", "U"],
            1:  ["Statue 1", "00", "00", "00", "00", "00", "00", "0", "U"],
            2:  ["Statue 2", "00", "00", "00", "00", "00", "00", "0", "U"],
            3:  ["Statue 3", "00", "00", "00", "00", "00", "00", "0", "U"],
            4:  ["Statue 4", "00", "00", "00", "00", "00", "00", "0", "U"],
            5:  ["Statue 5", "00", "00", "00", "00", "00", "00", "0", "U"],
            6:  ["Statue 6", "00", "00", "00", "00", "00", "00", "0", "U"],
            7:  ["Statue 7", "00", "00", "00", "00", "00", "00", "0", "U"],
            8:  ["Statue 8", "00", "00", "00", "00", "00", "00", "0", "U"],
            9:  ["Statue 9", "00", "00", "00", "00", "00", "00", "0", "U"],
            10:  ["Statue 10", "00", "00", "00", "00", "00", "00", "0", "U"]
        }

    # Apply statue data from saved file
    def load_statues(self,cityGrid):
        for statueNumber in range (1,11):
            self.statues[statueNumber] = cityGrid[(statueNumber+40)]

    # Write output for z80 recompile
    def write(self):
        with open(self.filename, 'a') as outfile:
            for statue in self.statues.values():
                outfile.write('\n')
                outfile.write('          db    ')
                outfile.write(f'{statue[7]}')

            outfile.write('\n')
            outfile.write('\n')
            outfile.write('GUARDIANS:')

            for statue in self.statues.values():
                outfile.write('\n')
                outfile.write('          db  ')
                outfile.write(f'{statue[1]}')
                outfile.write('h')

            outfile.write('\n')
            outfile.write('\n')
            outfile.write('GUARDIAN_COORDS:')

            for statue in self.statues.values():
                outfile.write('\n')
                outfile.write('          db  ')
                outfile.write(f'{statue[3]},{statue[4]}')


# Write output for application save/load
    def writeStatues(self):
         with open(DATADIR+'new_city.city', 'a') as cityOutFile:
            for statue in self.statues.values():
                cityOutFile.write(f'{statue[0]}, ')
                cityOutFile.write(f'{statue[1]}, ')
                cityOutFile.write(f'{statue[2]}, ')
                cityOutFile.write(f'{statue[3]}, ')
                cityOutFile.write(f'{statue[4]}, ')
                cityOutFile.write(f'{statue[5]}, ')
                cityOutFile.write(f'{statue[6]}, ')
                cityOutFile.write(f'{statue[7]}, ')
                cityOutFile.write(f'{statue[8]}')
                cityOutFile.write('\n')


    def configure(self, x):
        
        font = pg.font.Font('freesansbold.ttf', 16)
        doneStatue = False
        statueValue = 1
        monsterValue = 1
        direction = 0
        text = font.render(self.statues[statueValue][0], True, RED, BLACK)
        blank_box(2)
        blank_box(4)
        configText = font.render("Configure: "+str(self.statues[statueValue][0]), True, RED, BLACK)
        screen.blit(configText, (1010, 256))
        t0Text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))
        for inx, statue in self.statues.items():
            sText = font.render('Statue: '+str(inx), True, RED, BLACK)
            if statue[2] == '00':
                tText = font.render("Unassigned", True, RED, BLACK)
            else:
                stat = int(statue[2])
                tText = font.render(str(MONSTERS[stat][0]), True, RED, BLACK)
            if (statue[3] == '00' and statue[4] == '00'):
                coords_txt = "Unassigned"
            else:
                coords_txt = f"N: {statue[5]}  E: {statue[6]}  Faces: {statue[8]}"
            tCoords = font.render(coords_txt, True, RED, BLACK)
            screen.blit(sText, (1002, (280+(inx*60))))
            screen.blit(tText, (1002, (300+(inx*60))))
            screen.blit(tCoords, (1010, (320+(inx*60))))
        while not doneStatue:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        if statueValue == 1:
                            statueValue = 10
                            blank_box(2)
                        else:
                            statueValue -= 1
                    elif event.key == pg.K_x:
                        if statueValue == 10:
                            statueValue = 1
                            blank_box(2)
                        else:
                            statueValue += 1
                    elif event.key == pg.K_LEFT:
                        if monsterValue == 1:
                            monsterValue = 127
                        else:
                            monsterValue -= 1
                    elif event.key == pg.K_DOWN:
                        if monsterValue < 11:
                            monsterValue = 127
                        else:
                            monsterValue -= 10
                    elif event.key == pg.K_RIGHT:
                        if monsterValue == 127:
                            monsterValue = 1
                        else:
                            monsterValue += 1
                    elif event.key == pg.K_UP:
                        if monsterValue > 117:
                            monsterValue = 1
                        else:
                            monsterValue += 10
                    elif event.key == pg.K_j:
                        if direction == 0:
                            direction = 4
                        else:
                            direction -= 1
                    elif event.key == pg.K_l:
                        if direction == 4:
                            direction = 0
                            blank_box(4)
                        else:
                            direction += 1
                    elif event.key == pg.K_c:
                        # confirm
                        #update north coordinate
                        self.statues[statueValue] = [
                            self.statues[statueValue][0],
                            MONSTERS[monsterValue][1],
                            monsterValue,
                            dec2hexAll(getNorth(x)),
                            dec2hexAll(getEast(x)),
                            getNorth(x),
                            getEast(x),
                            direction,
                            DIRECTIONS[direction]
                        ]
                        for inx in range(7):
                            print(self.statues[statueValue][inx])
                        doneStatue = True
            blank_box(1)
            text = font.render(str(MONSTERS[monsterValue][0]), True, RED, BLACK)
            screen.blit(text, (1020, 157))
            configText = font.render("Configure: "+str(self.statues[statueValue][0]), True, RED, BLACK)
            screen.blit(configText, (1010, 256))
            face = str(DIRECTIONS[direction])
            directionText = font.render(face, True, RED, BLACK)
            screen.blit(directionText, (1065, 210))
            pg.display.update()
        blank_box(2)
        blank_box(3)
        blank_box(4)
        configText = font.render("  City Editor", True, RED, BLACK)
        screen.blit(configText, (1020, 256))
        t0Text = font.render("Statue Updated", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))
        pg.display.update()
