import pandas as pd
import numpy as np
from preprocess import fetch_data, compute_date, weighted_avg
from context import Context

futures_kinds_shanghai = ['AL' ,'RU' ,'WR','RB' ,'AU','CU' ,'AG','PB' ,'ZN' ,'SN','NI' ,'HC' ,'BU'] 
future_kinds_shanghai = ['NI']


def close_all(context, last_main):
    sell_num = context.future_account.positions[last_main].sell_quantity
    buy_num = context.future_account.positions[last_main].buy_quantity
    if (sell_num + buy_num) == 0:
        context.last_main = context.main_futures[future_kinds_shanghai[0]]
    else:
        if sell_num > 0:
            buy_close(context.last_main, sell_num)
        if buy_num > 0:
            sell_close(context.last_main, buy_num)


def handle_bar(context, bar_dict):
    if context.stop_sell_open == True:
        if context.sell_count >= 20:
            context.stop_sell_open = False
            context.sell_count = 0
        else:
            context.sell_count +=1
    
    
    date_time = str(context.now).split(' ')[1]
    [hour,min,sec] = date_time.split(':')
    if hour == '09' and min == '01':
        context.counter = 0
    
    
    
    if context.stop_buy_open == True:
        if context.buy_count >= 20:
            context.stop_buy_open = False
            context.buy_count = 0
        else:
            context.buy_count += 1    

 
    if context.last_main != context.main_futures[future_kinds_shanghai[0]]:
        close_all(context, context.last_main)
    context.counter += 1
    if context.counter < 30:
        return
    
    look_back_num = 30
    data = history_bars(future_kinds_shanghai[0]+'88',30, '1m', fields=['close'], skip_suspended=True)
    data = [i[0] for i in data]
    mean_price = np.average(data,weights=range(1,len(data)+1,1))
    std_price = np.std(data)
    std_price = sum(np.std(data)*range(1,len(data)+1,1))/sum(range(1,len(data)+1,1))
    print(std_price)
    is_closed = False
    sell_num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].sell_quantity
    buy_num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].buy_quantity
    
    sell_pnl = context.avg_sell - bar_dict[context.main_futures[future_kinds_shanghai[0]]].close
    buy_pnl = bar_dict[context.main_futures[future_kinds_shanghai[0]]].close - context.avg_buy
    if sell_num !=0 or buy_num!=0:
        print("sell_pnl:%f,sell_num:%d, buy_pnl:%f, buy_num:%d"%(sell_pnl,sell_num,buy_pnl,buy_num))
    
    if sell_pnl >= 20 and sell_num > 0:
        if sell_num > 10:
            sell_num = 10
        buy_close(context.main_futures[future_kinds_shanghai[0]], sell_num)
        is_closed = True

    if buy_pnl >= 20 and buy_num > 0:
        if buy_num > 10:
            buy_num = 10
        sell_close(context.main_futures[future_kinds_shanghai[0]], buy_num)
        is_closed = True

    if sell_pnl <= -40 and sell_num > 0:
        context.stop_sell_open = True
        if sell_num > 10:
            sell_num = 10
        buy_close(context.main_futures[future_kinds_shanghai[0]], sell_num)
        
    if buy_pnl <= -40 and buy_num > 0:
        context.stop_buy_open = True
        if sell_num > 10:
            sell_num = 10
        sell_close(context.main_futures[future_kinds_shanghai[0]], buy_num)

    if is_closed == True:
        return
    
    if_over = (context.future_account.margin / context.future_account.total_value) <= context.pot_rate
    sell_num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].sell_quantity
    buy_num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].buy_quantity
    if (bar_dict[context.main_futures[future_kinds_shanghai[0]]].close > (mean_price + std_price)) and if_over and (context.stop_sell_open == False) and sell_num <= context.max_hold:
        #print("close:%f, mean:%f , std:%f"%(bar_dict[context.main_futures[future_kinds_shanghai[0]]].close,mean_price,std_price))
        order = sell_open(context.main_futures[future_kinds_shanghai[0]], 2)
        if type(order) != list and order is not None and order.status == ORDER_STATUS.FILLED:
            num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].sell_quantity
            context.avg_sell = update_avg_sell(context.avg_sell, num-order.filled_quantity, order.avg_price, order.filled_quantity)

    elif bar_dict[context.main_futures[future_kinds_shanghai[0]]].close < (mean_price - std_price) and if_over and context.stop_buy_open == False and buy_num <= context.max_hold:
        #print("close:%f, mean:%f , std:%f"%(bar_dict[context.main_futures[future_kinds_shanghai[0]]].close,mean_price,std_price))
        order = buy_open(context.main_futures[future_kinds_shanghai[0]], 2)
        if type(order) != list and order is not None and order.status == ORDER_STATUS.FILLED:
            num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].buy_quantity
            context.avg_buy = update_avg_buy(context.avg_buy, num-order.filled_quantity, order.avg_price, order.filled_quantity)

