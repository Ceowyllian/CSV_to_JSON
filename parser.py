import csv
import json
from mapping import Mapping


def create_table(path: str, schema: dict):
    mapping = Mapping(schema)
    with open(path, 'w') as csvfile:
        header = mapping.table_fields
        writer = csv.DictWriter(csvfile, header, delimiter=';')
        writer.writeheader()


def csv_to_json(csvpath: str, jsonpath: str, schema: dict):
    mapping = Mapping(schema)
    with open(csvpath, 'r') as csvfile:
        with open(jsonpath, 'w') as jsonfile:
            header = mapping.table_fields
            csvreader = csv.DictReader(csvfile, header, delimiter=';')
            strbuffer = '['
            for row in csvreader:
                if row[header[0]] != header[0]:
                    if len(strbuffer) != 1:
                        strbuffer += ',\n'
                    struct = mapping.row_to_dict(row)
                    strbuffer += (json.dumps(struct,
                                             ensure_ascii=False,
                                             indent=4))
            strbuffer += ']'
            jsonfile.write(strbuffer)
