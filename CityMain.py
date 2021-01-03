
""" Main Module for City Editor """

import pygame as pg
from pygame.locals import *
import numpy as np
#import MonsterList

#output file inits

dfile = open('diagnost.txt', 'w')
dfile.write('\n')
dfile.write('Diagnostic:')
dfile.close()

tavernFile = open('E8DE-E8F5_inns_data.asm', 'w')
tavernFile.write('inns_data:')
tavernFile.write('\n')
tavernFile.close()

statueFile = open('E856-E87D_guardians.asm', 'w')
statueFile.write('___table_70:')
statueFile.write('\n')
statueFile.close()

ironGatesFile = open('constants_gates.asm', 'w')
ironGatesFile.close()

def main():
    """ Main Program """
    
  
def strip_from_sheet(sheet, start, size, columns, rows):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames

def create_grid (size):
    return ["   0" for _ in range(size)]
 

def dec2hexAll(n):
    if n < 10:
        return '   '+str(n)
    else:
        if n > 9 and n < 16:
           return ' 0'+("%X" % n)+'h'
        else:
            if n > 159:
                return '0'+("%X" % n)+'h'
            else:
                return ' '+("%X" % n)+'h'


def coordsInHex(n):
    print('coords in hex: ' + str(n))
    if n < 10:
        return '0'+str(n)
    else:
        if n > 9 and n < 16:
            return '0'+str("%X" % n)
        else:
            return "%X" % n


