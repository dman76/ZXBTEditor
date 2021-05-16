import pygame as pg
pg.init()

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
CYAN = ( 0, 255, 255)

from spritesheet_functions import SpriteSheet
from dungeon_support_funcs import *
import sys
from PIL import Image

CURRDIR = sys.path[0]
DATADIR = CURRDIR + '\\data\\'
 
# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite


def strip_from_sheet(src_sheet, start, size, columns, rows):
    frames = []
    #print('start '+str(start))
    #print('size '+str(size))
    #print('columns '+str(columns))
    #print('rows '+str(rows))
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(src_sheet.subsurface(pg.Rect(location, size)))
    return frames


def draw_boxes(scr):
    boxes = [
        #Draw outline around selected building picture
        (CYAN, (1012, 2, 134, 134)),
        (BLACK, (1013, 3, 132, 132)),

        #Draw outline around main text box
        (CYAN, (980, 150, 200, 30)),
        (BLACK, (981, 151, 198, 28)),

        #Draw outline around secondary text box
        (CYAN, (980, 250, 200, 30)),
        (BLACK, (981, 251, 198, 28)),

        #Draw outline around long information box
        (CYAN, (980, 300, 200, 650)),
        (BLACK, (981, 301, 198, 648)),

        #Draw outline around coordinates box
        (CYAN, (1056, 196, 50, 42)),
        (BLACK, (1057, 197, 48, 40))
    ]

    for box in boxes:
        pg.draw.rect(screen, box[0], box[1])


def saved_grid_to_list():
    savedDungeonData = []

    DUNGEONS = {
        0: 'blank.dun',
        1: 'walledDungeon.dun',
        2: 'WineCellar.dun',
        3: 'Sewers1.dun',
        4: 'Sewers2.dun',
        5: 'Sewers3.dun',
        6: 'Catacombs1.dun',
        7: 'Catacombs2.dun',
        8: 'Catacombs3.dun',
        9: 'Castle1.dun',
        10: 'Castle2.dun',
        11: 'Castle3.dun',
        12: 'Kylearans.dun',
        13: 'Mangars1.dun',
        14: 'Mangars2.dun',
        15: 'Mangars3.dun',
        16: 'Mangars4.dun',
        17: 'Mangars5.dun'
        }

    dungeonname = DUNGEONS.get(sel, None)

    if dungeonname:
        with open(DATADIR+dungeonname, 'r') as grid_dungeon:
           for lines in grid_dungeon:
                #print (lines)
                element_list = [elt.strip() for elt in lines.split(',')]
                savedDungeonData.append(element_list)

                
    return savedDungeonData



def main():
    """Main Program"""

# Open a new window
screen = pg.display.set_mode((1200, 960))
pg.display.set_caption("Dungeon Editor")

# assigning values to X and Y variable 
X = 400
Y = 400

font = pg.font.Font('freesansbold.ttf', 12) 


sheet = pg.image.load(CURRDIR + '/dungeon.png')

dungeonTiles = strip_from_sheet(sheet, (0, 0), (32, 32), 10, 4)

sheetBig = pg.image.load(CURRDIR + '/dungeonBig.png')
dungeonBig = strip_from_sheet(sheetBig, (0, 0), (128, 128), 10, 4)

loadEventIcons = pg.image.load(CURRDIR + '/DungeonEvents8by8.png')
eventsSheet = strip_from_sheet(loadEventIcons, (0, 0), (8, 8), 5, 3)

loadEventBlocks = pg.image.load(CURRDIR + '/DARK_SMOKE_LEECH_big.png')
otherSheet = strip_from_sheet(loadEventBlocks, (0, 0), (32, 32), 5, 1)

cursor = pg.image.load(CURRDIR + '/Cursor.jpg')
cursor.set_alpha(150)

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

bitTable = create_grid(31)

font = pg.font.Font('freesansbold.ttf', 16)

# text boxes init

draw_boxes(screen)

#Set initial text
configText = font.render("Dungeon Edit Mode", True, CYAN, BLACK)
screen.blit(configText, (1020, 256))

