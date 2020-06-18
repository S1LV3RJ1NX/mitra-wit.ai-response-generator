import config as cfg
import os
import pandas as pd
from collections import defaultdict

def read_excel_generate_mapping(fname, to_map=True,key=""):
	pre = os.path.dirname(os.path.realpath(__file__))
	path = os.path.join(pre, fname)

	mappings = defaultdict(list)
	df = pd.read_excel(path)
	if to_map:
		df.City = df.City.str.lower()	
		for index, row in df.iterrows():
			mappings[row.City].append(row)
	else:
		for index, row in df.iterrows():
			mappings[key].append(row)
	return mappings



if __name__ == '__main__':	
	ngo = read_excel_generate_mapping(cfg.excel_path["ngo"])
	food = read_excel_generate_mapping(cfg.excel_path["food"])
	hospital = read_excel_generate_mapping(cfg.excel_path["hospital"])
	yoga = read_excel_generate_mapping(cfg.excel_path["yoga"], to_map=False, key="yoga")
	music = read_excel_generate_mapping(cfg.excel_path["music"], to_map=False, key="music")
	emergency = read_excel_generate_mapping(cfg.excel_path["emergency"], to_map=False, key="emergency")


	# print(ngo.keys())
	# print(ngo["sangli"][0][3])
	# print("========================================")
	# print(ngo["sangli"][1])

	# print(food.keys())
	# print(food["sangli"][0][2])
	# print("========================================")
	# print(food["kolhapur"][1])

	# print(food.keys())
	# print(hospital["sangli"][0][2])
	# print("========================================")
	# print(hospital["kolhapur"][1])

	# print(yoga.keys())
	# print(yoga["yoga"][0])
	# print("========================================")
	# print(music.keys())
	# print(music["music"][0])
	# print("========================================")
	# print(emergency.keys())
	# print(emergency["emergency"][0])
