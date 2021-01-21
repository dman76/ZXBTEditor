import pygame as pg
import sys
from blank_box import *
CURRDIR = sys.path[0]
DATADIR = CURRDIR + '\\data\\'

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

DIRECTIONS = ['U', 'N', 'E', 'S', 'W']
DIRECTIONS_PARAM = ['UNASSIGNED', 'FACE_NORTH', 'FACE_EAST', 'FACE_SOUTH', 'FACE_WEST']


def create_grid(size):
    return ["   0" for _ in range(size)]
         

def dec2hexAll(num):
    if num < 10:
        return '   '+str(num)
    else:
        if num > 9 and num < 16:
            return ' 0'+("%X" % num)+'h'
        else:
            if num > 159:
                return '0'+("%X" % num)+'h'
            else:
                return ' '+("%X" % num)+'h'


def coordsInHex(num):
    print('coords in hex: ' + str(num))

    if num < 10:
        return '0'+str(num)
    else:
        if num > 9 and num < 16:
            return '0'+str("%X" % num)
        else:
            return "%X" % num

def getNorth(num):
    print(num)

    if num == 0:
        result = 29
    else:
        result = 29 - (num // 30)
        print(result)

    if result == 9:
        blank_box(4)

    return result


def getEast(num):
    print(num)

    if num == 0:
        result = 0
    else:
        result = num % 30
        print(result)

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
