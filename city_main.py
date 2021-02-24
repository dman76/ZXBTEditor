""" Main Module for City Editor """

#import numpy as np
import pygame as pg
#from pygame.locals import *
import sys


import MonsterList
from support_functions import *
from blank_box import *
from irongates import IronGates
from statues import Statues
from taverns import Taverns


CURRDIR = sys.path[0]
DATADIR = CURRDIR + '\\data\\'

#output file inits


with open(DATADIR+'diagnost.txt', 'w') as dfile:
    dfile.write('\n')
    dfile.write('Diagnostic:')

with open(DATADIR+'E8DE-E8F5_inns_data.asm', 'w') as tavernFile:
    tavernFile.write('inns_data:')
    tavernFile.write('\n')

with open(DATADIR+'E856-E87D_guardians.asm', 'w') as statueFile:
    statueFile.write('___table_70:')
    statueFile.write('\n')

with open(DATADIR+'constants_gates.asm', 'w') as ironGatesFile:
    pass



def strip_from_sheet(src_sheet, start, size, columns, rows):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(src_sheet.subsurface(pg.Rect(location, size)))
    return frames


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
                        print('Do some buffering')
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
                            print(">30: Space Left = ", spaceLeft)
                            print("Space to fill with packing: ", spaceToFill)

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
                        for _ in range(1, (cCount+1)):
                            CityPacked.append(last)
                            noPacking = 1

                        with open(DATADIR+'diagnost.txt', 'a') as outfile:
                            outfile.write('\n')
                            outfile.write('remainder: '+str(cCount))
                            outfile.write('packing off')

                    else:       # process normally (CCount less than spaceToFill)
                        if cCount == (212 - addCount):      # if remaining packed space filled exactly, set noPacking for next time
                            noPacking = 1
                            with open('diagnost.txt', 'a') as outfile:
                                outfile.write('\n')
                                outfile.write("---packed exactly---")
                        if cCount > 30:                     # strip 30 off and continue
                            CityPacked.append("0FCh")
                            CityPacked.append(" 1Eh")
                            CityPacked.append(last)
                            cCount = (cCount - 30)
                            spaceToFill = spaceToFill - 30
                            spaceLeft = spaceLeft - 3
                            addCount = addCount + 27
                            diag(xcount, spaceToFill, spaceLeft, addCount, last)
                            print("*NP >30: Space Left = ", spaceLeft)
                            print("Space to fill with packing: ", spaceToFill)
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
                            print("*NP >15: Space Left = ", spaceLeft)
                            print("Space to fill with packing: ", spaceToFill)
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

    with open(DATADIR+'constants_guild.asm', 'w') as gfile:
        gfile.write('GUILD_COORDSEQU ')

        for inx in range(900):
            if CityOut[inx] == "   9":
                if guildCount == 1:
                    print("Warning: > 1 Guild, 1st will be start location")
                else:
                    guildCount += 1

                    if inx == 0:
                        guild_north = '1D'  #29
                        guild_east = '00'
                    else:
                        guild_north = str(coordsInHex(29- (inx//30)))
                        gfile.write(str(guild_north))
                        guild_east = str(coordsInHex(inx % 30))
                        gfile.write(str(guild_east)+'h')


def write_Out():
    first3 = 1
    eightCount = 0
    hexCount = 0
    print(memNumber)

    with open(DATADIR + 'F7E7-FA98_city_map.asm', 'w') as myfile:
        myfile.write('\n')
        myfile.write('CITY_MAP_DATA:  db ')
        for o in range(690):
            
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

    myfile.close()
    
    # Write Tavern & Statue Coords
    taverns.write()
    statues.write()
    irongates.write()


def write_Map(CityOut):     
# This function writes map for load/save format for editor rather than for z80 recompile
    with open(DATADIR+'new_city.city', 'w') as cityOutFile:
        lineCount = 0
        for x in range(900):
            if lineCount == 30:
                cityOutFile.write('\n')
                lineCount = 0
            if lineCount == 29:
                cityOutFile.write(str(CityOut[x]))
            else:
                cityOutFile.write(str(CityOut[x])+',')
            lineCount = lineCount + 1
    taverns.writeTavern()
    irongates.writeGates()
    statues.writeStatues()
    cityOutFile.close()


def draw_boxes(scr):
    boxes = [
        #Draw outline around selected building picture
        (RED, (1012, 2, 134, 134)),
        (BLACK, (1013, 3, 132, 132)),

        #Draw outline around main text box
        (RED, (980, 150, 200, 30)),
        (BLACK, (981, 151, 198, 28)),

        #Draw outline around secondary text box
        (RED, (980, 250, 200, 30)),
        (BLACK, (981, 251, 198, 28)),

        #Draw outline around long information box
        (RED, (980, 300, 200, 650)),
        (BLACK, (981, 301, 198, 648)),

        #Draw outline around coordinates box
        (RED, (1056, 196, 50, 42)),
        (BLACK, (1057, 197, 48, 40))
    ]

    for box in boxes:
        pg.draw.rect(screen, box[0], box[1])




def saved_grid_to_list():
    savedCityData = []

    CITIES = {
        1: 'blankMap.city',
        2: 'walledCity.city',
        3: 'Skara_Brae.city',
        4: 'new_city.city'
        }

    cityname = CITIES.get(sel, None)

    if cityname:
        with open(DATADIR+cityname, 'r') as grid_city:
           for lines in grid_city:
                element_list = [elt.strip() for elt in lines.split(',')]
                savedCityData.append(element_list)

                
    return savedCityData

def map_to_display(mS):

    mapSquare = mS.strip()

    SQUARES = {
        "0": 0,
        "1": 1,
        "9": 2,
        "19h" : 3,
        "29h" : 4,
        "11h" : 5,
        "0A8h": 6,
        "21h" : 7,
        "89h" : 8,
        "60h" : 9,
        "68h" : 10,
        "71h" : 11,
        "99h" : 12,
        "91h" : 13,
        "0A1h": 14,
        "78h" : 15
        }
    
    return SQUARES.get(mapSquare, 0)   

def main():
    """ Main Program """


pg.init()

screen = pg.display.set_mode((1200, 960))
pg.display.set_caption("City Editor")
done = False

CityDisplay = create_grid(900)
CityOut = create_grid(900)

sheet = pg.image.load(CURRDIR + '/CitySpriteSheet32.png')
city = strip_from_sheet(sheet, (0, 0), (32, 32), 3, 6)

sheetBig = pg.image.load(CURRDIR + '/CitySpriteSheet128.png')
cityBig = strip_from_sheet(sheetBig, (0, 0), (128, 128), 3, 6)


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


X = 1200
Y = 960
display_surface = pg.display.set_mode((X, Y))
display_surface.fill(BLACK)

font = pg.font.Font('freesansbold.ttf', 16)
text = font.render('     Blank     ', True, RED, BLACK)
textX = font.render('E: '+str(east), True, RED, BLACK)
textY = font.render('N: 29', True, RED, BLACK)

# initial menu
#-------- Select Start Grid -------------

gridSelectText = font.render("Select Grid Type:", True, RED, BLACK)
gridBlankText = font.render("E)mpty Grid", True, RED, BLACK)
gridSkaraText = font.render("S)kara Brae", True, RED, BLACK)
gridWallsText = font.render("W)alled City", True, RED, BLACK)
gridLoadText = font.render("L)oad Previous", True, RED, BLACK)

screen.blit(gridSelectText, (300,10))
screen.blit(gridBlankText, (320,100))
screen.blit(gridSkaraText, (320,120))
screen.blit(gridWallsText, (320,140))
screen.blit(gridLoadText, (320,160))

pg.display.update()

doneSelect = False
sel = 0

while not doneSelect:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                sel = 1
                doneSelect = True
            if event.key == pg.K_w:
                sel = 2
                doneSelect = True
            if event.key == pg.K_s:
                sel = 3
                doneSelect = True
            if event.key == pg.K_l:
                sel = 4
                doneSelect = True


pg.display.update()

# text boxes init

draw_boxes(screen)

#Set initial text
configText = font.render("  City Editor", True, RED, BLACK)
screen.blit(configText, (1020, 256))



#Draw grid based on selected type

cityGrid = saved_grid_to_list()
print (cityGrid)

n = 0    

for y in range(30):
    rowElements = cityGrid[y]
   
    for x in range(30):

        map_element = map_to_display(rowElements[x])
        CityOut[n] = BLOCKS[map_element][1]
        
        screen.blit(city[map_element], ((x*32), (y*32)))
        CityDisplay[n] = map_element
        n = n + 1


statues = Statues(DATADIR+'E856-E87D_guardians.asm')
irongates = IronGates(DATADIR+'constants_gates.asm')
taverns = Taverns(DATADIR+'E8DE-E8F5_inns_data.asm')

taverns.load_taverns(cityGrid)
statues.load_statues(cityGrid)
irongates.load_gates(cityGrid)

pg.display.update()


#Loop until the user clicks the close button.
done = False

# -------- Main Program Loop -----------
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            break

        screen.blit(cityBig[selectedBlock], (selectX, selectY))
        blank_box(1)
        screen.blit(text, (1020, 156))
        screen.blit(city[selectedBlock], (XPos, YPos))
        screen.blit(textX, (1060, 200))
        screen.blit(textY, (1060, 220))

        pg.display.update()

        if event.type == pg.KEYDOWN:
            pg.draw.rect(screen, BLACK, (1000, 200, 20, 20))

            if event.key == pg.K_LEFT and selectedBlock > 0:
                selectedBlock -= 1
            elif event.key == pg.K_RIGHT and selectedBlock < 17:
                selectedBlock += 1
            elif event.key == pg.K_UP and selectedBlock < 17:
                selectedBlock += 1
            elif event.key == pg.K_DOWN and selectedBlock > 0:
                selectedBlock -= 1
            elif event.key == pg.K_a and XPos > 0:
                x_disp = -32
                y_disp = 0
                point_disp = -1
            elif event.key == pg.K_d and XPos < 928:
                x_disp = 32
                y_disp = 0
                point_disp = 1
            elif event.key == pg.K_w and YPos > 29:
                x_disp = 0
                y_disp = -32
                point_disp = -30
            elif event.key == pg.K_s and YPos < 928:
                x_disp = 0
                y_disp = 32
                point_disp = 30
            else:
                x_disp = 0
                y_disp = 0
                point_disp = 0

            LastPointer = CityDisplay[Pointer]

            LastSelected = int(LastPointer)
            screen.blit(city[LastSelected], ((XPos, YPos)))

            XPos += x_disp
            YPos += y_disp
            Pointer += point_disp

            textX = font.render(f'E: {getEast(Pointer)}', True, RED, BLACK)
            textY = font.render(f'N: {getNorth(Pointer)}', True, RED, BLACK)

            if event.key == pg.K_p:
                CityDisplay[Pointer] = selectedBlock
                CityOut[Pointer] = outValue
            elif event.key == pg.K_x:
                CityPacked = []
                # end 64152
                # start 63466
                # available memory space = 686
                memNumber = len(CityPacked)
                pack_2()
                print(f"Number of items in the list = {len(CityPacked)}")
                if memNumber < 690: # will pack ok
                    #city_io.write_Map()
                    write_Out()
                    find_Guild()
                    write_Map(CityOut)
                else:
                    print("City Map will not pack!")
            elif event.key == pg.K_c:
                # configurable properties
                if CityOut[Pointer] == " 11h":
                    print('Tavern config')
                    taverns.configure(Pointer)
                elif CityOut[Pointer] == " 60h":
                    print('Statue config')
                    statues.configure(Pointer)
                elif CityOut[Pointer] == " 68h":
                    print('Iron Gate config')
                    irongates.configure(Pointer)

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