def getNorth(x):
    print (x)
    if x == 0:
        north = 29
    else:
        north = 29 - (x // 30)
        print (north)
    if north == 9:
        blankBox(4)
    return north

def getEast(x):
    print (x)
    if x == 0:
        east = 0
    else:
        east = x % 30
        print (east)
    if east == 9:
        blankBox(4)
    return east

def blankBox(selected):
    if selected == 0:   # Blank Selected Building picture box
        pg.draw.rect(screen,BLACK, (1013,3,132,132))
    if selected == 1:   # Blank Selected Text Box
        pg.draw.rect(screen,BLACK, (981,151,198,28))
    if selected == 2:    # Blank Secondary text  box
        pg.draw.rect(screen,BLACK, (981,251,198,28))
    if selected == 3:   # Blank long text information box
        pg.draw.rect(screen,BLACK,(981, 301, 198, 648))
    if selected == 4:   # Blank coordinates box
        pg.draw.rect(screen,BLACK,(1057, 197, 48, 40))
        

def diag(xcount, spaceToFill, spaceLeft, addCount, last):
    dfile = open('diagnost.txt', 'a')
    dfile.write('\n')
    dfile.write("grid count: "+str(xcount))
    dfile.write(" SpaceToFill: "+str(spaceToFill))
    dfile.write(" SpaceLeft: "+str(spaceLeft))
    dfile.write(" AddCount: "+str(addCount))
    dfile.write(" Last: "+str(last))
    dfile.close()

def writeTavern():
    tavernFile = open('E8DE-E8F5_inns_data.asm', 'a')
    for t in range (1, 8):
        tavernFile.write('db  ')
        tavernFile.write(str(INNS[t][2])+', ')
        tavernFile.write(str(INNS[t][3])+', ')
        tavernFile.write(str(INNS[t][1]))
        tavernFile.write('      ; '+str(INNS[t][0])+' Coords + Identifier')
        tavernFile.write('\n')
    tavernFile.write('\n')
    tavernFile.write('default_inn:')
    tavernFile.write('\n')
    tavernFile.write('db 0FFh,0FFh,0')
    tavernFile.close()

def writeStatues():
    statueFile = open('E856-E87D_guardians.asm', 'a')
    for s in range (1, 11):
        statueFile.write('\n')
        statueFile.write('          db    ')
        statueFile.write(str(STATUES[s][7]))
        
    statueFile.write('\n')   
    statueFile.write('\n')
    statueFile.write('GUARDIANS:')
    for s in range (1, 11):
        statueFile.write('\n')
        statueFile.write('          db  ')
        statueFile.write(str(STATUES[s][1]))
        statueFile.write('h')

    statueFile.write('\n')
    statueFile.write('\n')
    statueFile.write('GUARDIAN_COORDS:')
    for s in range (1, 11):
        statueFile.write('\n')
        statueFile.write('          db  ')
        statueFile.write(str(STATUES[s][3]+','+STATUES[s][4]))
    statueFile.close()


def writeGates():
    ironGatesFile = open('constants_gates.asm', 'a')
    for t in range (1, 5):
        ironGatesFile.write('          db  ')
        ironGatesFile.write(str(IRONGATES[t][1])+', ')
        ironGatesFile.write(str(IRONGATES[t][2])+', ')
        ironGatesFile.write(str(IRONGATES[t][5]))
        ironGatesFile.write('      ; '+str(IRONGATES[t][0])+' Coords + Direction')
        ironGatesFile.write('\n')
    ironGatesFile.close()


def pack_2():
    cCount = 1
    spaceToFill = 210     #(900 - 690)
    spaceLeft = 690
    xcount = 0
    addCount = 0
    noPacking = 0
    for x in range(900):      
        if x == 0:  #on first iteration
            last = CityOut[x]
            spaceLeft = spaceLeft - 1
        else:
            xcount = xcount + 1
            if noPacking == 0:
                if CityOut[x] == last:
                    cCount = cCount + 1
                else:                   # on a change     
                    if cCount > (212 - addCount):
                        print ('Do some buffering')
                        packLeft = (212 - addCount)
                        cCount = (cCount - packLeft)
                        if packLeft > 30:           # strip 30 off and continue                                
                            CityPacked.append("0FCh")
                            CityPacked.append(" 1Eh")
                            CityPacked.append(last)
                            packLeft = (packLeft - 30)
                            spaceToFill = spaceToFill - 30
                            spaceLeft = spaceLeft - 3
                            diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            print (">30: Space Left = ", spaceLeft)
                            print ("Space to fill with packing: ", spaceToFill)
                        if packLeft > 3:
                            CityPacked.append("0FCh")
                            CityPacked.append(str(dec2hexAll(packLeft)))
                            CityPacked.append(last)
                            spaceToFill = spaceToFill - cCount 
                            spaceLeft = spaceLeft - 3
                            diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            last = CityOut[x]
                        else:
                                if packLeft == 3:
                                    CityPacked.append(last)
                                    CityPacked.append(last)
                                    CityPacked.append(last)
                                    spaceLeft = spaceLeft - 3
                                    diag(xcount, spaceToFill, spaceLeft, addCount, last)
                                    last = CityOut[x]
                                if packLeft == 2:
                                    CityPacked.append(last)
                                    CityPacked.append(last)
                                    spaceLeft = spaceLeft - 2
                                    diag(xcount, spaceToFill, spaceLeft, addCount, last)
                                    last = CityOut[x]
                                if packLeft == 1:
                                    CityPacked.append(last)
                                    spaceLeft = spaceLeft - 1
                                    diag(xcount, spaceToFill, spaceLeft, addCount, last)
                                    last = CityOut[x]
                        #Write remainder (if any, unpacked)
                        for r in range (1, (cCount+1)):
                            CityPacked.append(last)
                            noPacking = 1
                        dfile = open('diagnost.txt', 'a')
                        dfile.write('\n')
                        dfile.write('remainder: '+str(cCount))
                        dfile.write('packing off')
                        dfile.close()
                        
                    else:       # process normally (CCount less than spaceToFill)
                        if cCount == (212 - addCount):      # if remaining packed space filled exactly, set noPacking for next time
                            noPacking = 1
                            dfile = open('diagnost.txt', 'a')
                            dfile.write('\n')
                            dfile.write("---packed exactly---")
                            dfile.close()
                        if cCount > 30:                     # strip 30 off and continue
                            CityPacked.append("0FCh")
                            CityPacked.append(" 1Eh")
                            CityPacked.append(last)
                            cCount = (cCount - 30)
                            spaceToFill = spaceToFill - 30
                            spaceLeft = spaceLeft - 3
                            addCount = addCount + 27
                            diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            print ("*NP >30: Space Left = ", spaceLeft)
                            print ("Space to fill with packing: ", spaceToFill)
                        if cCount > 3:
                            CityPacked.append("0FCh")                   
                            CityPacked.append(str(dec2hexAll(cCount)))
                            CityPacked.append(last)
                            spaceToFill = spaceToFill - cCount 
                            spaceLeft = spaceLeft - 3
                            addCount = (addCount + cCount) - 3
                            diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            cCount = 1
                            last = CityOut[x]
                            print ("*NP >15: Space Left = ", spaceLeft)
                            print ("Space to fill with packing: ", spaceToFill)
                        else:
                            if cCount == 3:
                                CityPacked.append(last)
                                CityPacked.append(last)
                                CityPacked.append(last)
                                spaceLeft = spaceLeft - 3
                                diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            if cCount == 2:
                                CityPacked.append(last)
                                CityPacked.append(last)
                                spaceLeft = spaceLeft - 2
                                diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            if cCount == 1:
                                CityPacked.append(last)
                                spaceLeft = spaceLeft - 1
                                diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            cCount = 1
                            last = CityOut[x]
            else:  # NoPacking = 1, no more packing...
                    CityPacked.append(CityOut[x])


def find_Guild():
    guildCount = 0
    gfile = open('constants_guild.asm', 'w')
    gfile.write('GUILD_COORDSEQU ')
    for z in range(900):
        if CityOut[z] == "   9":
            if guildCount == 1:
                print("Warning: > 1 Guild, 1st will be start location")
            else:
                guildCount = guildCount + 1
                if z == 0:
                    guild_north = '1D'  #29
                    guild_east = '00'
                else:
                    guild_north = str(coordsInHex(29- ( z// 30)))
                    gfile.write(str(guild_north))
                    guild_east = str(coordsInHex(z % 30))
                    gfile.write(str(guild_east)+'h')
                           

def configureTavern(x):

        print(x)
        doneInn = False
        innValue = 0
        #innText = font.render(INNS[innValue][0], True, RED, BLACK)
        text = font.render(INNS[innValue][0], True, RED, BLACK)
        blankBox(2)
        configText = font.render("Configure Tavern", True, RED, BLACK)
        screen.blit(configText, (1020, 256))

        t0Text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))

        for t in range (1, 8):
            tText = font.render(str(INNS[t][0]), True, RED, BLACK)
            if (INNS[t][2] == '00' and INNS[t][3] == '00'):
                tCoords = font.render("Unassigned", True, RED, BLACK)
            else:
                tCoords = font.render("N: "+str(INNS[t][4])+ "   E: "+str(INNS[t][5]), True, RED, BLACK)
            screen.blit(tText, (1002, (300+(t*50))))
            screen.blit(tCoords, (1010,(320+(t*50))))
        
        while not doneInn:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                   
                    if event.key == pg.K_z:
                        if innValue == 0:
                            innValue = 7
                        else:
                            innValue = innValue - 1
                    if event.key == pg.K_x:
                        if innValue == 7:
                            innValue = 0
                        else:
                            innValue = innValue + 1
                    if event.key == pg.K_c:
                        # confirm
                        #update north coordinate
                        if innValue != 0:   # Don't update coords for default tavern!
                            INNS[innValue][2] = dec2hexAll(getNorth(x))
                            INNS[innValue][3] = dec2hexAll(getEast(x))
                            INNS[innValue][4] = getNorth(x)
                            INNS[innValue][5] = getEast(x)
                            print (INNS[innValue][0])
                            print (INNS[innValue][2])
                            print (INNS[innValue][3])
                        doneInn = True
                        
            
            blankBox(1)
            text = font.render(INNS[innValue][0], True, RED, BLACK)
            screen.blit(text, (1020, 157))
            pg.display.update()

        blankBox(2)
        blankBox(3)
        configText = font.render("  City Editor", True, RED, BLACK)
        screen.blit(configText, (1020, 256))
        t0Text = font.render("Tavern Updated", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))
        pg.display.update()

def configureStatue(x):

        print(x)
        doneStatue = False
        statueValue = 1
        monsterValue = 1
        direction = 0
        text = font.render(STATUES[statueValue][0], True, RED, BLACK)
        blankBox(2)
        blankBox(4)
        configText = font.render("Configure: "+str(STATUES[statueValue][0]), True, RED, BLACK)
        screen.blit(configText, (1010, 256))

        t0Text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))

        for t in range (1, 11):
            sText = font.render('Statue: '+str(t), True, RED, BLACK)
            if STATUES[t][2] == '00':
                tText = font.render("Unassigned", True, RED, BLACK)
            else:
                stat = STATUES[t][2]
                tText = font.render(str(MONSTERS[stat][0]), True, RED, BLACK)
            if (STATUES[t][3] == '00' and STATUES[t][4] == '00'):
                tCoords = font.render("Unassigned", True, RED, BLACK)
            else:
                tCoords = font.render("N: "+str(STATUES[t][5])+ "  E: "+str(STATUES[t][6])+ "  Faces: "+ str(STATUES[t][8]), True, RED, BLACK)
            screen.blit(sText, (1002, (280+(t*60))))
            screen.blit(tText, (1002, (300+(t*60))))
            screen.blit(tCoords, (1010,(320+(t*60))))
        
        while not doneStatue:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                   
                    if event.key == pg.K_z:
                        if statueValue == 1:
                            statueValue = 10
                            blankBox(2)
                        else:
                            statueValue = statueValue - 1
                    if event.key == pg.K_x:
                        if statueValue == 10:
                            statueValue = 1
                            blankBox(2)
                        else:
                            statueValue = statueValue + 1
                    if event.key == pg.K_LEFT:
                        if monsterValue == 1:
                            monsterValue = 127
                        else:
                            monsterValue = monsterValue - 1
                    if event.key == pg.K_DOWN:
                        if monsterValue < 11:
                            monsterValue = 127
                        else:
                            monsterValue = monsterValue - 10
                    if event.key == pg.K_RIGHT:
                        if monsterValue == 127:
                            monsterValue = 1
                        else:
                            monsterValue = monsterValue + 1
                    if event.key == pg.K_UP:
                        if monsterValue > 117:
                            monsterValue = 1
                        else:
                            monsterValue = monsterValue + 10        
                    if event.key == pg.K_j:
                        if direction == 0:
                            direction = 4
                        else:
                            direction = direction - 1
                    if event.key == pg.K_l:
                        if direction == 4:
                            direction = 0
                            blankBox(4)
                        else:
                            direction = direction + 1      
                       
                    if event.key == pg.K_c:
                        # confirm
                        #update north coordinate
                        STATUES[statueValue][1] = MONSTERS[monsterValue][1]
                        STATUES[statueValue][2] = monsterValue
                        STATUES[statueValue][3] = dec2hexAll(getNorth(x))
                        STATUES[statueValue][4] = dec2hexAll(getEast(x))
                        STATUES[statueValue][5] = getNorth(x)
                        STATUES[statueValue][6] = getEast(x)
                        STATUES[statueValue][7] = direction
                        STATUES[statueValue][8] = DIRECTIONS[direction]
                        print (STATUES[statueValue][0])
                        print (STATUES[statueValue][1])
                        print (STATUES[statueValue][2])
                        print (STATUES[statueValue][3])
                        print (STATUES[statueValue][4])
                        print (STATUES[statueValue][5])
                        print (STATUES[statueValue][6])
                        doneStatue = True
                        
            
            blankBox(1)
            text = font.render(str(MONSTERS[monsterValue][0]), True, RED, BLACK)
            screen.blit(text, (1020, 157))
            configText = font.render("Configure: "+str(STATUES[statueValue][0]), True, RED, BLACK)
            screen.blit(configText, (1010, 256))
            face = str(DIRECTIONS[direction])
            directionText = font.render(face, True, RED, BLACK)
            screen.blit(directionText, (1065, 210))
            pg.display.update()

        blankBox(2)
        blankBox(3)
        blankBox(4)
        configText = font.render("  City Editor", True, RED, BLACK)
        screen.blit(configText, (1020, 256))
        t0Text = font.render("Statue Updated", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))
        pg.display.update()

