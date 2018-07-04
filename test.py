import pandas as pd
import numpy as np
import json
import os

def load_info():
	filename = os.getcwd()
	filename = os.path.join(filename,'dataset','info')
	filename = os.path.join(filename,'future_info.json')
	try:
		with open(filename, 'r') as f:
			info = json.load(fp=f)
			print(type(info['cu']['multiplier']))

	except FileNotFoundError:
		print("File is not found.")
	else:
		return info


load_info()