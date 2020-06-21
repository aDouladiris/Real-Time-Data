import datetime as dt

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import animation, rc, style

from binance.client import Client
from binance.websockets import BinanceSocketManager

style.use('fivethirtyeight')


api_key = None
api_secret = None

client = Client(api_key, api_secret)

symbol = 'BTCUSDT'

coins = 'BTC', 'LTC', 'XRP', 'ETH', 'EOS'
  
period = '60 minute ago UTC+2'

coin = 'BTC'

plot_df = pd.DataFrame() # begin empty

def creat_signals(plot_df):
  live_df = pd.DataFrame() # begin empty

  #print(coin)
  ratio = [f"{coin}-USD"]

  klines = client.get_historical_klines(f"{coin}USDT", Client.KLINE_INTERVAL_1MINUTE, f"{period}")  

  df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

  plot_df = df.drop(columns=['open', 'high', 'low', 'volume','close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',  'Taker buy quote asset volume', 'Ignore'])

  df.drop(columns=['close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',   'Taker buy quote asset volume', 'Ignore'], inplace=True)
  df = df[['close', 'volume']]
  df['close'] = df['close'].astype(float)
  df['volume'] = df['volume'].astype(float)
  df.rename(columns={"close": f"{ratio}_close", "volume": f"{ratio}_volume"}, inplace=True)

  if len(live_df)==0:  # if the dataframe is empty
       live_df = df  # then it's just the current df
  else:  # otherwise, join this data to the main one
        live_df = live_df.join(df)

  return plot_df.values.tolist()




# Create figure for plotting
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
fig, ax = plt.subplots(figsize=(15,5))
#plt.close()

#This function is called periodically from FuncAnimation
def animate(i):
  datas = creat_signals(plot_df)
  xs = []
  ys = []

  for line in datas:
    xs.append(float(line[0]))
    ys.append(float(line[1]))
  

  # Draw x and y lists
  ax.clear()
  ax.plot(xs, ys)
  


# Set up plot to call animate() function periodically
anim = animation.FuncAnimation(fig, animate, frames=100, blit=False)

plt.show()