def configureIronGate(x):

        print(x)
        doneGate = False
        gateValue = 1
        direction = 0
        text = font.render(IRONGATES[gateValue][0], True, RED, BLACK)
        blankBox(2)
        blankBox(4)
        configText = font.render("Configure: "+str(IRONGATES[gateValue][0]), True, RED, BLACK)
        screen.blit(configText, (1002, 256))

        t0Text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))

        for g in range (1, 5):
            gText = font.render('Iron Gate: '+str(g), True, RED, BLACK)
            if (IRONGATES[g][3] == '00' and IRONGATES[g][4] == '00'):
                tCoords = font.render("Unassigned", True, RED, BLACK)
            else:
                tCoords = font.render("N: "+str(IRONGATES[g][3])+ "  E: "+str(IRONGATES[g][4])+ "  Faces: "+ str(IRONGATES[g][6]), True, RED, BLACK)
            screen.blit(gText, (1002, (340+(g*60))))
            screen.blit(tCoords, (1010,(360+(g*60))))
        
        while not doneGate:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                   
                    if event.key == pg.K_z:
                        if gateValue == 1:
                            gateValue = 4
                            blankBox(2)
                        else:
                            gateValue = gateValue - 1
                    if event.key == pg.K_x:
                        if gateValue == 4:
                            gateValue = 1
                            blankBox(2)
                        else:
                            gateValue = gateValue + 1     
                    if event.key == pg.K_j:
                        if direction == 0:
                            direction = 4
                        else:
                            direction = direction - 1
                    if event.key == pg.K_l:
                        if direction == 4:
                            direction = 0
                            blankBox(4)
                        else:
                            direction = direction + 1      
                       
                    if event.key == pg.K_c:
                        # confirm
                        #update north coordinate
                        IRONGATES[gateValue][1] = dec2hexAll(getNorth(x))
                        IRONGATES[gateValue][2] = dec2hexAll(getEast(x))
                        IRONGATES[gateValue][3] = getNorth(x)
                        IRONGATES[gateValue][4] = getEast(x)
                        IRONGATES[gateValue][5] = DIRECTIONS_PARAM[direction]
                        IRONGATES[gateValue][6] = DIRECTIONS[direction]
                        print (IRONGATES[gateValue][0])
                        print (IRONGATES[gateValue][1])
                        print (IRONGATES[gateValue][2])
                        print (IRONGATES[gateValue][3])
                        print (IRONGATES[gateValue][4])
                        print (IRONGATES[gateValue][5])
                        print (IRONGATES[gateValue][6])
                        doneGate = True
                        
            
            blankBox(1)
