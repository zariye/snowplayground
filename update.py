from snow import Snowflake
from tickers import tickers
import yfinance as yf
import logging

import pandas as pd

class Update:
    def __init__(self):
        self.snow = Snowflake()

    def stock_data(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period='1y')

            if df.empty:
                logging.error(f"No data found for {ticker}")
                return

            df = self.calculate_signals(df)
            df.reset_index()

            self.snow.update(df, ticker)

        except Exception as e:
            logging.error(f"Error updating {ticker}: {e}")

    @staticmethod
    def calculate_signals(df):
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()

        df['MA_Diff'] = ((df['MA5'] - df['MA20']) / df['MA20']) * 100

        df['Signal_Strength'] = pd.cut(
            df['MA_Diff'],
            bins=[-float('inf'), -5, -2, -0.5, 0.5, 2, 5, float('inf')],
            labels=[-3, -2, -1, 0, 1, 2, 3]
        ).astype(float)

        return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    for ticker in tickers.values():
        logging.info(f"Processing {ticker}... ")
        try:
            update = Update()
            update.stock_data(ticker)
            logging.info(f"{ticker} done!\n")
        except Exception as e:
            logging.error(f"Failed for {ticker}: {e}\n")
