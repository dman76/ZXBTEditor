""" Main Module for City Editor """

import sys

import pygame as pg
#from pygame.locals import *

from support_functions import BLACK, RED, BLOCKS
from support_functions import diag, dec2hex_all, coords_in_hex, create_grid, get_north, get_east
from irongates import IronGates
from statues import Statues
from taverns import Taverns


CURRDIR = sys.path[0]
DATADIR = CURRDIR + '\\data\\'

X = 1200
Y = 960


def prepare_files():
    """Prepare files for output"""

    with open(DATADIR+'diagnost.txt', 'w') as dfile:
        dfile.write('\n')
        dfile.write('Diagnostic:')

    with open(DATADIR+'E8DE-E8F5_inns_data.asm', 'w') as tavernfile:
        tavernfile.write('inns_data:')
        tavernfile.write('\n')

    with open(DATADIR+'E856-E87D_guardians.asm', 'w') as statuefile:
        statuefile.write('___table_70:')
        statuefile.write('\n')

    with open(DATADIR+'constants_gates.asm', 'w') as gatesfile:
        gatesfile.write('\n')


def strip_from_sheet(src_sheet, start, size, columns, rows):
    """Get surface from sheet"""

    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(src_sheet.subsurface(pg.Rect(location, size)))
    return frames


def blank_box(scr, selected):
    """Draw blank box """

    boxes = {
        0: (1013, 3, 132, 132),    # Blank Selected Building picture box
        1: (981, 151, 198, 28),    # Blank Selected Text Box
        2: (981, 251, 198, 28),    # Blank Secondary text  box
        3: (981, 301, 198, 648),   # Blank long text information box
        4: (1057, 197, 48, 40)     # Blank coordinates box
    }

    coords = boxes.get(selected, None)

    if coords:
        pg.draw.rect(scr, BLACK, coords)


def pack_2(city_out, city_packed):
    """Encode city data"""

    c_count = 1
    space_to_fill = 210     #(900 - 690)
    space_left = 690
    xcount = 0
    add_count = 0
    no_packing = 0

    for inx in range(900):
        if inx == 0:  #on first iteration
            last = city_out[inx]
            space_left -= 1
        else:
            xcount += 1
            if no_packing == 0:
                if city_out[inx] == last:
                    c_count += 1
                else:                   # on a change
                    if c_count > (212 - add_count):
                        print('Do some buffering')
                        pack_left = (212 - add_count)
                        c_count = (c_count - pack_left)

                        if pack_left > 30:           # strip 30 off and continue
                            city_packed.append("0FCh")
                            city_packed.append(" 1Eh")
                            city_packed.append(last)
                            pack_left = (pack_left - 30)
                            space_to_fill -= 30
                            space_left -= 3
                            diag(DATADIR, xcount, space_to_fill, space_left, add_count, last)
                            print(">30: Space Left = ", space_left)
                            print("Space to fill with packing: ", space_to_fill)

                        if pack_left > 3:
                            city_packed.append("0FCh")
                            city_packed.append(str(dec2hex_all(pack_left)))
                            space_to_fill -= c_count
                            space_left -= 3
                        elif pack_left == 3:
                            city_packed.append(last)
                            city_packed.append(last)
                            space_left -= 3
                        elif pack_left == 2:
                            city_packed.append(last)
                            space_left -= 2
                        elif pack_left == 1:
                            space_left -= 1

                        city_packed.append(last)
                        diag(DATADIR, xcount, space_to_fill, space_left, add_count, last)
                        last = city_out[inx]

                        #Write remainder (if any, unpacked)
                        for _ in range(1, (c_count+1)):
                            city_packed.append(last)
                            no_packing = 1

                        with open(DATADIR+'diagnost.txt', 'a') as outfile:
                            outfile.write('\n')
                            outfile.write(f'remainder: {c_count}')
                            outfile.write('packing off')

                    else:       # process normally (c_count less than space_to_fill)
                        # if remaining packed space filled exactly, set no_packing for next time
                        if c_count == (212 - add_count):
                            no_packing = 1
                            with open('diagnost.txt', 'a') as outfile:
                                outfile.write('\n')
                                outfile.write("---packed exactly---")
                        elif c_count > 30:                     # strip 30 off and continue
                            city_packed.append("0FCh")
                            city_packed.append(" 1Eh")
                            city_packed.append(last)
                            c_count = (c_count - 30)
                            space_to_fill -= 30
                            space_left -= 3
                            add_count += 27
                            diag(DATADIR, xcount, space_to_fill, space_left, add_count, last)
                            print("*NP >30: Space Left = ", space_left)
                            print("Space to fill with packing: ", space_to_fill)
                        elif c_count > 3:
                            city_packed.append("0FCh")
                            city_packed.append(str(dec2hex_all(c_count)))
                            city_packed.append(last)
                            space_to_fill -= c_count
                            space_left -= 3
                            add_count += (c_count - 3)
                            diag(DATADIR, xcount, space_to_fill, space_left, add_count, last)
                            c_count = 1
                            last = city_out[inx]
                            print("*NP >15: Space Left = ", space_left)
                            print("Space to fill with packing: ", space_to_fill)
                        else:
                            if c_count == 3:
                                city_packed.append(last)
                                city_packed.append(last)
                                space_left -= 3
                            elif c_count == 2:
                                city_packed.append(last)
                                space_left -= 2
                            elif c_count == 1:
                                space_left -= 1

                            city_packed.append(last)
                            diag(DATADIR, xcount, space_to_fill, space_left, add_count, last)
                            c_count = 1
                            last = city_out[inx]

            else:  # no_packing = 1, no more packing...
                city_packed.append(city_out[inx])