##            text = font.render(str(MONSTERS[monsterValue][0]), True, RED, BLACK)
##            screen.blit(text, (1020, 157))
            configText = font.render("Configure: "+str(IRONGATES[gateValue][0]), True, RED, BLACK)
            screen.blit(configText, (1002, 256))
            face = str(DIRECTIONS[direction])
            directionText = font.render(face, True, RED, BLACK)
            screen.blit(directionText, (1065, 210))
            pg.display.update()

        blankBox(2)
        blankBox(3)
        blankBox(4)
        configText = font.render("  City Editor", True, RED, BLACK)
        screen.blit(configText, (1020, 256))
        t0Text = font.render("Gate Updated", True, RED, BLACK)
        screen.blit(t0Text, (1010, 305))
        pg.display.update()


                     
def write_Out():
    first3 = 1
    eightCount = 0
    hexCount = 0
    print (memNumber)
    myfile = open('F7E7-FA98_city_map.asm', 'w')
    myfile.write('\n')
    myfile.write('CITY_MAP_DATA:  db ')
    for o in range (690):
        print ("index: " + str(o))
        if eightCount == 33:
            myfile.write('; '+ str(dec2hexAll(hexCount)))
            hexCount = hexCount + 32
            eightCount = 1
        if eightCount == 1:
            myfile.write('\n')
            myfile.write('                db ')
            myfile.write(str(CityPacked[o]))
            eightCount = eightCount + 1
        else:
            if eightCount > 0:
                if first3 == 1 and eightCount == 4:     # deal with 1st 3 values
                    first3 = 0
                    myfile.write('\n')
                    myfile.write('                db ')
                    eightCount = 1
                else:
                    myfile.write(',')
            myfile.write(str(CityPacked[o]))
            if eightCount == 0:
                eightCount = eightCount + 2
            else:
                eightCount = eightCount + 1
    # Write Tavern & Statue Coords
    writeTavern()
    writeStatues()
    writeGates()
            
