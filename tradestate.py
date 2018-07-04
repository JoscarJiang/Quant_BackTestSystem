class TradeState:
	def __init__(self):
		self.fcode = None
		self.stop_sell = False
		self.stop_buy = False
		self.sell_count = 0
		self.buy_count = 0
		self.trade_info = []