import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tickers import tickers


def load_data(ticker):
    conn = sqlite3.connect('stocks.db')
    table_name = ticker.replace('.', '_')
    query = f"SELECT * FROM {table_name} ORDER BY Date"
    df = pd.read_sql_query(query, conn)
    conn.close()
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def plot_stock(df, ticker):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.03,
                        subplot_titles=(f'{ticker} Price and Moving Averages', 'Trading Signals'))

    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'],
                             mode='lines',
                             name='Close Price',
                             line=dict(color='#17BECF')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA5'],
                             mode='lines',
                             name='MA5',
                             line=dict(color='#7F7F7F')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'],
                             mode='lines',
                             name='MA20',
                             line=dict(color='#FFA500')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Date'], y=df['Signal'],
                             mode='lines',
                             name='Signal',
                             line=dict(color='#2CA02C')), row=2, col=1)

    buy_signals = df[df['Signal'] == 1]
    fig.add_trace(go.Scatter(x=buy_signals['Date'],
                             y=buy_signals['Close'],
                             mode='markers',
                             name='Buy Signal',
                             marker=dict(color='green', size=10, symbol='triangle-up'),
                             showlegend=True), row=1, col=1)

    sell_signals = df[df['Signal'] == -1]
    fig.add_trace(go.Scatter(x=sell_signals['Date'],
                             y=sell_signals['Close'],
                             mode='markers',
                             name='Sell Signal',
                             marker=dict(color='red', size=10, symbol='triangle-down'),
                             showlegend=True), row=1, col=1)

    fig.update_layout(height=800,
                      title_text=f"{ticker} Stock Analysis",
                      showlegend=True)

    return fig


def main():
    st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
    st.title("📈 Stock Analysis Dashboard")

    st.sidebar.header("Settings")
    selected_ticker_name = st.sidebar.selectbox(
        "Select Stock",
        options=list(tickers.keys())
    )

    ticker_symbol = tickers[selected_ticker_name]

    try:
        df = load_data(ticker_symbol)

        last_row = df.iloc[-1]
        cols = st.columns(3)

        cols[0].metric("Last Close Price", f"${last_row['Close']:.2f}")

        signal_map = {1: "BUY 📈", -1: "SELL 📉", 0: "HOLD 🤝"}
        cols[1].metric("Current Signal", signal_map[last_row['Signal']])

        price_change = last_row['Close'] - df.iloc[-2]['Close']
        cols[2].metric("Price Change", f"${price_change:.2f}",
                       f"{(price_change / df.iloc[-2]['Close'] * 100):.2f}%")

        fig = plot_stock(df, ticker_symbol)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recent Data")
        st.dataframe(df.tail().sort_index(ascending=False))

    except Exception as e:
        st.error(f"Error loading data for {ticker_symbol}: {e}")


if __name__ == "__main__":
    main()