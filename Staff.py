
class Staff(object):
    def __init__(self, staff_matrix, line_width, line_spacing, staff_img, clef="treble", time_signature="44",):
        self.clef = clef
        self.time_signature = time_signature
        self.line_one = staff_matrix[0]
        self.line_two = staff_matrix[1]
        self.line_three = staff_matrix[2]
        self.line_four = staff_matrix[3]
        self.line_five = staff_matrix[4]
        #self.staff_box = staff_box
        self.img = staff_img
        self.bars = []
        self.line_width = line_width
        self.line_spacing = line_spacing

    def set_clef(self, clef):
        self.clef = clef

    def set_TS(self, time):
        self.time_signature = time

    def add_bar(self, bar):
        self.bars.append(bar)

    def get_clef(self):
        return self.clef

    def get_TS(self):
        return self.time_signature

    def get_image(self):
        return self.img

    def get_line_thickness(self):
        return self.line_width

    def get_line_spacing(self):
        return self.line_spacing

    def get_bars(self):
        return self.bars

    def get_pitch(self, note_center_y):
        clef_info = {
            "treble": [("F5", "E5", "D5", "C5", "B4", "A4", "G4", "F4", "E4"), (5,3), (4,2)],
            "bass": [("A3", "G3", "F3", "E3", "D3", "C3", "B2", "A2", "G2"), (3,5), (2,4)]
        }
        note_names = ["C", "D", "E", "F", "G", "A", "B"]

        MOE = 2

        test = [10,11,12]

        # Check within staff first
        # if (note_center_y == self.line_one or note_center_y == self.line_one + MOE or
        #         note_center_y == self.line_one - MOE):
        if (note_center_y in range(self.line_one - MOE, self.line_one + MOE + 1)):
            return clef_info[self.clef][0][0]
        elif (note_center_y  > self.line_one + MOE and note_center_y < self.line_two - MOE):
            return clef_info[self.clef][0][1]
        elif (note_center_y in range(self.line_two - MOE, self.line_two + MOE + 1)):
            return clef_info[self.clef][0][2]
        elif (note_center_y > self.line_two + MOE and note_center_y < self.line_three - MOE):
            return clef_info[self.clef][0][3]
        elif (note_center_y in range(self.line_three - MOE, self.line_three + MOE + 1)):
            return clef_info[self.clef][0][4]
        elif (note_center_y > self.line_three + MOE and note_center_y < self.line_four-MOE):
            return clef_info[self.clef][0][5]
        elif (note_center_y in range(self.line_four - MOE, self.line_four + MOE + 1)):
            return clef_info[self.clef][0][6]
        elif (note_center_y > self.line_four + MOE and note_center_y < self.line_five-MOE):
            return clef_info[self.clef][0][7]
        elif (note_center_y in range(self.line_five - MOE, self.line_five + MOE + 1)):
            return clef_info[self.clef][0][8]
        else:
            print(f'{note_center_y} not found.')