import get_data as gd
import json

list_of_dicts = gd.get_data_list_of_dicts();

with open("data.json","w") as filename:
	json.dump(list_of_dicts, filename, indent=2)
