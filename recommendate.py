import sqlite3
import sys
import pandas as pd

from tickers import tickers

def signal_to_label(signal):
    if signal == 1:
        return "BUY 📈"
    elif signal == -1:
        return "SELL 📉"
    else:
        return "HOLD 🤝"

def flatten_columns(df):
    new_columns = []
    for col in df.columns:
        if isinstance(col, tuple):
            new_columns.append("_".join([str(c) for c in col if c]))  # join non-empty parts
        else:
            new_columns.append(col)
    df.columns = new_columns
    return df

def see_recommendations(db_name, ticker):
    conn = sqlite3.connect(db_name)
    table_name = ticker.replace('.', '_')

    query = f"""
    SELECT *
    FROM {table_name}
    ORDER BY Date DESC
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = flatten_columns(df)

    print(f"Available columns: {list(df.columns)}")

    selected_cols = []
    for col in ['Close', 'Adj Close', 'MA5', 'MA20', 'Signal', 'Date']:
        if col in df.columns:
            selected_cols.append(col)

    df = df[selected_cols]

    if 'Signal' in df.columns:
        df['Recommendation'] = df['Signal'].apply(signal_to_label)

    print("\n📈 Last 10 Recommendations:\n")
    print(df[['Date', *[col for col in selected_cols if col != 'Date'], 'Recommendation']])



if __name__ == "__main__":
    for ticker_name in tickers.values():
        print(f"Processing {ticker_name}... 🚀")
        try:
            see_recommendations("stocks.db", ticker_name)
        except Exception as e:
            print(f"Failed for {ticker_name}: {e}\n")
