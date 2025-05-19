import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tickers import tickers
from snow import connect


def load_data(ticker):
    conn = connect()
    cs = conn.cursor()

    safe_ticker = f'"{ticker}"' if '.' in ticker else ticker

    query = f"SELECT * FROM {safe_ticker} ORDER BY Date"
    cs.execute(query)

    columns = [desc[0] for desc in cs.description]
    data = cs.fetchall()

    cs.close()
    conn.close()

    if not data:
        st.error(f"No data found for ticker {ticker}")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=columns)

    column_mapping = {
        'DATE': 'Date',
        'OPEN': 'Open',
        'HIGH': 'High',
        'LOW': 'Low',
        'CLOSE': 'Close',
        'VOLUME': 'Volume',
        'DIVIDENDS': 'Dividends',
        'STOCK_SPLITS': 'Stock_Splits',
        'MA5': 'MA5',
        'MA20': 'MA20',
        'MA_DIFF': 'MA_Diff',
        'SIGNAL_STRENGTH': 'Signal_Strength'
    }

    df = df.rename(columns=column_mapping)

    df['Date'] = pd.to_datetime(df['Date'])

    return df


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
        with st.spinner(f"Loading data for {ticker_symbol}..."):
            df = load_data(ticker_symbol)

        if df.empty:
            st.warning(f"No data available for {ticker_symbol}")
            return

        last_row = df.iloc[-1]
        cols = st.columns(4)

        cols[0].metric("Last Close Price", f"${last_row['Close']:.2f}")

        signal_strength_map = {
            3: "STRONG BUY 📈📈",
            2: "BUY 📈",
            1: "WEAK BUY 📈",
            0: "NEUTRAL ↔️",
            -1: "WEAK SELL 📉",
            -2: "SELL 📉",
            -3: "STRONG SELL 📉📉"
        }

        signal_strength = int(last_row['Signal_Strength'])

        cols[1].metric("Signal Strength",
                       signal_strength_map[signal_strength])

        cols[2].metric("MA Difference",
                       f"{last_row['MA_Diff']:.2f}%")

        price_change = last_row['Close'] - df.iloc[-2]['Close']
        cols[3].metric("Price Change",
                       f"${price_change:.2f}",
                       f"{(price_change / df.iloc[-2]['Close'] * 100):.2f}%")

        fig = plot_stock(df, ticker_symbol)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Signal Distribution (Last 30 Days)")
        recent_signals = df.tail(30)['Signal_Strength'].value_counts().sort_index()
        st.bar_chart(recent_signals)

        st.subheader("Recent Data")
        display_cols = ['Date', 'Close', 'MA5', 'MA20', 'MA_Diff', 'Signal_Strength']
        st.dataframe(df[display_cols].tail().sort_index(ascending=False))

    except Exception as e:
        st.error(f"Error loading data for {ticker_symbol}: {e}")
        st.exception(e)

def get_color(x):
    try:
        return {
            3: 'darkgreen',
            2: 'lightgreen',
            1: 'palegreen',
            0: 'gray',
            -1: 'pink',
            -2: 'lightcoral',
            -3: 'darkred'
        }.get(int(x), 'gray')
    except:
        return 'gray'

def plot_stock(df, ticker):
    df = df.copy()
    df['Signal_Strength'] = pd.to_numeric(df['Signal_Strength'].fillna(0))

    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.03,
                        row_heights=[0.5, 0.25, 0.25],
                        subplot_titles=(f'{ticker} Price and Moving Averages',
                                        'Signal Strength',
                                        'MA Difference %'))

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

    df['Signal_Strength'] = pd.to_numeric(df['Signal_Strength'])

    signal_colors = df['Signal_Strength'].apply(get_color)

    fig.add_trace(go.Bar(x=df['Date'],
                         y=df['Signal_Strength'],
                         name='Signal Strength',
                         marker_color=signal_colors), row=2, col=1)

    fig.add_trace(go.Scatter(x=df['Date'],
                             y=df['MA_Diff'],
                             name='MA Difference %',
                             fill='tozeroy',
                             line=dict(color='purple')), row=3, col=1)

    strong_buy = df[df['Signal_Strength'] >= 2]
    fig.add_trace(go.Scatter(x=strong_buy['Date'],
                             y=strong_buy['Close'],
                             mode='markers',
                             name='Strong Buy',
                             marker=dict(color='darkgreen', size=12, symbol='triangle-up'),
                             showlegend=True), row=1, col=1)

    strong_sell = df[df['Signal_Strength'] <= -2]
    fig.add_trace(go.Scatter(x=strong_sell['Date'],
                             y=strong_sell['Close'],
                             mode='markers',
                             name='Strong Sell',
                             marker=dict(color='darkred', size=12, symbol='triangle-down'),
                             showlegend=True), row=1, col=1)

    fig.update_layout(height=1000,
                      title_text=f"{ticker} Stock Analysis",
                      showlegend=True)

    fig.update_yaxes(title_text="Signal Strength (-3 to +3)", row=2, col=1)
    fig.update_yaxes(title_text="MA Diff %", row=3, col=1)

    return fig


if __name__ == "__main__":
    main()