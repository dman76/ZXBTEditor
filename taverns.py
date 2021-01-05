""" Taverns for BT editor """


from support_functions import BLACK, RED
from support_functions import dec2hex_all, get_east, get_north


class Taverns:
    """ Class for implementing taverns """

    def __init__(self, filename):
        """ Constructor """

        self.filename = filename
        self.taverns = {
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


    def write(self):
        """ Write taverns file """

        with open(self.filename, 'a') as outfile:
            for tavern in self.taverns.values():
                outfile.write('db  ')
                outfile.write(f'{tavern[2]}, ')
                outfile.write(f'{tavern[3]}, ')
                outfile.write(f'{tavern[1]}')
                outfile.write(f'      ; {tavern[0]} Coords + Identifier')
                outfile.write('\n')

            outfile.write('\n')
            outfile.write('default_inn:')
            outfile.write('\n')
            outfile.write('db 0FFh,0FFh,0')


    def configure(self, inx, pglink):
        """ Create taverns """

        pg = pglink['pg']
        screen = pglink['screen']
        font = pglink['font']
        blank_box = pglink['blank_box']

        print(inx)
        inn_value = 0
        text = font.render(self.taverns[inn_value][0], True, RED, BLACK)
        blank_box(2)
        conf_text = font.render("Configure Tavern", True, RED, BLACK)
        screen.blit(conf_text, (1020, 256))

        t0_text = font.render("Current Coords:", True, RED, BLACK)
        screen.blit(t0_text, (1010, 305))

        for tavern_inx, tavern in self.taverns.items():
            t_text = font.render(f'{tavern[0]}', True, RED, BLACK)
            screen.blit(t_text, (1002, (300+(tavern_inx*50))))

            if (tavern[2] == '00' and tavern[3] == '00'):
                coords_txt = "Unassigned"
            else:
                coords_txt = f"N: {tavern[4]}   E: {tavern[5]}"

            t_coords = font.render(coords_txt, True, RED, BLACK)
            screen.blit(t_coords, (1010, (320+(tavern_inx*50))))

        done_inn = False

        while not done_inn:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        if inn_value == 0:
                            inn_value = 7
                        else:
                            inn_value -= 1
                    elif event.key == pg.K_x:
                        if inn_value == 7:
                            inn_value = 0
                        else:
                            inn_value += 1
                    elif event.key == pg.K_c:   # confirm
                        #update north coordinate
                        if inn_value != 0:      # Don't update coords for default tavern!
                            self.taverns[inn_value] = [
                                self.taverns[inn_value][0],
                                self.taverns[inn_value][1],
                                dec2hex_all(get_north(inx)),
                                dec2hex_all(get_east(inx)),
                                get_north(inx),
                                get_east(inx),
                            ]
                            print(self.taverns[inn_value][0])
                            print(self.taverns[inn_value][2])
                            print(self.taverns[inn_value][3])

                        done_inn = True

            blank_box(1)
            text = font.render(self.taverns[inn_value][0], True, RED, BLACK)
            screen.blit(text, (1020, 157))
            pg.display.update()

        blank_box(2)
        blank_box(3)
        conf_text = font.render("  City Editor", True, RED, BLACK)
        screen.blit(conf_text, (1020, 256))
        t0_text = font.render("Tavern Updated", True, RED, BLACK)
        screen.blit(t0_text, (1010, 305))
        pg.display.update()
