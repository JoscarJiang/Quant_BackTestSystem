class Position:
	def __init__(self, fcode, sell_quantity, buy_quantity, sell_open_price, buy_open_price):
		self.fcode = fcode
		self.total_sell_quantity = sell_quantity
		self.total_buy_quantity = buy_quantity
		self.today_sell_quantity = sell_quantity
		self.today_buy_quantity = buy_quantity
		self.yesterday_sell_quantity = 0
		self.yesterday_buy_quantity = 0
		self.sell_open_price = sell_open_price
		self.buy_open_price = buy_open_price
	
	def today_buy_open_update(buy_quantity, buy_price):
		self.buy_open_price = (self.buy_open_price * self.total_buy_quantity + buy_price * buy_quantity)/(self.total_buy_quantity + buy_quantity)
		self.total_buy_quantity += buy_quantity
		self.today_buy_quantity += buy_quantity

	def today_sell_open_update(sell_quantity, sell_price):
		self.sell_open_price = (self.sell_open_price * self.total_sell_quantity + sell_price * sell_quantity)/(self.total_sell_quantity + sell_quantity)
		self.total_sell_quantity += sell_quantity
		self.today_sell_quantity += sell_quantity


	def buy_close_update(buy_close_quantity):
		today_pos = 0
		yesterday_pos = 0
		# today_positions should be closed first
		if buy_close_quantity > self.total_sell_quantity:
			raise Exception("Error: func <buy_close_update> Mo Much Quantity to Buy Close")
		if buy_close_quantity > self.today_sell_quantity:
			buy_close_quantity -= self.today_sell_quantity
			today_pos = self.today_sell_quantity
			self.total_sell_quantity -= self.today_sell_quantity
			self.today_sell_quantity = 0 
		else:
			self.today_sell_quantity -= buy_close_quantity
			self.total_sell_quantity -= buy_close_quantity
			today_pos = buy_close_quantity
			buy_close_quantity = 0

		if buy_close_quantity > 0:
			self.yesterday_sell_quantity -= buy_close_quantity
			self.total_sell_quantity -= buy_close_quantity
			yesterday_pos = buy_close_quantity
			buy_close_quantity = 0


		return today_pos,yesterday_pos


	def sell_close_update(sell_close_quantity):
		today_pos = 0
		yesterday_pos = 0
		# today_positions should be closed first
		if sell_close_quantity > self.total_buy_quantity:
			raise Exception("Error: func <sell_close_update> Mo Much Quantity to Sell Close")
		if sell_close_quantity > self.today_buy_quantity:
			sell_close_quantity -= self.today_buy_quantity
			self.total_buy_quantity -= self.today_buy_quantity
			today_pos = self.today_buy_quantity
			self.today_buy_quantity = 0 
		else:
			self.today_buy_quantity -= sell_close_quantity
			self.total_buy_quantity -= sell_close_quantity
			today_pos = sell_close_quantity
			sell_close_quantity = 0

		if sell_close_quantity > 0:
			self.yesterday_buy_quantity -= sell_close_quantity
			self.total_buy_quantity -= sell_close_quantity
			yesterday_pos = sell_close_quantity
			sell_close_quantity = 0

		return today_pos,yesterday_pos


	def quantity_update():
		"""
		@func: used after trading is closed to update the quantity
		"""
		self.yesterday_buy_quantity = self.yesterday_buy_quantity + self.today_buy_quantity
		self.yesterday_sell_quantity = self.yesterday_sell_quantity + self.today_sell_quantity

		if self.yesterday_sell_quantity != self.total_sell_quantity:
			raise Exception("Error: func <quantity_update> Wrong Sell Quantity")

		if self.yesterday_buy_quantity != self.total_buy_quantity:
			raise Exception("Error: func <quantity_update> Wrong Buy Quantity")
