import json
import pprint

file_path = 'system-podlewania-ogrodu/plany_export.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

pprint.pprint(data)
