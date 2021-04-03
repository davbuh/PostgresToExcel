import os
import re
from PostgressParse import Table, Field
import pandas as pd
import openpyxl


def field_to_frame(tbl, field):
    keys = ['TableName', 'TableDescription', 'FieldName', 'FieldDescription', 'FieldFormat', 'FieldID']
    values = [[item] for item in [tbl.name, tbl.desc, field.name, field.description, field.format, field.id]]
    return pd.DataFrame(dict(zip(keys, values)))


def file_to_df(file):
    print(file.path)
    input_stream = open(file.path, "r")
    lines = input_stream.read().splitlines()
    #assuming each file  represents a phisical table
    curr_tbl = Table()
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

            if struct:  # if new object
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

    #create a dataframe containing a row for each field in the table,
    return pd.concat([field_to_frame(curr_tbl, field) for field in curr_tbl.fields])


def main():
    directory = r"C:\Users\buhbut\SVN\Hubble Project\Business Team\1 - Base data\3 - Supplies\Job based pricing\Schema scripts"

    #list of all files n the directory
    dir = os.scandir(directory)

    #list of dataframes. each df is list of fields from a single table
    frames = [file_to_df(file) for file in dir]

    #union all df together
    df = pd.concat(frames, ignore_index=True)

    #drop unified df to excel for further analysis
    df.to_csv(r"pricing.csv", index=False)


if __name__ == "__main__":
    main()
