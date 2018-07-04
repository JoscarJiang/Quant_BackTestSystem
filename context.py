from math import floor
import json
from orderstate import OrderState
from futureaccount import FutureAccount
from tradestate import TradeState
from position import Position


ORDER = OrderState()
trade_succeed_rate = 0.25

class Context:
	"""
	The Class preload and take contral of all informations
	It contains FutureAccount to update Account Information 
	It contains TradeState to contral the trade state.
	It contains 
	"""
	def __init__(self, init_money):

		self.future_info = load_info()  
		self.future_account = FutureAccount(init_money, future_info)
		self.trade_state = TradeState()

	def subscribe_futures(self, futures=None):
		if futures is None:
			raise Exception("Error:func <subscribe_futures> has Invalid Input")
		future_dic = {}

		if type(futures) == list: 
			for f in futures:
				future_dic[f] = Position()
			self.future_account.positions = future_dic
		else:
			future_dic[futures] = Position()
			self.future_account.positions = future_dic

	def load_info():
		"""
		@func: load the multipliers, transaction_cost_rate,transaction_cost_amount,margin,close_today_discount,tick_size
		@return: dict with future_kind as key, the others as value
		"""
		filename = os.getpwd()
		filename = os.path.join(filename,'dataset','info')
		filename = os.path.join(filename,'future_info.json')
		try:
    		with open(filename, 'r') as f:
        		info = json.load(fp=f)

		except FileNotFoundError:
    		print "File is not found."
    	else:
    		return info


def buy_open(context, future, bar, num, reason=None):
	
	# check the num
	trade_num = floor(bar['volume'] * trade_succeed_rate)
	if trade_num >= num:
		trade_num = num

	new_order = Order()

	# update the order object
	new_order.trade_fcode = future
	new_order.trade_num = trade_num
	new_order.trade_price = bar['ask_price']
	new_order.trade_direction = ORDER.BUY
	new_order.trade_position = ORDER.OPEN
	new_order.trade_date = bar['date']
	new_order.trade_time = bar['time']
	new_order.trade_reason = reason

	# update the future account
	Context.future_account.buy_open_update(new_order)
	

def sell_open(context, future, bar, num, reason=None):
	# check the num
	trade_num = floor(bar['volume'] * trade_succeed_rate)
	if trade_num >= num:
		trade_num = num

	new_order = Order()

	# update the order object
	new_order.trade_fcode = future
	new_order.trade_num = trade_num
	new_order.trade_price = bar['bid_price']
	new_order.trade_direction = ORDER.SELL
	new_order.trade_position = ORDER.OPEN
	new_order.trade_date = bar['date']
	new_order.trade_time = bar['time']
	new_order.trade_reason = reason

	# update the future account
	Context.future_account.sell_open_update(new_order)



def buy_close(context, future, bar, num, reason=None):
	# check the num
	trade_num = floor(bar['volume'] * trade_succeed_rate)
	if trade_num >= num:
		trade_num = num

	new_order = Order()

	# update the order object
	new_order.trade_fcode = future
	new_order.trade_num = trade_num
	new_order.trade_price = bar['ask_price']
	new_order.trade_direction = ORDER.BUY
	new_order.trade_position = ORDER.CLOSE
	new_order.trade_date = bar['date']
	new_order.trade_time = bar['time']
	new_order.trade_reason = reason

	# update the future account
	Context.future_account.buy_close_update(new_order)

def sell_close(context, future, bar, num, reason=None):
	# check the num
	trade_num = floor(bar['volume'] * trade_succeed_rate)
	if trade_num >= num:
		trade_num = num

	new_order = Order()

	# update the order object
	new_order.trade_fcode = future
	new_order.trade_num = trade_num
	new_order.trade_price = bar['bid_price']
	new_order.trade_direction = ORDER.SELL
	new_order.trade_position = ORDER.CLOSE
	new_order.trade_date = bar['date']
	new_order.trade_time = bar['time']
	new_order.trade_reason = reason

	# update the future account
	Context.future_account.sell_close_update(new_order)



