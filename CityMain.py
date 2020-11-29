
""" Main Module for City Editor """

import pygame as pg
from pygame.locals import *
import numpy as np


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
    squares = []
    for n in range (size):
        location = "   0"
        squares.append(location)
    return squares
 
def dec2hex(n):
    return "%X" % n

def dec2hex10_16(n):
    if n == 10:
        hexValue = ' 0Ah'
    if n == 11:
        hexValue = ' 0Bh'
    if n == 12:
        hexValue = ' 0Ch'
    if n == 13:
        hexValue = ' 0Dh'
    if n == 14:
        hexValue = ' 0Eh'
    if n == 15:
        hexValue = ' 0Fh'
    return hexValue

def getCoords(x):
    print (x)
    if x == 0:
        north = 29
        east = 0
    else:
        north = 29 - (x // 30)
        east = x % 30
        textX = font.render(str(east), True, RED, BLACK)
        textY = font.render(str(north), True, RED, BLACK)
        pg.display.update()
        print (north)
        print (east)
    #return N, E

def pack_2():
    #CityOut.reverse()
    cCount = 1
    # spacetoFill needs to equal 900-x
    spaceToFill = 210     #(900 - 690)
    spaceLeft = 690
    dfile = open('diagnost.txt', 'w')
    dfile.write('\n')
    dfile.write('Diagnostic:')
    xcount = 0
    addCount = 0
    noPacking = 0
    for x in range(900):      
        if x == 0:  #on first iteration
            last = CityOut[x]
            spaceLeft = spaceLeft - 1
        else:
            xcount = xcount + 1
            #print ("Space left = ", spaceLeft)
            #print ("Space to fill with packing: ", spaceToFill)
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
                            dfile.write('\n')
                            dfile.write("grid count: "+str(xcount))
                            dfile.write(" SpaceToFill: "+str(spaceToFill))
                            dfile.write(" SpaceLeft: "+str(spaceLeft))
                            dfile.write(" AddCount: "+str(addCount))
                            dfile.write(" Last: "+str(last))
                            print (">30: Space Left = ", spaceLeft)
                            print ("Space to fill with packing: ", spaceToFill)
                        if packLeft > 15:
                            CityPacked.append("0FCh")                   
                            CityPacked.append(' '+str(dec2hex(packLeft))+'h')
                            CityPacked.append(last)
                            spaceToFill = spaceToFill - cCount 
                            spaceLeft = spaceLeft - 3
                            dfile.write('\n')
                            dfile.write("grid count: "+str(xcount))
                            dfile.write(" SpaceToFill: "+str(spaceToFill))
                            dfile.write(" SpaceLeft: "+str(spaceLeft))
                            dfile.write(" AddCount: "+str(addCount))
                            dfile.write(" Last: "+str(last))
                            last = CityOut[x]
                            print (">15: Space Left = ", spaceLeft)
                            print ("Space to fill with packing: ", spaceToFill)
                        else:
                            if packLeft > 9:
                                CityPacked.append("0FCh")
                                CityPacked.append(str(dec2hex10_16(packLeft)))                         
                                CityPacked.append(last)
                                spaceToFill = spaceToFill - cCount 
                                spaceLeft = spaceLeft - 3
                                dfile.write('\n')
                                dfile.write("grid count: "+str(xcount))
                                dfile.write(" SpaceToFill: "+str(spaceToFill))
                                dfile.write(" SpaceLeft: "+str(spaceLeft))
                                dfile.write(" AddCount: "+str(addCount))
                                dfile.write(" Last: "+str(last))
                                last = CityOut[x]
                                print (">9: Space Left = ", spaceLeft)
                                print ("Space to fill with packing: ", spaceToFill)
                            else:
                                if packLeft > 3:
                                    CityPacked.append("0FCh")                           
                                    CityPacked.append('   '+str(packLeft))
                                    CityPacked.append(last)
                                    spaceToFill = spaceToFill - cCount 
                                    spaceLeft = spaceLeft - 3
                                    dfile.write('\n')
                                    dfile.write("grid count: "+str(xcount))
                                    dfile.write(" SpaceToFill: "+str(spaceToFill))
                                    dfile.write(" SpaceLeft: "+str(spaceLeft))
                                    dfile.write(" AddCount: "+str(addCount))
                                    dfile.write(" Last: "+str(last))
                                    last = CityOut[x]
                                    print (">3: Space Left = ", spaceLeft)
                                    print ("Space to fill with packing: ", spaceToFill)
                                else:
                                    if packLeft == 3:
                                        CityPacked.append(last)
                                        CityPacked.append(last)
                                        CityPacked.append(last)
                                        spaceLeft = spaceLeft - 3
                                        dfile.write('\n')
                                        dfile.write("grid count: "+str(xcount))
                                        dfile.write(" SpaceToFill: "+str(spaceToFill))
                                        dfile.write(" SpaceLeft: "+str(spaceLeft))
                                        dfile.write(" AddCount: "+str(addCount))
                                        dfile.write(" Last: "+str(last))
                                        last = CityOut[x]
                                    if packLeft == 2:
                                        CityPacked.append(last)
                                        CityPacked.append(last)
                                        spaceLeft = spaceLeft - 2
                                        dfile.write('\n')
                                        dfile.write("grid count: "+str(xcount))
                                        dfile.write(" SpaceToFill: "+str(spaceToFill))
                                        dfile.write(" SpaceLeft: "+str(spaceLeft))
                                        dfile.write(" AddCount: "+str(addCount))
                                        dfile.write(" Last: "+str(last))
                                        last = CityOut[x]
                                    if packLeft == 1:
                                        CityPacked.append(last)
                                        spaceLeft = spaceLeft - 1
                                        dfile.write('\n')
                                        dfile.write("grid count: "+str(xcount))
                                        dfile.write(" SpaceToFill: "+str(spaceToFill))
                                        dfile.write(" SpaceLeft: "+str(spaceLeft))
                                        dfile.write(" AddCount: "+str(addCount))
                                        dfile.write(" Last: "+str(last))
                                        last = CityOut[x]
                        #Write remainder (if any, unpacked)
                        for r in range (1, (cCount+1)):
                            CityPacked.append(last)
                            noPacking = 1
                        dfile.write('\n')
                        dfile.write('remainder: '+str(cCount))
                        dfile.write('packing off')
                        
                    else:       # process normally (CCount less than spaceToFill)
                        if cCount == (212 - addCount):      # if remaining packed space filled exactly, set noPacking for next time
                            noPacking = 1
                            dfile.write('\n')
                            dfile.write("---packed exactly---")
                        if cCount > 30:                     # strip 30 off and continue
                            CityPacked.append("0FCh")
                            CityPacked.append(" 1Eh")
                            CityPacked.append(last)
                            cCount = (cCount - 30)
                            spaceToFill = spaceToFill - 30
                            spaceLeft = spaceLeft - 3
                            addCount = addCount + 27
                            dfile.write('\n')
                            dfile.write("grid count: "+str(xcount))
                            dfile.write(" SpaceToFill: "+str(spaceToFill))
                            dfile.write(" SpaceLeft: "+str(spaceLeft))
                            dfile.write(" AddCount: "+str(addCount))
                            dfile.write(" Last: "+str(last))
                            print ("*NP >30: Space Left = ", spaceLeft)
                            print ("Space to fill with packing: ", spaceToFill)
                        if cCount > 15:
                            CityPacked.append("0FCh")                   
                            CityPacked.append(' '+str(dec2hex(cCount))+'h')
                            CityPacked.append(last)
                            spaceToFill = spaceToFill - cCount 
                            spaceLeft = spaceLeft - 3
                            addCount = (addCount + cCount) - 3
                            dfile.write('\n')
                            dfile.write("grid count: "+str(xcount))
                            dfile.write(" SpaceToFill: "+str(spaceToFill))
                            dfile.write(" SpaceLeft: "+str(spaceLeft))
                            dfile.write(" AddCount: "+str(addCount))
                            dfile.write(" Last: "+str(last))
                            cCount = 1
                            last = CityOut[x]
                            print ("*NP >15: Space Left = ", spaceLeft)
                            print ("Space to fill with packing: ", spaceToFill)
                        else:
                            if cCount > 9:
                                CityPacked.append("0FCh")
                                CityPacked.append(str(dec2hex10_16(cCount)))                         
                                CityPacked.append(last)
                                spaceToFill = spaceToFill - cCount 
                                spaceLeft = spaceLeft - 3
                                addCount = (addCount + cCount) - 3
                                dfile.write('\n')
                                dfile.write("grid count: "+str(xcount))
                                dfile.write(" SpaceToFill: "+str(spaceToFill))
                                dfile.write(" SpaceLeft: "+str(spaceLeft))
                                dfile.write(" AddCount: "+str(addCount))
                                dfile.write(" Last: "+str(last))
                                cCount = 1
                                last = CityOut[x]
                                print ("*NP >9: Space Left = ", spaceLeft)
                                print ("Space to fill with packing: ", spaceToFill)
                            else:
                                if cCount > 3:
                                    CityPacked.append("0FCh")                           
                                    CityPacked.append('   '+str(cCount))
                                    CityPacked.append(last)
                                    spaceToFill = spaceToFill - cCount 
                                    spaceLeft = spaceLeft - 3
                                    addCount = (addCount + cCount) - 3
                                    dfile.write('\n')
                                    dfile.write("grid count: "+str(xcount))
                                    dfile.write(" SpaceToFill: "+str(spaceToFill))
                                    dfile.write(" SpaceLeft: "+str(spaceLeft))
                                    dfile.write(" AddCount: "+str(addCount))
                                    dfile.write(" Last: "+str(last))
                                    cCount = 1
                                    last = CityOut[x]
                                    print ("*NP >3: Space Left = ", spaceLeft)
                                    print ("Space to fill with packing: ", spaceToFill)
                                else:
                                    if cCount == 3:
                                        CityPacked.append(last)
                                        CityPacked.append(last)
                                        CityPacked.append(last)
                                        spaceLeft = spaceLeft - 3
                                        dfile.write('\n')
                                        dfile.write("grid count: "+str(xcount))
                                        dfile.write(" SpaceToFill: "+str(spaceToFill))
                                        dfile.write(" SpaceLeft: "+str(spaceLeft))
                                        dfile.write(" Last: "+str(last))
                                    if cCount == 2:
                                        CityPacked.append(last)
                                        CityPacked.append(last)
                                        spaceLeft = spaceLeft - 2
                                        dfile.write('\n')
                                        dfile.write("grid count: "+str(xcount))
                                        dfile.write(" SpaceToFill: "+str(spaceToFill))
                                        dfile.write(" SpaceLeft: "+str(spaceLeft))
                                        dfile.write(" Last: "+str(last))
                                    if cCount == 1:
                                        CityPacked.append(last)
                                        spaceLeft = spaceLeft - 1
                                        dfile.write('\n')
                                        dfile.write("grid count: "+str(xcount))
                                        dfile.write(" SpaceToFill: "+str(spaceToFill))
                                        dfile.write(" SpaceLeft: "+str(spaceLeft))
                                        dfile.write(" Last: "+str(last))
                                    cCount = 1
                                    last = CityOut[x]
            else:  # NoPacking = 1, no more packing...
                    CityPacked.append(CityOut[x])
    #CityOut.reverse()

def find_Guild():
    gridCount = 0
    guildCount = 0
    gfile = open('constants_guild.asm', 'w')
    gfile.write('GUILD_COORDS	EQU ')
    for z in range(900):
        gridCount = gridCount + 1
        if CityOut[z] == "   9":
            if guildCount > 1:
                print("Warning: > 1 Guild, 1st will be start location")
            else:
                guildCount = guildCount + 1
                if z == 0:
                    guild_north = '1D'  #29
                    guild_east = '00'
                else:
                    guild_north = 29 - (z // 30)
                    if guild_north > 15:
                        guild_north = str(dec2hex(guild_north))
                    else:
                        if guild_north > 9:
                                if guild_north == 10:
                                    guild_north = '0A'
                                if guild_north == 11:
                                    guild_north = '0B'
                                if guild_north == 12:
                                    guild_north = '0C'
                                if guild_north == 13:
                                    guild_north = '0D'
                                if guild_north == 14:
                                    guild_north = '0E'
                                if guild_north == 15:
                                    guild_north = '0F'
                        else:
                            guild_north = '0'+str(guild_north)
                    gfile.write(str(guild_north))
                    guild_east = z % 30
                    if guild_east > 15:
                        guild_east = str(dec2hex(guild_east))
                    else:
                        if guild_east > 9:
                                if guild_east == 10:
                                    guild_east = '0A'
                                if guild_east == 11:
                                    guild_east = '0B'
                                if guild_east == 12:
                                    guild_east = '0C'
                                if guild_east == 13:
                                    guild_east = '0D'
                                if guild_east == 14:
                                    guild_east = '0E'
                                if guild_east == 15:
                                    guild_east = '0F'
                        else:
                            guild_east = '0'+str(guild_east)
                    gfile.write(str(guild_east)+'h')
        

def pack_grid():
    conseqCount = 1
    for z in range(900):
        if z == 0: # on first iteration
            last = CityOut[z]
        else:
            if CityOut[z] == last:
                conseqCount = conseqCount + 1
                if z == 899: # write out on final iteration if = to previous
                    if conseqCount > 3:
                        CityPacked.append("0FCh")
                        CityPacked.append(str(' '+dec2hex(conseqCount))+'h')
                        CityPacked.append(last)
                    else:
                        if conseqCount == 3:
                            CityPacked.append(last)
                            CityPacked.append(last)
                            CityPacked.append(last)
                        if conseqCount == 2:
                            CityPacked.append(last)
                            CityPacked.append(last)
                        if conseqCount == 1:
                            CityPacked.append(last)
            else:   # When changes
                if conseqCount > 3: # can pack
                    if conseqCount > 30:
                        remainder = conseqCount - 30
                        CityPacked.append("0FCh")
                        if conseqCount > 9:
                                if conseqCount == 10:
                                    CityPacked.append(' 0Ah')
                                if conseqCount == 11:
                                    CityPacked.append(' 0Bh')
                                if conseqCount == 12:
                                    CityPacked.append(' 0Ch')
                                if conseqCount == 13:
                                    CityPacked.append(' 0Dh')
                                if conseqCount == 14:
                                    CityPacked.append(' 0Eh')
                                if conseqCount == 15:
                                    CityPacked.append(' 0Fh')
                                if conseqCount > 15:
                                    CityPacked.append(str(' '+dec2hex(30))+'h')
                        else:
                            CityPacked.append('   '+str(conseqCount))
                        CityPacked.append(last)
                        if remainder > 3:
                            CityPacked.append("0FCh")
                            if remainder > 9:
                                if remainder == 10:
                                    CityPacked.append(' 0Ah')
                                if remainder == 11:
                                    CityPacked.append(' 0Bh')
                                if remainder == 12:
                                    CityPacked.append(' 0Ch')
                                if remainder == 13:
                                    CityPacked.append(' 0Dh')
                                if remainder == 14:
                                    CityPacked.append(' 0Eh')
                                if remainder == 15:
                                    CityPacked.append(' 0Fh')
                                if remainder > 15:
                                    CityPacked.append(str(' '+dec2hex(remainder))+'h')
                                    #CityPacked.append('  '+str(conseqCount))
                        else:
                            if remainder == 3:
                                CityPacked.append(last)
                                CityPacked.append(last)
                                CityPacked.append(last)
                            if remainder == 2:
                                CityPacked.append(last)
                                CityPacked.append(last)
                            if remainder == 1:
                                CityPacked.append(last)
                        conseqCount = 1
                        last = CityOut[z]
                    else:    
                        CityPacked.append("0FCh")
                        if conseqCount > 9:
                                if conseqCount == 10:
                                    CityPacked.append(' 0Ah')
                                if conseqCount == 11:
                                    CityPacked.append(' 0Bh')
                                if conseqCount == 12:
                                    CityPacked.append(' 0Ch')
                                if conseqCount == 13:
                                    CityPacked.append(' 0Dh')
                                if conseqCount == 14:
                                    CityPacked.append(' 0Eh')
                                if conseqCount == 15:
                                    CityPacked.append(' 0Fh')
                                if conseqCount > 15:                         
                                    CityPacked.append(str(' '+dec2hex(conseqCount))+'h')
                        else:
                            CityPacked.append(last)
                        conseqCount = 1
                        last = CityOut[z]
                else:
                    if conseqCount == 3:
                        CityPacked.append(last)
                        CityPacked.append(last)
                        CityPacked.append(last)
                    if conseqCount == 2:
                        CityPacked.append(last)
                        CityPacked.append(last)
                    if conseqCount == 1:
                        CityPacked.append(last)
                    conseqCount = 1
                    last = CityOut[z]
                    
                
def write_Out():
    first3 = 1
    eightCount = 0
    hexCount = 0
    myfile = open('F7E7-FA98_city_map.asm', 'w')
    print (memNumber)
    myfile.write('\n')
    myfile.write('CITY_MAP_DATA:  db ')
    for o in range (690):
        print ("index: " + str(o))
        if eightCount == 33:
            myfile.write('; '+ str(dec2hex(hexCount)))
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
            
pg.init()
   
screen = pg.display.set_mode((1200,960))
#screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
#screen_rect = screen.get_rect()
pg.display.set_caption("City Editor")
done = False

CityDisplay = create_grid(900)
CityOut = create_grid(900)
#print ('CityOut 0:' + str(CityOut[0]))
#CityPacked = []

sheet = pg.image.load('CitySpriteSheet32.png')
city = strip_from_sheet(sheet, (0,0), (32,32), 3, 6)

sheetBig = pg.image.load('CitySpriteSheet128.png')
cityBig = strip_from_sheet(sheetBig, (0,0), (128,128), 3, 6)


selectX = 1000
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
#textX = font.render(str(0), True, RED, BLACK)
#textY = font.render(str(0), True, RED, BLACK)
textX = font.render('E: '+str(east), True, RED, BLACK)
textY = font.render('N: '+str(north), True, RED, BLACK)
textOut = font.render('000', True, RED, BLACK)

# create a rectangular object for the 
# text surface object 
textRect = text.get_rect()  
  
# set the center of the rectangular object. 
textRect = (selectX, 200)

coordxRect = textX.get_rect()
coordxRect = (selectX, 250)
coordyRect = textY.get_rect()
coordyRect = (selectX, 275)
outValRect = textOut.get_rect()
outValRect = (selectX, 540)

# text boxes init
pg.draw.rect(screen,RED,(1000, 300, 150, 500))
pg.draw.rect(screen,BLACK,(1001, 301, 148, 498))
pg.draw.rect(screen,BLACK,(1000, 200, 200, 10))

pg.draw.rect(screen,BLACK,(1000, 250, 100, 100))


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

            #screen.blit(city[0], screen_rect.center)
            screen.blit(cityBig[selectedBlock], (selectX,selectY))
            display_surface.blit(text, textRect)
            screen.blit(text, textRect)
            screen.blit(city[selectedBlock], (XPos,YPos))
            #display_surface.blit(textOut, outValRect)
            #getCoords(Pointer)
            #textX = font.render(str(east), True, RED, BLACK)
            #textY = font.render(str(north), True, RED, BLACK)
            display_surface.blit(textX, coordxRect)
            display_surface.blit(textY, coordyRect)
            screen.blit(textX, (1000, 250))
            screen.blit(textY, (1000, 275))
            pg.display.update()
 
            if event.type == pg.KEYDOWN:
                #getCoords(Pointer)
                #print (north)
                #print (east)
                if event.key == pg.K_LEFT:
                    if selectedBlock > 0:
                        selectedBlock = selectedBlock - 1
                        pg.draw.rect(screen,BLACK,(1000, 200, 200, 20))
                if event.key == pg.K_RIGHT:
                    if selectedBlock < 17:
                        selectedBlock = selectedBlock + 1
                        pg.draw.rect(screen,BLACK,(1000, 200, 200, 20))
                if event.key == pg.K_UP:
                    if selectedBlock < 17:
                        selectedBlock = selectedBlock + 1
                        pg.draw.rect(screen,BLACK,(1000, 200, 200, 20))
                if event.key == pg.K_DOWN:
                    if selectedBlock > 0:
                        selectedBlock = selectedBlock - 1
                        pg.draw.rect(screen,BLACK,(1000, 200, 200, 20))
                if event.key == pg.K_a:
                    if XPos > 0:
                        XPos = XPos - 32
                        LastPointer = CityDisplay[Pointer]
                        Pointer = Pointer - 1
                        LastSelected = int(LastPointer)
                        screen.blit(city[LastSelected], ((XPos+32,YPos)))
                        pg.draw.rect(screen,BLACK,(1000, 250, 100, 100))
                        getCoords(Pointer)
                if event.key == pg.K_d:
                    if XPos < 928:
                        XPos = XPos + 32
                        LastPointer = CityDisplay[Pointer]
                        Pointer = Pointer + 1
                        LastSelected = int(LastPointer)
                        screen.blit(city[LastSelected], ((XPos-32,YPos)))
                        pg.draw.rect(screen,BLACK,(1000, 250, 100, 100))
                        getCoords(Pointer)
                if event.key == pg.K_w:
                    if Pointer > 29:
                        YPos = YPos - 32
                        LastPointer = CityDisplay[Pointer]
                        Pointer = Pointer - 30
                        LastSelected = int(LastPointer)
                        screen.blit(city[LastSelected], ((XPos,YPos+32)))
                        pg.draw.rect(screen,BLACK,(1000, 250, 100, 100))
                        getCoords(Pointer)
                if event.key == pg.K_s:
                    if Pointer < 870:
                        YPos = YPos + 32
                        LastPointer = CityDisplay[Pointer]
                        Pointer = Pointer + 30
                        LastSelected = int(LastPointer)
                        screen.blit(city[LastSelected], ((XPos,YPos-32)))
                        pg.draw.rect(screen,BLACK,(1000, 250, 100, 100))
                        getCoords(Pointer)
                if event.key == pg.K_p:
                    CityDisplay[Pointer] = selectedBlock
                    CityOut[Pointer] = outValue
                if event.key == pg.K_x:
                    #CityOut = create_grid(900)
                    print ('CityOut 0:' + str(CityOut[0]))
                    CityPacked = []
                    #pack_grid()
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
                              

                #hotkeys
                if event.key == pg.K_0:
                    selectedBlock = 0

                if event.key == pg.K_1:
                    selectedBlock = 1

                if event.key == pg.K_2:
                    selectedBlock = 2

                if event.key == pg.K_3:
                    selectedBlock = 3

                if event.key == pg.K_4:
                    selectedBlock = 4

                if event.key == pg.K_5:
                    selectedBlock = 5

                if event.key == pg.K_6:
                    selectedBlock = 6

                if event.key == pg.K_7:
                    selectedBlock = 7

                if event.key == pg.K_8:
                    selectedBlock = 8

                if event.key == pg.K_9:
                    selectedBlock = 9

                #textX = str(XPos)
                #textY = str(YPos)
                #coordxRect = font.render((XPos), True, RED, BLACK)
                #coordyRect = font.render((YPos), True, RED, BLACK)


            if selectedBlock == 0:
                text = font.render('      Blank     ', True, RED, BLACK)
                outValue = "   0"
                outValRect = font.render('out: 000', True, RED, BLACK)
            if selectedBlock == 1:
                text = font.render(' Empty Building ', True, RED, BLACK)
                outValue = "   1"
                outValRect = font.render('out: 001', True, RED, BLACK)
            if selectedBlock == 2:
                text = font.render('   The Guild    ', True, RED, BLACK)
                outValue = "   9"
                outValRect = font.render('out: 009', True, RED, BLACK)
            if selectedBlock == 3:
                text = font.render('   The Shoppe   ', True, RED, BLACK)
                outValue = " 19h"
                outValRect = font.render('out: 025', True, RED, BLACK)
            if selectedBlock == 4:
                text = font.render('  Review Board  ', True, RED, BLACK)
                outValue = " 29h"
                outValRect = font.render('out: 041', True, RED, BLACK)
            if selectedBlock == 5:
                text = font.render('       Inn      ', True, RED, BLACK)
                outValue = " 11h"
                outValRect = font.render('out: 017', True, RED, BLACK)
            if selectedBlock == 6:
                text = font.render('    City Gates  ', True, RED, BLACK)
                outValue = "0A8h"
                outValRect = font.render('out: 168', True, RED, BLACK)
            if selectedBlock == 7:
                text = font.render('      Temple    ', True, RED, BLACK)
                outValue = " 21h"
                outValRect = font.render('out: 033', True, RED, BLACK)
            if selectedBlock == 8:
                text = font.render('     Roscoe''s  ', True, RED, BLACK)
                outValue = " 89h"
                outValRect = font.render('out: 137', True, RED, BLACK)
            if selectedBlock == 9:
                text = font.render(' Guardian Statue', True, RED, BLACK)
                outValue = " 60h"
                outValRect = font.render('out: 096', True, RED, BLACK)
            if selectedBlock == 10:
                text = font.render('    Iron Gate   ', True, RED, BLACK)
                outValue = " 68h"
                outValRect = font.render('out: 104', True, RED, BLACK)
            if selectedBlock == 11:
                text = font.render(' Mad God Temple ', True, RED, BLACK)
                outValue = " 71h"
                outValRect = font.render('out: 113', True, RED, BLACK)
            if selectedBlock == 12:
                text = font.render('      Castle    ', True, RED, BLACK)
                outValue = " 99h"
                outValRect = font.render('out: 153', True, RED, BLACK)
            if selectedBlock == 13:
                text = font.render('Kylearans Tower ', True, RED, BLACK)
                outValue = " 91h"
                outValRect = font.render('out: 145', True, RED, BLACK)
            if selectedBlock == 14:
                text = font.render('  Mangars Tower ', True, RED, BLACK)
                outValue = "0A1h"
                outValRect = font.render('out: 161', True, RED, BLACK)
            if selectedBlock == 15:
                text = font.render(' Sewer Entrance ', True, RED, BLACK)
                outValue = " 78h"
                outValRect = font.render('out: 120', True, RED, BLACK)
            if selectedBlock == 16:
                text = font.render(' Teleport From  ', True, RED, BLACK)
                outValue = "   0"
                outValRect = font.render('out: 0', True, RED, BLACK)
            if selectedBlock == 17:
                text = font.render(' Teleport To:   ', True, RED, BLACK)
                outValue = "   0"
                outValRect = font.render('out: 0', True, RED, BLACK)


        # Go ahead and update the screen with what we've drawn.
        pg.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pg.quit()
 
if __name__ == "__main__":
    main()