text = font.render('     Blank     ', True, CYAN, BLACK)
textX = font.render('E: '+str(east), True, CYAN, BLACK)
textY = font.render('N: 21', True, CYAN, BLACK)

textN = font.render('N: ', True, CYAN, BLACK)
textS = font.render('S: ', True, CYAN, BLACK)
textE = font.render('E: ', True, CYAN, BLACK)
textW = font.render('W: ', True, CYAN, BLACK)
locationText = font.render('', True, CYAN, BLACK)

blockText = create_grid(20)
blockTextNum = 0
blockTextMax = 0

# initial menu
#-------- Select Start Grid -------------

gridSelectText = font.render("Select Grid Type:", True, CYAN, BLACK)
gridBlankText = font.render("0) Empty Grid", True, CYAN, BLACK)
gridWalledText = font.render("1) Walled Dungeon", True, CYAN, BLACK)
gridCellarText = font.render("2) Wine Cellar", True, CYAN, BLACK)
gridSewer1Text = font.render("3) Sewer Level 1", True, CYAN, BLACK)
gridSewer2Text = font.render("4) Sewer Level 2", True, CYAN, BLACK)
gridSewer3Text = font.render("5) Sewer Level 3", True, CYAN, BLACK)
gridCat1Text = font.render("6) Catacombs Level 1", True, CYAN, BLACK)
gridCat2Text = font.render("7) Catacombs Level 2", True, CYAN, BLACK)
gridCat3Text = font.render("8) Catacombs Level 3", True, CYAN, BLACK)
gridCastle1Text = font.render("9) Castle Level 1", True, CYAN, BLACK)
gridCastle2Text = font.render("q) Castle Level 2", True, CYAN, BLACK)
gridCastle3Text = font.render("w) Castle Level 3", True, CYAN, BLACK)
gridKylearansText = font.render("e) Kylearans Tower", True, CYAN, BLACK)
gridMangars1Text = font.render("r) Mangars Tower Level 1", True, CYAN, BLACK)
gridMangars2Text = font.render("t) Mangars Tower Level 2", True, CYAN, BLACK)
gridMangars3Text = font.render("y) Mangars Tower Level 3", True, CYAN, BLACK)
gridMangars4Text = font.render("u) Mangars Tower Level 4", True, CYAN, BLACK)
gridMangars5Text = font.render("i) Mangars Tower Level 5", True, CYAN, BLACK)

screen.blit(gridSelectText, (300,10))
screen.blit(gridBlankText, (320,100))
screen.blit(gridWalledText, (320,120))
screen.blit(gridCellarText, (320,140))
screen.blit(gridSewer1Text, (320,160))
screen.blit(gridSewer2Text, (320,180))
screen.blit(gridSewer3Text, (320,200))
screen.blit(gridCat1Text, (320,220))
screen.blit(gridCat2Text, (320,240))
screen.blit(gridCat3Text, (320,260))
screen.blit(gridCastle1Text, (320,280))
screen.blit(gridCastle2Text, (320,300))
screen.blit(gridCastle3Text, (320,320))
screen.blit(gridKylearansText, (320,340))
screen.blit(gridMangars1Text, (320,360))
screen.blit(gridMangars2Text, (320,380))
screen.blit(gridMangars3Text, (320,400))
screen.blit(gridMangars4Text, (320,420))
screen.blit(gridMangars5Text, (320,440))


pg.display.update()

doneSelect = False
sel = 0

while not doneSelect:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_0:
                sel = 0
                doneSelect = True
            if event.key == pg.K_1:
                sel = 1
                doneSelect = True
            if event.key == pg.K_2:
                sel = 2
                doneSelect = True
            if event.key == pg.K_3:
                sel = 3
                doneSelect = True

pg.display.update()


n = 0
dungeonGrid = saved_grid_to_list()
DungeonOut = create_grid(484)
wallsGrid = create_grid(484)
DungeonEvent = create_grid(484)
Event2 = create_grid(484)

# set up arrays