pg.init()
   
screen = pg.display.set_mode((1200,960))
pg.display.set_caption("City Editor")
done = False




CityDisplay = create_grid(900)
CityOut = create_grid(900)

sheet = pg.image.load('CitySpriteSheet32.png')
city = strip_from_sheet(sheet, (0,0), (32,32), 3, 6)

sheetBig = pg.image.load('CitySpriteSheet128.png')
cityBig = strip_from_sheet(sheetBig, (0,0), (128,128), 3, 6)


selectX = 1015
selectY = 5
XPos = 0
YPos = 0
Pointer = 0
LastPointer = 0
LastSelected = 0
selectedBlock = 0
outValue = 0
north = 0
east = 0

x_disp = 0
y_disp = 0
point_disp = 0
  
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

X = 1200
Y = 960
display_surface = pg.display.set_mode((X, Y ))
display_surface.fill(BLACK)

font = pg.font.Font('freesansbold.ttf', 16)
text = font.render('     Blank     ', True, RED, BLACK)
textX = font.render('E: '+str(east), True, RED, BLACK)
textY = font.render('N: 29', True, RED, BLACK)

# text boxes init

#Draw outline around selected building picture
pg.draw.rect(screen,RED,(1012,2,134,134))
pg.draw.rect(screen,BLACK, (1013,3,132,132))

