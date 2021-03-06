from enum import Enum
from core.inputfile import Section


class CurveType(Enum):
    """Curve Type"""
    STORAGE = 1
    SHAPE = 2
    DIVERSION = 3
    TIDAL = 4
    PUMP1 = 5
    PUMP2 = 6
    PUMP3 = 7
    PUMP4 = 8
    RATING = 9
    CONTROL = 10


class Curve(Section):
    """Defines data curves and their X,Y points"""

    field_format = " {:16}\t{:10}\t{:10}\t{:10}\n"

    def __init__(self, new_text=None):
        Section.__init__(self)

        self.curve_id = ''      # string
        """Curve ID Label"""

        self.curve_type = CurveType.PUMP1
        """Curve type"""

        self.curve_xy = []      # list of (x, y) tuples
        """X, Y Values"""

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        """format contents of this item for writing to file"""
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        type_name = self.curve_type.name
        for xy in self.curve_xy:
            inp += Curve.field_format.format(self.curve_id, type_name, xy[0], xy[1])
            type_name = "          "
        return inp

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            self.set_comment_check_section(line)
            if line.strip():
                fields = line.split()
                if len(fields) > 2:
                    self.curve_id = fields[0]
                    try:
                        self.curve_type = CurveType[fields[1].upper()]
                        x_index = 2
                    except:
                        x_index = 1
                    for x in range(x_index, len(fields) - 1, 2):
                        self.curve_xy.append((fields[x], fields[x + 1]))
