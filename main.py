import os
import re
from PostgressParse import Table, Field
import pandas as pd
import openpyxl

#import pandas as pd
def file_to_df(file):


def main():
    directory = r"C:\Users\buhbut\SVN\Hubble Project\Business Team\1 - Base data\3 - Supplies\Job based pricing\Schema scripts"
    dir = os.scandir(directory)
    tables = []
    frames = [file_to_df(file) for file in dir]
    for file in dir:
        print(file.path)
        input_stream = open(file.path, "r")
        lines = input_stream.read().splitlines()
        curr_tbl = Table()
        tables.append(curr_tbl)
        curr_field = None
        context = ""
        for line in lines:
            if line.strip() == "":
                if context == "field":
                    curr_tbl.add_field(curr_field)
                context = ""
            else:
                struct = re.search(r'(ADD )(?P<type>TABLE|FIELD) "(?<= ")(?P<value>\w+)(?=")', line)
                attr = re.search(r'(?P<name>DESCRIPTION|FORMAT) "(?<= ")(?P<value>[-\w ]+)(?=")', line)

                if struct: #if new object
                    if struct.group("type") == "TABLE":
                        context = "table"
                        tbl_name = struct.group("value")
                        curr_tbl.set_name(tbl_name)
                    elif struct.group("type") == "FIELD":
                        context = "field"
                        field_name = struct.group("value")
                        curr_field = Field(field_name)

                elif attr:
                    val = attr.group("value")
                    if attr.group("name") == "DESCRIPTION":
                        if context == "field":
                            curr_field.set_description(val)
                        elif context == "table":
                            curr_tbl.set_description(val)
                    elif attr.group("name") == "FORMAT" and context == "field":
                        curr_field.set_format(val)

        input_stream.close()
    list2d = []

    for table in tables:
        for field in table.fields:
            list2d.append([table.name, table.desc, field.name, field.description, field.format, field.id])
    data = pd.DataFrame(list2d, columns=['TableName', 'TableDescription', 'FieldName', 'FieldDescription', 'FieldFormat', 'FieldID'])
    data.to_excel(r"pricing.xlsx", sheet_name="QAD Schema", )

if __name__ == "__main__":
    main()


