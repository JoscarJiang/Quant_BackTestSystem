class OrderState:
	def __init__(self):
		self.BUY = -1
		self.SELL = 1
		self.OPEN = -1
		self.CLOSE = 1
		self.REQUIRED = 1
		self.STOP_LOSS = 2
		self.CHANGE_MAIN = 3
		self.EXPIRED = 4
		self.END_OF_DAY = 5 # specific to intraday
		self.FULL_CLOSE = 100
		self.PART_CLOSE = 101