#Draw outline around main text box
pg.draw.rect(screen,RED, (980,150, 200, 30))
pg.draw.rect(screen,BLACK, (981,151,198,28))

#Draw outline around secondary text box
pg.draw.rect(screen,RED, (980,250, 200, 30))
pg.draw.rect(screen,BLACK, (981,251,198,28))

#Draw outline around long information box
pg.draw.rect(screen,RED,(980, 300, 200, 650))
pg.draw.rect(screen,BLACK,(981, 301, 198, 648))

#Draw outline around coordinates box
pg.draw.rect(screen,RED,(1056, 196, 50, 42))
pg.draw.rect(screen,BLACK,(1057, 197, 48, 40))

#Set initial text
configText = font.render("  City Editor", True, RED, BLACK)
screen.blit(configText, (1020, 256))


DIRECTIONS = ['U','N','E','S','W']
DIRECTIONS_PARAM = ['UNASSIGNED','FACE_NORTH','FACE_EAST','FACE_SOUTH','FACE_WEST']


INNS = {
    #Name , output value, N coord HEX, E coord Hex, N coord Dec, E coord Dec
0:  ["Unnamed Tavern", "0", "00", "00", "00", "00"],
1:  [" Scarlet Bard", "44h", "00", "00", "00", "00"],
2:  ["  Sinister Inn", "45h", "00", "00", "00", "00"],
3:  ["Dragon's Breath", "46h", "00", "00", "00", "00"],
4:  [" Ask Y'Mother", "47h", "00", "00", "00", "00"],
5:  [" Archmage Inn", "48h", "00", "00", "00", "00"],
6:  [" Skull Tavern", "49h", "00", "00", "00", "00"],
7:  [" Drawn Blade", "4Ah", "00", "00", "00", "00"]
}

