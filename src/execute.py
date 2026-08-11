import pandas as pd
import ccxt
import ta
import numpy as np

exchange = ccxt.coinsph () # default id
coinsph = ccxt.coinsph ({ 'id': 'okcoin1' })

data_1d = exchange.fetch_ohlcv(symbol='BTC/PHP', timeframe='1d', since=None, limit=None, params={})
data_1w = exchange.fetch_ohlcv(symbol='BTC/PHP', timeframe='1w', since=None, limit=None, params={})
data_4h = exchange.fetch_ohlcv(symbol='BTC/PHP', timeframe='4h', since=None, limit=None, params={})
df = pd.DataFrame(data_1d)
#df.to_csv('Raw-btc.csv', index=False)
columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
cleaned_df1d = pd.DataFrame(data_1d, columns=columns)
cleaned_df1w = pd.DataFrame(data_1w, columns=columns)
cleaned_df4h = pd.DataFrame(data_4h, columns=columns)
cleaned_df1d["timestamp"] = pd.to_datetime(cleaned_df1d["timestamp"], unit="ms")
cleaned_df1w["timestamp"] = pd.to_datetime(cleaned_df1w["timestamp"], unit="ms")
cleaned_df4h["timestamp"] = pd.to_datetime(cleaned_df4h["timestamp"], unit="ms")
#cleaned_df1d.to_csv('Cleaned-btc.csv', index=False)
#cleaned_df1w.to_csv('Cleaned-btc-weekly.csv', index=False)
#cleaned_df4h.to_csv('Cleaned-btc-4h.csv', index=False)

df = pd.read_csv('Cleaned-btc.csv')
df['EMA20'] = ta.trend.ema_indicator(df['close'], window=20)
df['EMA50'] = ta.trend.ema_indicator(df['close'], window=50)
df['mavolume'] = df['volume'].rolling(window=20).mean()
df['Prev_EMA_20'] = df['EMA20'].shift(1)
df['Prev_EMA_50'] = df['EMA50'].shift(1)
df1 = df[['high', 'low', 'close', 'EMA20', 'Prev_EMA_20']].tail(50)
df['RSI'] = ta.momentum.rsi(df['close'], window=14)
df['EMA_200'] = ta.trend.ema_indicator(df['close'], window=200)

df['ATR'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)

df['Trend_Bullish'] = df['close'] > df['EMA_200']
df['RSI_Recently_Oversold'] = (df['RSI'] < 35).rolling(window=14).max() == 1 
df['RSI_Overbought'] = df['RSI'] > 65

df_clean = df.dropna()