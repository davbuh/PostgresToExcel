
class Table:
    def __init__(self):
        self.name = ""
        self.desc = ""
        self.fields = []

    def set_name(self, name):
        self.name = name

    def set_description(self, desc):
        self.desc = desc

    def add_field(self, field):
        self.fields.append(field)

class Field:
    id = 0

    def __init__(self, name = None):
        if name is None:
            self.name = ""
        else:
            self.name = name
        self.description = ""
        self.format = ""
        self.id = Field.id
        Field.id += 1

    def set_description(self, desc):
        self.description = desc

    def set_format(self, format):
        self.format = format