STATUES = {
    #Name , Monster Type (hex), Monster Type Dec, N coord HEX, E coord Hex, N coord Dec, E coord Dec, direction
0:  ["Statue 0", "00", "00", "00", "00", "00", "00", "0", "U"],
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

IRONGATES = {
    #Name, N coord hex, E coord hex, N coord dec, E Coord dec, Direction, Direction display
0:  ["Iron Gate 0", "00", "00", "00", "00", "0", "U"],
1:  ["Iron Gate 1", "00", "00", "00", "00", "0", "U"],
2:  ["Iron Gate 2", "00", "00", "00", "00", "0", "U"],
3:  ["Iron Gate 3", "00", "00", "00", "00", "0", "U"],
4:  ["Iron Gate 4", "00", "00", "00", "00", "0", "U"]
}

MONSTERS = {
0:["Monster","00"],
1:["Kobold","01"],
2:["Hobbit","02"],
3:["Gnome","03"],
4:["Dwarf","04"],
5:["Thief","05"],
6:["Hobgoblin","06"],
7:["Conjurer","07"],
8:["Magician","08"],
9:["Orc","09"],
10:["Skeleton","0A"],
11:["Nomad","0B"],
12:["Spider","0C"],
13:["Mad Dog","0D"],
14:["Barbarian","0E"],
15:["Mercenary","0F"],
16:["Wolf","10"],
17:["Jade Monk","11"],
18:["Half Orc","12"],
19:["Swordsman","13"],
20:["Zombie","14"],
21:["Conjurer","15"],
22:["Magician","16"],
23:["Sorcerer","17"],
24:["Wizard","18"],
25:["Samurai","19"],
26:["Black Widow","1A"],
27:["Assassin","1B"],
28:["Werewolf","1C"],
29:["Ogre","1D"],
30:["Wight","1E"],
31:["Statue","1F"],
32:["Bladesman","20"],
33:["Goblin Lord","21"],
34:["Master Thief","22"],
35:["Conjurer","23"],
36:["Magician","24"],
37:["Sorcerer","25"],
38:["Wizard","26"],
39:["Ninja","27"],
40:["Spinner","28"],
41:["Scarlet Monk","29"],
42:["Doppleganger","2A"],
43:["Stone Giant","2B"],
44:["Ogre Magician","2C"],
45:["Jackalwere","2D"],
46:["Stone Elemental","2E"],
47:["Blue Dragon","2F"],
48:["Seeker","30"],
49:["Dwarf King","31"],
50:["Samurai Lord","32"],
51:["Ghoul","33"],
52:["Conjurer","34"],
53:["Magician","35"],
54:["Sorcerer","36"],
55:["Wizard","37"],
56:["Azure Monk","38"],
57:["Weretiger","39"],
58:["Hydra","3A"],
59:["Green Dragon","3B"],
60:["Wraith","3C"],
61:["Lurker","3D"],
62:["Fire Giant","3E"],
63:["Copper Dragon","3F"],
64:["  Ivory Monk","40"],
65:["   Shadow","41"],
66:[" Berserker","42"],
67:[" Conjurer","43"],
68:[" Magician","44"],
69:[" Sorcerer","45"],
70:["  Wizard","46"],
71:["White Dragon","47"],
72:[" Ice Giant","48"],
73:["  Eye Spy","49"],
74:[" Ogre Lord","4A"],
75:["Body Snatcher","4B"],
76:["   Xorn","4C"],
77:["  Phantom","4D"],
78:[" Lesser Demon","4E"],
79:["   Fred","4F"],
80:[" Conjurer","50"],
81:[" Magician","51"],
82:[" Sorcerer","52"],
83:["  Wizard","53"],
84:["Master Ninja","54"],
85:["  War Giant","55"],
86:["Warrior Elite","56"],
87:["Bone Crusher","57"],
88:["   Ghost","58"],
89:[" Grey Dragon","59"],
90:["  Basilisk","5A"],
91:["  Evil Eye","5B"],
92:["   Mimic","5C"],
93:["   Golem","5D"],
94:["  Vampire","5E"],
95:["   Demon","5F"],
96:[" Bandersnatch","60"],
97:[" Maze Dweller","61"],
98:["   Mongo","62"],
99:["Mangar Guard","63"],
100:["   Gimp","64"],
101:[" Red Dragon","65"],
102:["   Titan","66"],
103:["Master Conjurer","67"],
104:["Master Magician","68"],
105:["Master Sorcerer","69"],
106:[" Mind Shadow","6A"],
107:["  Spectre","6B"],
108:[" Cloud Giant","6C"],
109:["  Beholder","6D"],
110:["Vampire Lord","6E"],
111:["Greater Demon","6F"],
112:["Master Wizard","70"],
113:["  Mad God","71"],
114:["Maze Master","72"],
115:["Death Denizen","73"],
116:["Jabberwock","74"],
117:["Black Dragon","75"],
118:["Mangar","76"],
119:["Crystal Golem","77"],
120:["Soul Sucker","78"],
121:["Storm Giant","79"],
122:["Ancient Enemy","7A"],
123:["   Balrog","7B"],
124:["    Lich","7C"],
125:["  Archmage","7D"],
126:["  Demon Lord","7E"],
127:["   Old Man","7F"]
}

#Draw initial blank grid

for a in range(30):
    for b in range (30):
        screen.blit(city[0], ((a*32),(b*32)))
pg.display.update()

#Loop until the user clicks the close button.
done = False

# -------- Main Program Loop -----------
while not done:
        for event in pg.event.get(): # User did something
            if event.type == pg.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            screen.blit(cityBig[selectedBlock], (selectX,selectY))
            #display_surface.blit(text, textRect)
            blankBox(1)
            screen.blit(text, (1020, 156))
            screen.blit(city[selectedBlock], (XPos,YPos))
            screen.blit(textX, (1060, 200))
            screen.blit(textY, (1060, 220))

            pg.display.update()
 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and selectedBlock > 0:
                    selectedBlock += -1
                        
                elif event.key == pg.K_RIGHT and selectedBlock < 17:
                    selectedBlock += 1
                        
                elif event.key == pg.K_UP and selectedBlock < 17:
                    selectedBlock += 1
                        
                elif event.key == pg.K_DOWN and selectedBlock > 0:
                    selectedBlock += -1
                        
                pg.draw.rect(screen,BLACK,(1000, 200, 20, 20))

                LastPointer = CityDisplay[Pointer]
                x_disp = 0
                y_disp = 0
                point_disp = 0

                if event.key == pg.K_a and XPos > 0:
                    x_disp = -32
                    y_disp = 0
                    point_disp = -1

                if event.key == pg.K_d and XPos < 928:
                    x_disp = 32
                    y_disp = 0
                    point_disp = 1

                if event.key == pg.K_w and YPos > 29:
                    x_disp = 0
                    y_disp = -32
                    point_disp = -30

                if event.key == pg.K_s and YPos < 928:
                    x_disp = 0
                    y_disp = 32
                    point_disp = 30


                LastSelected = int(LastPointer)
                screen.blit(city[LastSelected], ((XPos,YPos)))

               
                XPos += x_disp
                YPos += y_disp
                Pointer += point_disp

                textX = font.render('E: '+str(getEast(Pointer)), True, RED, BLACK)
                textY = font.render('N: '+str(getNorth(Pointer)), True, RED, BLACK)
                
                if event.key == pg.K_p:
                    CityDisplay[Pointer] = selectedBlock
                    CityOut[Pointer] = outValue
                if event.key == pg.K_x:
                    print ('CityOut 0:' + str(CityOut[0]))
                    CityPacked = []
                    # end 64152
                    # start 63466
                    # available memory space = 686
                    memNumber = len(CityPacked)
                    pack_2()
                    print ("Number of items in the list = ", len(CityPacked))
                    if memNumber < 687: # will pack ok
                        write_Out()
                        find_Guild()
                    else:
                        print("City Map will not pack!")
                              
                if event.key == pg.K_c:
                    # configurable properties
                    if CityOut[Pointer] == " 11h":
                        print ('Tavern config')
                        configureTavern(Pointer)
                    if CityOut[Pointer] == " 60h":
                        print ('Statue config')
                        configureStatue(Pointer)
                    if CityOut[Pointer] == " 68h":
                        print ('Iron Gate config')
                        configureIronGate(Pointer)

                HOTKEYS = {
                    pg.K_0: 0,
                    pg.K_1: 1,
                    pg.K_2: 2,
                    pg.K_3: 3,
                    pg.K_4: 4,
                    pg.K_5: 5,
                    pg.K_6: 6,
                    pg.K_7: 7,
                    pg.K_8: 8,
                    pg.K_9: 9,
                }

                selectedBlock = HOTKEYS.get(event.key, selectedBlock)

            BLOCKS = {
                0:  ["       Blank     ", "   0", 'out: 000'],
                1:  [" Empty Building ", "   1", 'out: 001'],
                2:  ["    The Guild   ", "   9", 'out: 009'],
                3:  ["  The  Shoppe  ", " 19h", 'out: 025'],
                4:  ["  Review Board  ", " 29h", 'out: 041'],
                5:  ["       Tavern     ", " 11h", 'out: 017'],
                6:  ["   City Gates   ", "0A8h", 'out: 168'],
                7:  ["       Temple    ", " 21h", 'out: 033'],
                8:  ["     Roscoe's   ", " 89h", 'out: 137'],
                9:  ["Guardian Statue", " 60h", 'out: 096'],
                10: ["    Iron Gate   ", " 68h", 'out: 104'],
                11: ["Mad God Temple ", " 71h", 'out: 113'],
                12: ["      Castle     ", " 99h", 'out: 153'],
                13: ["Kylearans Tower ", " 91h", 'out: 145'],
                14: [" Mangars Tower  ", "0A1h", 'out: 161'],
                15: ["Sewer Entrance ", " 78h", 'out: 120'],
                16: ["  Teleport From ", "   0", 'out: 000'],
                17: ["  Teleport To:  ", "   0", 'out: 000'],
            }    

            if selectedBlock in BLOCKS:
                text = font.render(BLOCKS[selectedBlock][0], True, RED, BLACK)
                outValue = BLOCKS[selectedBlock][1]
                outValRect = font.render(BLOCKS[selectedBlock][2], True, RED, BLACK)



        # Go ahead and update the screen with what we've drawn.
        pg.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pg.quit()
 
if __name__ == "__main__":
    main()