antiMagicArray = create_grid_ff(32)
teleportFromArray = create_grid_ff(16)
teleportToArray = create_grid_ff(16)
spinnerArray = create_grid_ff(16)
smokeArray = create_grid_ff(16)
HPLeechArray = create_grid_ff(32)
SPRegenArray = create_grid_ff(16)
stasisArray = create_grid_ff(16)
messagesArray = create_grid_ff(16)
fixedEncounterArray = create_grid_ff(16)
specialArray = create_grid_ff(16)



#BIT holding/manipulation table for location
#[0]= holding Bit value
#[1]= count for number limited events
#[2]= max count for number limited events (99 = unlimited)
#[3]= group
#[4]= next bit multiplier for table loop

BIT = {
        1: [0, 0, 99, 0, 1],     #Nbit
        2: [0, 0, 99, 0, 1],     #Nbit
        3: [0, 0, 99, 0, 1],     #Nbit
        4: [0, 0, 99, 0, 4],     #Sbit 
        5: [0, 0, 99, 0, 4],     #Sbit
        6: [0, 0, 99, 0, 4],     #Sbit
        7: [0, 0, 99, 0, 16],     #Ebit 
        8: [0, 0, 99, 0, 16],     #Ebit
        9: [0, 0, 99, 0, 16],     #Ebit
       10: [0, 0, 99, 0, 64],     #Wbit 
       11: [0, 0, 99, 0, 64],     #Wbit
       12: [0, 0, 99, 0, 64],     #Wbit
       13: [0, 0, 99, 1, 1],   #StairsUBit
       14: [0, 0, 99, 1, 2],   #stairsDBit
       15: [0, 0, 99, 3, 8],   #darkBit
       16: [0, 0, 99, 0, 16],   #trapBit
       17: [0, 0, 99, 1, 32],   #portalDBit
       18: [0, 0, 99, 1, 64],   #portalUBit
       19: [0, 0, 99, 2, 128],   #encounterBit
       20: [0, 0, 8, 4, 256],    #messageBit
       21: [0, 0, 8, 0, 512],    #stasisBit
       22: [0, 0, 8, 0, 1024],    #spinnerBit
       23: [0, 0, 8, 0, 2048],    #telFromBit
       24: [0, 0, 8, 0, 4096],    #telToBit
       25: [0, 0, 16, 0, 8192],   #antiMagicBit
       26: [0, 0, 8, 0, 16384],    #spptBit
       27: [0, 0, 8, 2, 32768],    #fixedEncounterBit
       28: [0, 0, 8, 3, 65536],    #smokeBit
       29: [0, 0, 16, 0, 131072],   #leechBit
       30: [0, 0, 8, 4, 262144]     #specialBit  
}


for y in range(22):

    rowElements = dungeonGrid[y]
   
    for x in range(22):
        #map_element = map_to_display(rowElements[x])
        
        #DungeonOut[n] = BLOCKS[map_element][1]
        
        #screen.blit(dungeonTiles[map_element], ((x*32), (y*32)))
        screen.blit(dungeonTiles[0], ((x*32), (y*32)))
        #dungeonGrid[n] = map_element
        #print (map_element)
        n = n + 1


pg.display.update()


