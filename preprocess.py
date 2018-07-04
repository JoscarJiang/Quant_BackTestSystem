import pandas as pd
import numpy as np
import datetime
import sys
import os

def fetch_data(exchange, future_kind):
	"""
	@usage: to get all dates the kind of future can be trade
	"""
	data = None
	filename = os.getcwd()
	filename = os.path.join(filename, 'dataset')
	filename = os.path.join(filename, exchange)
	filename = os.path.join(filename, future_kind) ## future+88 -> main continuity
	try:
		data = pd.read_csv(filename)
	except IOError:
		print("Error: File read Fail")
	else:
		return data



def compute_date(start, end=None, is_end_include=False):
	try:
		date_start = datetime.datetime.strptime(start, "%Y-%m-%d")
		if end is not None:
			date_end = datetime.datetime.strptime(end, "%Y-%m-%d")
			date_temp = date_start
			date_list = []
			while date_temp < date_end:
				date_temp += datetime.timedelta(days=1)
				date_list.append(date_temp.strftime('%Y-%m-%d'))
			if is_end_include:
				date_list.append(date_end)
	except NameError:
		print(">>> Error: Input is Wrong!")
	else:
		return date_list


	



def weighted_avg(data, name, feature, if_include_now=True):
	data[name] = pd.rolling_apply(data[[feature]], window=window_size, func=weighted_avg)

	if if_include_now:
		data[name] = pd.rolling_apply(data[[feature]], window=window_size, func=weighted_avg)
	else:
		data[name] = pd.rolling_apply(data[[feature]], window=window_size, func=weighted_avg).shift(1)
	"""
	res = pd.ewma(data[['r']], min_periods=window_size, span=9)
	"""
	return data

def w_a(dt):
	dt = np.average(dt,weights=range(1,len(dt)+1,1)) # can be optimized
	return dt