def write_guild_coords(city_out):
    """Write guild goords to file"""

    with open(DATADIR+'constants_guild.asm', 'w') as gfile:
        gfile.write('GUILD_COORDSEQU ')

        guild_count = 0
        guild_north = '1D'  #29
        guild_east = '00'

        for inx in range(900):
            if city_out[inx] == "   9":
                if guild_count == 1:
                    print("Warning: > 1 Guild, 1st will be start location")
                else:
                    guild_count += 1

                    guild_north = coords_in_hex(29- (inx//30))
                    guild_east = coords_in_hex(inx % 30)
                    gfile.write(f'{guild_north}')
                    gfile.write(f'{guild_east}h')


def write_out(num, city_packed):
    """Write packed city data"""

    first3 = 1
    eight_count = 0
    hex_count = 0
    print(num)

    with open(DATADIR + 'F7E7-FA98_city_map.asm', 'w') as myfile:
        myfile.write('\n')
        myfile.write('CITY_MAP_DATA:  db ')

        for out in range(690):
            print(f"index: {out}")
            if eight_count == 33:
                myfile.write(f'; {dec2hex_all(hex_count)}')
                hex_count += 32
                eight_count = 1

            if eight_count == 1:
                myfile.write('\n')
                myfile.write('                db ')
                myfile.write(str(city_packed[out]))
                eight_count += 1
            else:
                if eight_count > 0:
                    if first3 == 1 and eight_count == 4:     # deal with 1st 3 values
                        first3 = 0
                        myfile.write('\n')
                        myfile.write('                db ')
                        eight_count = 1
                    else:
                        myfile.write(',')

                myfile.write(str(city_packed[out]))

                if eight_count == 0:
                    eight_count += 2
                else:
                    eight_count += 1


def draw_boxes(scr):
    """Draw decorative boxes"""

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
        pg.draw.rect(scr, box[0], box[1])


def main():
    """ Main Program """

    prepare_files()

    pg.init()

    screen = pg.display.set_mode((1200, 960))
    pg.display.set_caption("City Editor")

    display_surface = pg.display.set_mode((X, Y))
    display_surface.fill(BLACK)

    font = pg.font.Font('freesansbold.ttf', 16)
    text = font.render('     Blank     ', True, RED, BLACK)
    text_x = font.render('E: 0', True, RED, BLACK)
    text_y = font.render('N: 29', True, RED, BLACK)

    # text boxes init
    draw_boxes(screen)

    #Set initial text
    config_text = font.render("  City Editor", True, RED, BLACK)
    screen.blit(config_text, (1020, 256))

    city_display = create_grid(900)
    city_out = create_grid(900)

    sheet = pg.image.load(CURRDIR + '/CitySpriteSheet32.png')
    city = strip_from_sheet(sheet, (0, 0), (32, 32), 3, 6)

    sheet_big = pg.image.load(CURRDIR + '/CitySpriteSheet128.png')
    city_big = strip_from_sheet(sheet_big, (0, 0), (128, 128), 3, 6)


    select_x = 1015
    select_y = 5
    xpos = 0
    ypos = 0
    pointer = 0
    last_pointer = 0
    last_selected = 0
    selected_block = 0
    out_value = 0

    x_disp = 0
    y_disp = 0
    point_disp = 0


    statues = Statues(DATADIR+'E856-E87D_guardians.asm')
    irongates = IronGates(DATADIR+'constants_gates.asm')
    taverns = Taverns(DATADIR+'E8DE-E8F5_inns_data.asm')

    #Draw initial blank grid

    for coord1 in range(30):
        for coord2 in range(30):
            screen.blit(city[0], ((coord1*32), (coord2*32)))
    pg.display.update()

    #Loop until the user clicks the close button.
    done = False

    # -------- Main Program Loop -----------
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                break

            screen.blit(city_big[selected_block], (select_x, select_y))
            #display_surface.blit(text, textRect)
            blank_box(screen, 1)
            screen.blit(text, (1020, 156))
            screen.blit(city[selected_block], (xpos, ypos))
            screen.blit(text_x, (1060, 200))
            screen.blit(text_y, (1060, 220))

            pg.display.update()

            if event.type == pg.KEYDOWN:
                pg.draw.rect(screen, BLACK, (1000, 200, 20, 20))

                if event.key == pg.K_LEFT and selected_block > 0:
                    selected_block -= 1
                elif event.key == pg.K_RIGHT and selected_block < 17:
                    selected_block += 1
                elif event.key == pg.K_UP and selected_block < 17:
                    selected_block += 1
                elif event.key == pg.K_DOWN and selected_block > 0:
                    selected_block -= 1
                elif event.key == pg.K_a and xpos > 0:
                    x_disp = -32
                    y_disp = 0
                    point_disp = -1
                elif event.key == pg.K_d and xpos < 928:
                    x_disp = 32
                    y_disp = 0
                    point_disp = 1
                elif event.key == pg.K_w and ypos > 29:
                    x_disp = 0
                    y_disp = -32
                    point_disp = -30
                elif event.key == pg.K_s and ypos < 928:
                    x_disp = 0
                    y_disp = 32
                    point_disp = 30
                else:
                    x_disp = 0
                    y_disp = 0
                    point_disp = 0

                last_pointer = city_display[pointer]

                last_selected = int(last_pointer)
                screen.blit(city[last_selected], ((xpos, ypos)))

                xpos += x_disp
                ypos += y_disp
                pointer += point_disp

                curr_east = get_east(pointer)
                curr_north = get_north(pointer)

                if (curr_east == 9) or (curr_north == 9):
                    blank_box(screen, 4)

                text_x = font.render(f'E: {curr_east}', True, RED, BLACK)
                text_y = font.render(f'N: {curr_north}', True, RED, BLACK)

                if event.key == pg.K_p:
                    city_display[pointer] = selected_block
                    city_out[pointer] = out_value
                elif event.key == pg.K_x:
                    print(f'city_out 0:{city_out[0]}')
                    city_packed = []
                    # end 64152
                    # start 63466
                    # available memory space = 686
                    mem_number = len(city_packed)
                    pack_2(city_out, city_packed)
                    print(f"Number of items in the list = {len(city_packed)}")
                    if mem_number < 687: # will pack ok
                        write_out(mem_number, city_packed)

                        taverns.write()
                        statues.write()
                        irongates.write()

                        write_guild_coords(city_out)
                    else:
                        print("City Map will not pack!")
                elif event.key == pg.K_c:
                    # configurable properties
                    if city_out[pointer] == " 11h":
                        print('Tavern config')
                        taverns.configure(pointer)
                    elif city_out[pointer] == " 60h":
                        print('Statue config')
                        statues.configure(pointer,
                                          {"pg": pg,
                                           "screen": screen,
                                           "font": font,
                                           "blank_box": blank_box
                                          }
                                         )
                    elif city_out[pointer] == " 68h":
                        print('Iron Gate config')
                        irongates.configure(pointer)

                hotkeys = {
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

                selected_block = hotkeys.get(event.key, selected_block)

            if selected_block in BLOCKS:
                text = font.render(BLOCKS[selected_block][0], True, RED, BLACK)
                out_value = BLOCKS[selected_block][1]
                #outValRect = font.render(BLOCKS[selected_block][2], True, RED, BLACK)

        # Go ahead and update the screen with what we've drawn.
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
