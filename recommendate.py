import sqlite3
import pandas as pd

from tickers import tickers

def signal_to_label(strength):
    signal_map = {
        3: "STRONG BUY 📈📈",
        2: "BUY 📈",
        1: "WEAK BUY 📈",
        0: "NEUTRAL ↔️",
        -1: "WEAK SELL 📉",
        -2: "SELL 📉",
        -3: "STRONG SELL 📉📉"
    }
    return signal_map.get(strength, "UNKNOWN ❓")

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
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='{table_name}'
    """
    if not pd.read_sql_query(query, conn).empty:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} ORDER BY Date DESC LIMIT 10", conn)
        conn.close()

        df = flatten_columns(df)

        print("\nAvailable columns:", df.columns.tolist())

        required_cols = ['Date', 'Close', 'MA_Diff', 'Signal_Strength']
        if not all(col in df.columns for col in required_cols):
            print(f"Missing required columns. Please run update.py first.")
            return

        df['Recommendation'] = df['Signal_Strength'].apply(signal_to_label)

        print("\n📈 Last 10 Recommendations:\n")
        print(df[['Date', 'Close', 'MA_Diff', 'Signal_Strength', 'Recommendation']])
    else:
        print(f"No data found for {ticker}. Please run update.py first.")


if __name__ == "__main__":
    for ticker_name in tickers.values():
        print(f"Processing {ticker_name}... 🚀")
        try:
            see_recommendations("stocks.db", ticker_name)
        except Exception as e:
            print(f"Failed for {ticker_name}: {e}\n")
