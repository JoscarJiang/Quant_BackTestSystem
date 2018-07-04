class FutureAccount:
	def __init__(self, init_money, future_info):
		
		self.positions = {}

		self.available = init_money
		self.transaction_cost = 0
		self.total_value = init_money
		
		self.total_pnl = 0
		self.daily_pnl = 0
		self.realized_pnl = 0

		self.future_info = future_info
		self.order_record = pd.DataFrame(columns = ["fcode", "date", "time", "price", "num", "direction", 'position', 'reason'])
	
	def buy_open_update(new_order):
		"""
		@func: update the buy_open info
		@para: order object containing order infos 
		"""
		fcode = new_order.trade_fcode
		this_info = self.future_info[fcode[:2]]   
		
		self.open_value_update(this_info, new_order)
		self.open_position_update(fcode, new_order)
		#self.open_order_in_trade_update(new_order)
		self.order_record_update(new_order)


	def sell_open_update(new_order):
		"""
		@func: update the buy_open info
		@para: order object containing order infos 
		"""
		fcode = new_order.trade_fcode
		this_info = self.future_info[fcode[:2]]   
		
		self.open_value_update(this_info, new_order)
		self.open_position_update(fcode, new_order)
		self.order_record_update(new_order)

	def buy_close_update(new_order):
		fcode = new_order.trade_fcode
		this_info = self.future_info[fcode[:2]]  
		today_pos, yesterday_pos = self.close_position_update(fcode, new_order)
		self.close_value_update(this_info, new_order, today_pos, yesterday_pos)
		self.order_record_update(new_order)


	def sell_close_update(new_order):
		fcode = new_order.trade_fcode
		this_info = self.future_info[fcode[:2]]  
		today_position, yesterday_position = self.close_position_update(fcode, new_order)
		self.close_value_update(this_info, new_order)
		self.order_record_update(new_order)

	def order_record_update(self, new_order):
		self.order_record.append([new_order.fcode, new_order.trade_date, new_order.trade_time, 
								  new_order.trade_price, new_order.trade_num, 
								  new_order.trade_direction, new_order.trade_position,
								  new_order.trade_reason],ignore_index=True)


	def close_value_update(self, this_info, new_order, today_pos, yesterday_pos):

		if this_info['close_today_discount'] == 0:

		tc = 0
		if this_info['transaction_cost_amount'] == 0 and this_info['transaction_cost_rate'] > 0:
			tc = this_info['transaction_cost_rate'] * new_order.trade_price * this_info['multiplier']
		elif this_info['transaction_cost_amount'] > 0 and this_info['transaction_cost_rate'] == 0:
			tc = this_info['transaction_cost_amount']
		tc = new_order.trade_num * tc
		deposit = new_order.trade_num * new_order.trade_price * this_info['multiplier'] * this_info['margin']
	
		self.available -= (tc + deposit)

		if self.available < 0:
			raise Exception(">>> Error: Deposit is insufficient!")

		self.transaction_cost += tc
		self.total_value -= tc

	def open_value_update(self, this_info, new_order):
		"""
		@func: update the available, transaction_cost, total_value
		@warning:
		for transaction_cost_rate: transaction_cost(one hand) = transaction_cost_rate * trade_price * multiplier
		for transaction_cost_amount : transaction_cost(one hand) = transaction_cost_amount
		"""
		tc = 0
		if this_info['transaction_cost_amount'] == 0 and this_info['transaction_cost_rate'] > 0:
			tc = this_info['transaction_cost_rate'] * new_order.trade_price * this_info['multiplier']
		elif this_info['transaction_cost_amount'] > 0 and this_info['transaction_cost_rate'] == 0:
			tc = this_info['transaction_cost_amount']
		tc = new_order.trade_num * tc
		deposit = new_order.trade_num * new_order.trade_price * this_info['multiplier'] * this_info['margin']
	
		self.available -= (tc + deposit)

		if self.available < 0:
			raise Exception(">>> Error: Deposit is insufficient!")

		self.transaction_cost += tc
		self.total_value -= tc


	def close_position_update(self, fcode, new_order):
		if fcode not in self.positions:
			raise Exception(">>> Error: func <close_position_update> No such Position")

		if new_order.trade_direction == ORDER.BUY:
			today_pos,yesterday_pos = self.positions[fcode].buy_close_update(buy_close_quantity=new_order.trade_num)
		elif new_order.trade_direction == ORDER.SELL:
			today_pos,yesterday_pos = self.positions[fcode].sell_close_update(sell_close_quantity=new_order.trade_num)
		return today_pos,yesterday_pos



	def open_position_update(self, fcode, new_order):
		if fcode not in self.positions:
			self.positions[fcode] = Position()
		
		if new_order.trade_direction == ORDER.BUY:
			self.positions[fcode].today_buy_open_update(buy_quantity=new_order.trade_num, buy_price=new_order.trade_price)
		elif  new_order.trade_direction == ORDER.SELL:
			self.positions[fcode].today_sell_open_update(buy_quantity=new_order.trade_num, buy_price=new_order.trade_price)


	def before_trading_update(self):
		self.realized_pnl = 0
		self.transaction_cost = 0
		self.daily_pnl = 0

	def after_trading_update(self):
		daily_pnl_update()
		self.total_pnl += self.daily_pnl 

	def daily_pnl_update(self):
