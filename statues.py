""" Statues for BT editor """


from MonsterList import MONSTERS
from support_functions import BLACK, RED, DIRECTIONS
from support_functions import dec2hex_all, get_east, get_north


class Statues:
    """Class for implementing statues"""

    def __init__(self, filename):
        """ Constructor """

        self.filename = filename
        self.statues = {
            #Name , Type (hex), Type (dec), N (hex), E (hex), N (dec), E (dec), direction
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

    def write(self):
        """ Write statues file """

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

    def configure(self, inx, pglink):
        """ Create statues """

        def get_monster_index(inx, shift):
            if inx + shift < 1:
                result = len(MONSTERS)-1
            elif inx + shift >= len(MONSTERS):
                result = 1
            else:
                result = inx + shift

            return result


        pg = pglink['pg']
        screen = pglink['screen']
        font = pglink['font']
        blank_box = pglink['blank_box']

        print(inx)
        statue_value = 1
        monster_value = 1
        direction = 0
        text = font.render(self.statues[statue_value][0], True, RED, BLACK)
        blank_box(2)
        blank_box(4)
        conf_text = font.render(f"Configure: {self.statues[statue_value][0]}", True, RED, BLACK)
        screen.blit(conf_text, (1010, 256))

        t0_text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0_text, (1010, 305))

        for statue_inx, statue in self.statues.items():
            s_text = font.render(f'Statue: {statue_inx}', True, RED, BLACK)
            screen.blit(s_text, (1002, (280+(statue_inx*60))))

            if statue[2] == '00':
                t_text = font.render("Unassigned", True, RED, BLACK)
            else:
                stat = statue[2]
                t_text = font.render(str(MONSTERS[stat][0]), True, RED, BLACK)

            if (statue[3] == '00' and statue[4] == '00'):
                coords_txt = "Unassigned"
            else:
                coords_txt = f"N: {statue[5]}  E: {statue[6]}  Faces: {statue[8]}"

            t_coords = font.render(coords_txt, True, RED, BLACK)

            screen.blit(t_text, (1002, (300+(statue_inx*60))))
            screen.blit(t_coords, (1010, (320+(statue_inx*60))))

        done_statue = False

        while not done_statue:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_z:
                        if statue_value == 1:
                            statue_value = 10
                            blank_box(2)
                        else:
                            statue_value -= 1
                    elif event.key == pg.K_x:
                        if statue_value == 10:
                            statue_value = 1
                            blank_box(2)
                        else:
                            statue_value += 1
                    elif event.key == pg.K_LEFT:
                        monster_value = get_monster_index(monster_value, -1)
                    elif event.key == pg.K_DOWN:
                        monster_value = get_monster_index(monster_value, -10)
                    elif event.key == pg.K_RIGHT:
                        monster_value = get_monster_index(monster_value, 1)
                    elif event.key == pg.K_UP:
                        monster_value = get_monster_index(monster_value, 10)
                    elif event.key == pg.K_j:   # anticlockwise
                        if direction == 0:
                            direction = 4
                        else:
                            direction -= 1
                    elif event.key == pg.K_l:   # clockwise
                        if direction == 4:
                            direction = 0
                            blank_box(4)
                        else:
                            direction += 1
                    elif event.key == pg.K_c:   # confirm
                        #update north coordinate
                        self.statues[statue_value] = [
                            self.statues[statue_value][0],
                            MONSTERS[monster_value][1],
                            monster_value,
                            dec2hex_all(get_north(inx)),
                            dec2hex_all(get_east(inx)),
                            get_north(inx),
                            get_east(inx),
                            direction,
                            DIRECTIONS[direction]
                        ]

                        for inx in range(7):
                            print(self.statues[statue_value][inx])

                        done_statue = True


            blank_box(1)
            text = font.render(str(MONSTERS[monster_value][0]), True, RED, BLACK)
            screen.blit(text, (1020, 157))
            conf_text = font.render(f"Configure: {self.statues[statue_value][0]}", True, RED, BLACK)
            screen.blit(conf_text, (1010, 256))
            face = str(DIRECTIONS[direction])
            direction_text = font.render(face, True, RED, BLACK)
            screen.blit(direction_text, (1065, 210))
            pg.display.update()

        blank_box(2)
        blank_box(3)
        blank_box(4)
        conf_text = font.render("  City Editor", True, RED, BLACK)
        screen.blit(conf_text, (1020, 256))
        t0_text = font.render("Statue Updated", True, RED, BLACK)
        screen.blit(t0_text, (1010, 305))
        pg.display.update()