# Main loop variable
done = False
selectedBlock = 1

 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pg.event.get(): 
        if event.type == pg.QUIT: 
              done = False 

        screen.blit(dungeonBig[selectedBlock], (selectX, selectY))
        blank_box(1)
        screen.blit(text, (1020, 156))
        screen.blit(textX, (1060, 200))
        screen.blit(textY, (1060, 220))
        blank_box(3)

        # determine which tiles to blit to screen in current location


        walls = int(DungeonOut[Pointer])
        events = int(DungeonEvent[Pointer])

        # Loop and set bits for walls
        for bitSet in range(1,13):
            BIT[bitSet][0] = getBit(walls,BIT[bitSet][4],(BIT[bitSet][4]*2))

        # Loop and set bits for events
        for bitSet in range(13,31):
            BIT[bitSet][0] = getBit(events,BIT[bitSet][4],0)


        # Store bit flags for this location in array

        for bt in range (1, 31):
            bitTable[bt] = BIT[bt][0]


        # Do walls/doors
        blockTextNum = 0
        for bit in range (1, 31):
            if BIT[bit][0] == LU[bit][1]:
                blockTextNum += 1
                blockText[blockTextNum] = str(LU[bit][0])

        # Do event blocks
        #Display Walls/Events text for this location
        
        for txt in range (1, (blockTextNum+1)):
            
            locationText = font.render(str(blockText[txt]), True, CYAN, BLACK)
            screen.blit(locationText, (1000,400+(txt*20)))
                                   
        screen.blit(cursor, (XPos, YPos))

        if event.type == pg.KEYDOWN:   

            if event.key == pg.K_j:      # cursor loops N-W-E-S
                if selectedBlock < 4:
                    selectedBlock += 9
                else:
                    selectedBlock -=3

            if event.key == pg.K_l:       # cursor loops N-S-E-W
                if selectedBlock > 9:
                    selectedBlock -= 9
                else:
                    selectedBlock += 3                   

            if event.key == pg.K_LEFT  and selectedBlock > 0:
                selectedBlock -= 1
            elif event.key == pg.K_RIGHT  and selectedBlock < 30:
                selectedBlock += 1
            elif event.key == pg.K_UP:
                selectedBlock = 30
            elif event.key == pg.K_DOWN:
                selectedBlock = 0
                
            if event.key == pg.K_a and XPos > 0:
                x_disp = -32
                y_disp = 0
                point_disp = -1
            elif event.key == pg.K_d and XPos < 662:
                x_disp = 32
                y_disp = 0
                point_disp = 1
            elif event.key == pg.K_w and YPos > 29:
                x_disp = 0
                y_disp = -32
                point_disp = -22
            elif event.key == pg.K_s and YPos < 662:
                x_disp = 0
                y_disp = 32
                point_disp = 22
            else:
                x_disp = 0
                y_disp = 0
                point_disp = 0

            LastPointer = DungeonOut[Pointer]

            LastSelected = int(LastPointer)

            update_display(dungeonTiles, eventsSheet, otherSheet, XPos, YPos, bitTable)
                                  

            XPos += x_disp
            YPos += y_disp
            Pointer += point_disp

            textX = font.render(f'E: {getEast(Pointer)}', True, CYAN, BLACK)
            textY = font.render(f'N: {getNorth(Pointer)}', True, CYAN, BLACK)

            if selectedBlock in LU:
                text = font.render(LU[selectedBlock][0], True, CYAN, BLACK)

            #Place tile           
            if event.key == pg.K_p: #and mode == 1:
                
                #Do checks to see if tile can be added or updated
                if selectedBlock == 0:
                    DungeonOut[Pointer] = 0   # clear all walls / block values

                    for blank in range (20,31):     # Loop round types limited in number 
                        if BIT[blank][0] > 0:
                            BIT[blank][1] =- 1      # if bit set, decrease count by 1
                            
                    DungeonEvent[Pointer] = 0       # Blank all events
                    
                else:
                    for wallPlace in range (1,13):
                        if wallPlace == selectedBlock:
                            if BIT[wallPlace][0] == 0:
                                walls += (LU[selectedBlock][1])
                                DungeonOut[Pointer] = str(walls)
                            elif LU[selectedBlock][1] != BIT[wallPlace][0]:
                                walls -= BIT[wallPlace][0]
                                walls += (LU[selectedBlock][1])
                                DungeonOut[Pointer] = str(walls)

                    for sb in range (13, 31):
                        if selectedBlock == sb:
                            if BIT[sb][0] == 0:
                                events += (LU[selectedBlock][1])
                                DungeonEvent[Pointer] = str(events)
                                if BIT[sb][2] < 99:
                                    if BIT[sb][1] < BIT[sb][2]:
                                        BIT[sb][1] =+ 1


 
    # --- Go ahead and update the screen with what we've drawn.
    pg.display.flip()
     
 
#Once we have exited the main program loop we can stop the game engine:
pg.quit()

if __name__ == "__main__":
    main()
