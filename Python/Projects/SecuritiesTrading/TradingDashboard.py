import pandas as pd
import numpy as np
import yfinance as yf
import backtrader as bt

# CONFIGURATION
TICKER = "AAPL"
START_DATE = "2022-01-01"
END_DATE = "2024-01-01"

# FETCH MARKET DATA
def get_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    return df

# STRATEGY IMPLEMENTATION
class SMACross(bt.Strategy):
    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(period=50)
        self.sma_long = bt.indicators.SimpleMovingAverage(period=200)

    def next(self):
        if self.sma_short[0] > self.sma_long[0]:
            self.buy()
        elif self.sma_short[0] < self.sma_long[0]:
            self.sell()

# BACKTESTING
def run_backtest():
    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=get_data(TICKER, START_DATE, END_DATE))
    cerebro.adddata(data)
    cerebro.addstrategy(SMACross)
    cerebro.run()
    cerebro.plot()

if __name__ == "__main__":
    run_backtest()