import json

def write_data(name_data, data):
	with open(name_data, "w", encoding="utf-8") as f:
   		json.dump(data, f, ensure_ascii=False, indent=4)

def read_data(name_data):
	with open(name_data, "r", encoding="utf-8") as f:
		return json.load(f)
