import pygame as pg
from blank_box import *
from support_functions import *

class IronGates:
    def __init__(self, filename):
        self.filename = filename
        self.irongates = {
            #Name, N coord hex, E coord hex, N coord dec, E Coord dec, Direction, Direction display
            #0:  ["Iron Gate 0", "00", "00", "00", "00", "0", "U"],
            1:  ["Iron Gate 1", "00", "00", "00", "00", "0", "U"],
            2:  ["Iron Gate 2", "00", "00", "00", "00", "0", "U"],
            3:  ["Iron Gate 3", "00", "00", "00", "00", "0", "U"],
            4:  ["Iron Gate 4", "00", "00", "00", "00", "0", "U"]
        }

    # Apply gate data from saved file
    def load_gates(self,cityGrid):
        for gateNumber in range (1,5):
            print (gateNumber)
            print (cityGrid[(gateNumber+36)])
            self.irongates[gateNumber] = cityGrid[(gateNumber+36)]

    # Write output for z80 recompile
    def write(self):
        with open(self.filename, 'a') as outfile:
            for gate in self.irongates.values():
                outfile.write('          db  ')
                outfile.write(f'{gate[1]}, ')
                outfile.write(f'{gate[2]}, ')
                outfile.write(f'{gate[5]}')
                outfile.write(f'      ; {gate[0]} Coords + Direction')
                outfile.write('\n')

    # Write output for application save/load
    def writeGates(self):
        with open(DATADIR+'new_city.city', 'a') as cityOutFile:
            for gate in self.irongates.values():
                cityOutFile.write(f'{gate[0]}, ')
                cityOutFile.write(f'{gate[1]}, ')
                cityOutFile.write(f'{gate[2]}, ')
                cityOutFile.write(f'{gate[3]}, ')
                cityOutFile.write(f'{gate[4]}, ')
                cityOutFile.write(f'{gate[5]}, ')
                cityOutFile.write(f'{gate[6]}')
                cityOutFile.write('\n')


    def configure(self, x):
        
        print(x)
        font = pg.font.Font('freesansbold.ttf', 16)
        doneGate = False
        gateValue = 1
        direction = 0
        blank_box(2)
        blank_box(4)
        configText = font.render("Configure: "+str(self.irongates[gateValue][0]), True, RED, BLACK)
        screen.blit(configText, (1002, 256))
        t0Text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))
        for inx, gate in self.irongates.items():
            gText = font.render('Iron Gate: '+str(inx), True, RED, BLACK)
            if (gate[3] == '00' and gate[4] == '00'):
                coords_txt = "Unassigned"
            else:
                coords_txt = f"N: {gate[3]}  E: {gate[4]}  Faces: {gate[6]}"
            tCoords = font.render(coords_txt, True, RED, BLACK)
            screen.blit(gText, (1002, (340+(inx*60))))
            screen.blit(tCoords, (1010, (360+(inx*60))))
        while not doneGate:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        if gateValue == 1:
                            gateValue = 4
                            blank_box(2)
                        else:
                            gateValue -= 1
                    elif event.key == pg.K_x:
                        if gateValue == 4:
                            gateValue = 1
                            blank_box(2)
                        else:
                            gateValue += 1
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
                        self.irongates[gateValue] = [
                            self.irongates[gateValue][0],
                            dec2hexAll(getNorth(x)),
                            dec2hexAll(getEast(x)),
                            getNorth(x),
                            getEast(x),
                            DIRECTIONS_PARAM[direction],
                            DIRECTIONS[direction]
                        ]
                        for inx in range(7):
                            print(self.irongates[gateValue][inx])
                        doneGate = True
            blank_box(1)
            configText = font.render("Configure: "+str(self.irongates[gateValue][0]), True, RED, BLACK)
            screen.blit(configText, (1002, 256))
            face = str(DIRECTIONS[direction])
            directionText = font.render(face, True, RED, BLACK)
            screen.blit(directionText, (1065, 210))
            pg.display.update()
        blank_box(2)
        blank_box(3)
        blank_box(4)
        configText = font.render("  City Editor", True, RED, BLACK)
        screen.blit(configText, (1020, 256))
        t0Text = font.render("Gate Updated", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))
        pg.display.update()
