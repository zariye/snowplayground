from datetime import date

from tickers import tickers
import yfinance as yf
import logging
import sqlite3


def extract_stock_data(ticker):
    return yf.download(ticker, start="2024-01-01", end=date.today().strftime("%Y-%m-%d"))

def transform_stock_data(df):
    df = df.dropna()
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    return df

def generate_recommendations(df):
    df['Signal'] = 0
    df.loc[df['MA5'] > df['MA20'], 'Signal'] = 1  # Buy
    df.loc[df['MA5'] < df['MA20'], 'Signal'] = -1 # Sell
    df.loc[df['Signal'] == 0, 'Signal'] = 0  # Hold
    return df[['Signal']]

def flatten_columns_for_sql(df):
    new_columns = []
    for col in df.columns:
        if isinstance(col, tuple):
            new_columns.append(col[0])
        else:
            new_columns.append(str(col))
    df.columns = new_columns
    return df


def load_to_sqlite(df, db_name="stocks.db", table_name="stock_data"):
    df = flatten_columns_for_sql(df)

    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=True)
    conn.close()

if __name__ == "__main__":
    for ticker in tickers.values():
        logging.info(f"Processing {ticker}... ")
        try:
            df = extract_stock_data(ticker)
            df = transform_stock_data(df)
            generate_recommendations(df)
            load_to_sqlite(df, db_name="stocks.db", table_name=ticker.replace('.', '_'))

            logging.info(f"{ticker} done!\n")
        except Exception as e:
            logging.error(f"Failed for {ticker}: {e}\n")
