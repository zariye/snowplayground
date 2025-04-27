from datetime import date

from tickers import tickers
import yfinance as yf
import logging
import sqlite3
import pandas as pd

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

def update_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period='1y')

        if df.empty:
            print(f"No data found for {ticker}")
            return

        df = calculate_signals(df)

        conn = sqlite3.connect('stocks.db')
        table_name = ticker.replace('.', '_')
        df.to_sql(table_name, conn, if_exists='replace')
        conn.close()

        print(f"Updated {ticker} successfully")

    except Exception as e:
        print(f"Error updating {ticker}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    for ticker in tickers.values():
        logging.info(f"Processing {ticker}... ")
        try:
            update_stock_data(ticker)
            logging.info(f"{ticker} done!\n")
        except Exception as e:
            logging.error(f"Failed for {ticker}: {e}\n")
