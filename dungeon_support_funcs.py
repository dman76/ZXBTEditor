#python # -*- coding: utf-8 -*-

import sys

import pygame as pg

from blank_box import *


CURRDIR = sys.path[0]
DATADIR = CURRDIR + '\\data\\'

cursorN = pg.image.load(CURRDIR + '/WallCursor-N.jpg')
cursorE = pg.image.load(CURRDIR + '/WallCursor-E.jpg')
cursorS = pg.image.load(CURRDIR + '/WallCursor-S.jpg')
cursorW = pg.image.load(CURRDIR + '/WallCursor-W.jpg')

#sheet = pg.image.load(CURRDIR + '/dungeon.png')
#dungeonTiles = strip_from_sheet(sheet, (0, 0), (32, 32), 10, 4)

blockImage = pg.Surface([32,32]).convert_alpha()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


#LOOK UP TABLE
# 0: Description, 1: Bit value, 2: Cursor Direction or 2nd bit
# 3: print x pos, 4: print y pos, 5: x size in pix, 6: y size in pix
# 7: index as an integer, 8: display order
LU = {
    0:  ["       Blank     ",  0, cursorN, 0, 0, 0, 0, 0, 0],
    1:  ["     North Wall  ",  1, cursorN, 0, 0,32, 4, 1, 0],
    2:  ["     North Door  ",  2, cursorN, 0, 0,32, 4, 2, 0],
    3:  ["Secret North Door",  3, cursorN, 0, 0,32, 4, 3, 0],
    4:  ["     South Wall  ",  4, cursorS, 0,28,32, 4, 4, 0],
    5:  ["     South Door  ",  8, cursorS, 0,28,32, 4, 5, 0],
    6:  ["Secret South Door", 12, cursorS, 0,28,32, 4, 6, 0],
    7:  ["     East Wall   ", 16, cursorE,28, 0, 4,32, 7, 0],
    8:  ["     East Door   ", 32, cursorE,28, 0, 4,32, 8, 0],
    9:  ["Secret East Door ", 48, cursorE,28, 0, 4,32, 9, 0],
    10: ["     West Wall   ", 64, cursorW, 0, 0, 4,32,10, 0],
    11: ["     West Door   ",128, cursorW, 0, 0, 4,32,11, 0],
    12: ["Secret West Door ",192, cursorW, 0, 0, 4,32,12, 0],
    13: ["     Stairs Up   ",  1, 0, 0, 0, 0, 0, 13, 0],
    14: ["    Stairs Down  ",  2, 0, 0, 0, 0, 0, 14, 1],
    15: ["     Darkness!   ",  8, 0, 0, 0,32,32, 15,99],
    16: ["        Trap     ", 16, 0, 0, 0, 0, 0, 16, 4],
    17: ["     Portal Down ", 32, 0, 0, 0, 0, 0, 17, 2],
    18: ["     Portal Up   ", 64, 0, 0, 0, 0, 0, 18, 3],
    19: ["Random Encounter ",128, 0, 0, 0, 0, 0, 19, 5],
    20: ["     Message     ",256, 4, 0, 0, 0, 0, 20, 6],
    21: [" Stasis Chamber  ",512, 4, 0, 0, 0, 0, 21, 7],
    22: ["      Spinner    ",1024, 4, 0, 0, 0, 0, 22,8],
    23: ["  Teleport From: ",2048, 4, 0, 0, 0, 0, 23,9],
    24: ["   Teleport To:  ",4096, 4, 0, 0, 0, 0, 24,10],
    25: ["Anti-Magic Zone  ",8192, 4, 0, 0, 0, 0, 25,11],
    26: ["SpellPoint Regen ",16384, 4, 0, 0, 0, 0,26,12],
    27: ["  Fixed Encounter",32768, 4, 0, 0, 0, 0,27,13],
    28: [" Smoke in Eyes   ",65536, 4, 0, 0,32,32,28,99],
    29: [" Hit Point Leech ",131072, 4, 0, 0,32,32,29,99],
    30: ["     Special     ",262144, 4, 0, 0, 0, 0,30,14]
}

EVENT_ICON = {
    1: [8,8],
    2: [16,8],
    3: [8,16],
    4: [16,16]
}

DIRECTIONS = ['U', 'N', 'E', 'S', 'W']
DIRECTIONS_PARAM = ['UNASSIGNED', 'FACE_NORTH', 'FACE_EAST', 'FACE_SOUTH', 'FACE_WEST']

def update_display(dungeonTiles, eventsSheet, otherSheet, XPos, YPos, bitTable):

    blockImage.blit(dungeonTiles[0], (0,0)) # clear previous


    # Add dark/smoke/HP Leech backgrounds if required

    if bitTable[15] > 0:  #Darkness
        if bitTable[29] > 0:  # Dark + Leech 
            blockImage.blit(otherSheet[4], (0,0), (0,0,32,32))
        else:                # Dark only
            blockImage.blit(otherSheet[0], (0,0), (0,0,32,32))
    if bitTable[28] > 0: # Smoke
        if bitTable[29] > 0:  # Smoke + Leech
            blockImage.blit(otherSheet[3], (0,0), (0,0,32,32))
        else:                # Smoke only
            blockImage.blit(otherSheet[1], (0,0), (0,0,32,32))

    if bitTable[29] > 0 and (bitTable[15] == 0 and bitTable[28] == 0):  #HP Leech only
        blockImage.blit(otherSheet[2], (0,0), (0,0,32,32))

    # Loop and add walls
 
    for b in range (1, 13):
        if LU[b][1] == bitTable[b]:
            blockImage.blit(dungeonTiles[(LU[b][7])], (LU[b][3],LU[b][4]), (LU[b][3],LU[b][4],LU[b][5],LU[b][6]))


    displayEventIcon = 0

    # Loop and add events (display maximum of 4)

    for b in range (13, 31):
        if b != 15 and b != 28 and b != 29:    # already catered for darkness/smoke/Leech
            if LU[b][1] == bitTable[b]:
                if displayEventIcon < 4:
                    displayEventIcon = displayEventIcon + 1
                    blockImage.blit(eventsSheet[(LU[b][8])], (EVENT_ICON[displayEventIcon][0],EVENT_ICON[displayEventIcon][1]))


    screen.blit(blockImage, (XPos, YPos))



def create_grid(size):
    return ["   0" for _ in range(size)]

def create_grid_ff(size):
    return ["FF" for _ in range(size)]

def dec2hexAll(num):
    return f" #{num:02X}"


def coordsInHex(num):
    return f"{num:02X}"

def getBit(walls, bit1, bit2):
    return ((walls & bit1) + (walls & bit2))


def getNorth(num):
    result = 21 if num == 0 else 21 - (num // 22)

    if result == 9:
        blank_box(4)

    return result


def getEast(num):
    result = num % 22

    if result == 9:
        blank_box(4)

    return result


def diag(xcount, space_to_fill, space_left, add_count, last):
    with open(DATADIR+'diagnost.txt', 'a') as outfile:
        outfile.write('\n')
        outfile.write(f"grid count: {xcount}")
        outfile.write(f" SpaceToFill: {space_to_fill}")
        outfile.write(f" SpaceLeft: {space_left}")
        outfile.write(f" AddCount: {add_count}")
        outfile.write(f" Last: {last}")


def dump_data(filename, data):
    with open(filename, 'a') as outfile:
        #-*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++outfile.write('\n')

        for obj in data.values():
            obj_data = ', '.join(obj)
            outfile.write(f'{obj_data}\n')