def trade(context,bar_dict):

    if context.trade_state.stop_sell == True:
    	if context.trade_state.sell_count >= 20:
        	context.trade_state.stop_sell = False
        	context.trade_state.sell_count = 0
    	else:
        	context.trade_state.sell_count += 1
    
    if context.trade_state.stop_buy == True:
        if context.trade_state.buy_count >= 20:
            context.trade_state.stop_buy = False
            context.trade_state.buy_count = 0
        else:
            context.trade_state.buy_count += 1    

    [hour,mins,sec] = bar_dict['time'].split(':')
    
    if hour == '09' and mins == '01':
        context.counter = 0

    if context.last_main != context.main_futures[future_kinds_shanghai[0]]:
        close_all(context, context.last_main)
    context.counter += 1
    if context.counter < 30:
        return
    
    look_back_num = 30
    data = history_bars(future_kinds_shanghai[0]+'88',30, '1m', fields=['close'], skip_suspended=True)
    data = [i[0] for i in data]
    mean_price = np.average(data,weights=range(1,len(data)+1,1))
    std_price = np.std(data)
    std_price = sum(np.std(data)*range(1,len(data)+1,1))/sum(range(1,len(data)+1,1))
    print(std_price)
    is_closed = False
    sell_num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].sell_quantity
    buy_num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].buy_quantity
    
    sell_pnl = context.avg_sell - bar_dict[context.main_futures[future_kinds_shanghai[0]]].close
    buy_pnl = bar_dict[context.main_futures[future_kinds_shanghai[0]]].close - context.avg_buy
    if sell_num !=0 or buy_num!=0:
        print("sell_pnl:%f,sell_num:%d, buy_pnl:%f, buy_num:%d"%(sell_pnl,sell_num,buy_pnl,buy_num))


    if (bar_dict[context.main_futures[future_kinds_shanghai[0]]].close > (mean_price + std_price)) and if_over and (context.stop_sell_open == False) and sell_num <= context.max_hold:
        #print("close:%f, mean:%f , std:%f"%(bar_dict[context.main_futures[future_kinds_shanghai[0]]].close,mean_price,std_price))
        












	data = fetch_data('sc','bu')
	dates = data['datetime'].unique()
	tick_size = 10
	buy_multi = 2
	sell_multi = 3
	for date in dates:
		day_data = data[data['datetime'] == date]
		day_data = weighted_avg(day_data, name='weighted_avg', feature='last_price', if_include_now=False)
        day_data['if_buy'] = day_data['bid_price'] > (day_data['weighted_avg'] + tick_size * buy_multi)
        day_data['if_sell'] = day_data['ask_price'] < (day_data['weighted_avg'] - tick_size * sell_multi)
        day_data['sell']

def update_avg_buy(avg_buy_price, num, avg_price, filled_quantity):
    print("avg_sell_price:%f , num:%d,  avg_price:%f, filled_quantity:%d"%(avg_buy_price, num, avg_price, filled_quantity))
    sum_ = avg_buy_price * num + avg_price * filled_quantity
    avg_p = sum_/(num+filled_quantity)
    return avg_p
    

def update_avg_sell(avg_sell_price, num, avg_price, filled_quantity):
    print("avg_sell_price:%f , num:%d,  avg_price:%f, filled_quantity:%d"%(avg_sell_price, num, avg_price, filled_quantity))
    sum_ = avg_sell_price * num + avg_price * filled_quantity
    avg_p = sum_/(num+filled_quantity)
    return avg_p







def sell(future, price, num):
	order = sell_open(context.main_futures[future_kinds_shanghai[0]], 2)
    if order.status == ORDER_STATUS.FILLED:
        num = context.future_account.positions[context.main_futures[future_kinds_shanghai[0]]].sell_quantity
        context.avg_sell = update_avg_sell(context.avg_sell, num-order.filled_quantity, order.avg_price, order.filled_quantity)

def __main__():
	context = Context()
	trade()

