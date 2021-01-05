""" Iron gates for BT editor """


from support_functions import BLACK, RED, DIRECTIONS, DIRECTIONS_PARAM
from support_functions import dec2hex_all, get_east, get_north


class IronGates:
    """ Class for implementing iron gates """

    def __init__(self, filename):
        """ Constructor """

        self.filename = filename
        self.irongates = {
            #Name, N coord hex, E coord hex, N coord dec, E Coord dec, Direction, Direction display
            0:  ["Iron Gate 0", "00", "00", "00", "00", "0", "U"],
            1:  ["Iron Gate 1", "00", "00", "00", "00", "0", "U"],
            2:  ["Iron Gate 2", "00", "00", "00", "00", "0", "U"],
            3:  ["Iron Gate 3", "00", "00", "00", "00", "0", "U"],
            4:  ["Iron Gate 4", "00", "00", "00", "00", "0", "U"]
        }


    def write(self):
        """ Write gates file """

        with open(self.filename, 'a') as outfile:
            for gate in self.irongates.values():
                outfile.write('          db  ')
                outfile.write(f'{gate[1]}, ')
                outfile.write(f'{gate[2]}, ')
                outfile.write(f'{gate[5]}')
                outfile.write(f'      ; {gate[0]} Coords + Direction')
                outfile.write('\n')


    def configure(self, inx, pglink):
        """ Create gates """

        pg = pglink['pg']
        screen = pglink['screen']
        font = pglink['font']
        blank_box = pglink['blank_box']

        print(inx)
        gate_value = 1
        direction = 0
        blank_box(2)
        blank_box(4)
        conf_text = font.render(f"Configure: {self.irongates[gate_value][0]}", True, RED, BLACK)
        screen.blit(conf_text, (1002, 256))

        t0_text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0_text, (1010, 305))

        for gate_inx, gate in self.irongates.items():
            g_text = font.render(f'Iron Gate: {gate_inx}', True, RED, BLACK)
            screen.blit(g_text, (1002, (340+(gate_inx*60))))

            if (gate[3] == '00' and gate[4] == '00'):
                coords_txt = "Unassigned"
            else:
                coords_txt = f"N: {gate[3]}  E: {gate[4]}  Faces: {gate[6]}"

            t_coords = font.render(coords_txt, RED, BLACK)

            screen.blit(t_coords, (1010, (360+(gate_inx*60))))

        done_gate = False

        while not done_gate:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        if gate_value == 1:
                            gate_value = 4
                            blank_box(2)
                        else:
                            gate_value -= 1
                    elif event.key == pg.K_x:
                        if gate_value == 4:
                            gate_value = 1
                            blank_box(2)
                        else:
                            gate_value += 1
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
                        self.irongates[gate_value] = [
                            self.irongates[gate_value][0],
                            dec2hex_all(get_north(inx)),
                            dec2hex_all(get_east(inx)),
                            get_north(inx),
                            get_east(inx),
                            DIRECTIONS_PARAM[direction],
                            DIRECTIONS[direction]
                        ]

                        for gate_inx in range(7):
                            print(self.irongates[gate_value][gate_inx])

                        done_gate = True
                        break

            blank_box(1)
            ##            text = font.render(str(MONSTERS[monsterValue][0]), True, RED, BLACK)
            ##            screen.blit(text, (1020, 157))
            conf_text = font.render(f"Configure: {self.irongates[gate_value][0]}", True, RED, BLACK)
            screen.blit(conf_text, (1002, 256))
            face = str(DIRECTIONS[direction])
            direction_text = font.render(face, True, RED, BLACK)
            screen.blit(direction_text, (1065, 210))
            pg.display.update()

        blank_box(2)
        blank_box(3)
        blank_box(4)
        conf_text = font.render("  City Editor", True, RED, BLACK)
        screen.blit(conf_text, (1020, 256))
        t0_text = font.render("Gate Updated", True, RED, BLACK)
        screen.blit(t0_text, (1010, 305))
        pg.display.update()
