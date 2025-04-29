# Stock Pipeline

A simple Python application for fetching stock data and generating trading recommendations based on moving average crossovers.

## Features

- Fetches historical stock data from Yahoo Finance
- Calculates 5-day and 20-day moving averages
- Generates BUY/SELL/HOLD signals based on MA crossovers
- Stores data in SQLite database
- Shows recent recommendations for configured stocks
- Dashboard for visualizing stock data and recommendations using Streamlit

## Setup

### Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install required packages:
```bash
pip install streamlit plotly pandas yfinance snowflake-connector-python python-dotenv
```

## Usage

### Update Stock Data

To fetch new stock data and update recommendations in sqlite database:
```bash
python3 update.py
```

### View Recommendations

To view the latest recommendations for all configured stocks:

```bash
python3 recommendate.py
```

## Interactive Dashboard

To launch the interactive dashboard:

```bash
streamlit run dashboard.py
```



###  Configuration

Stock tickers are configured in tickers.py. Add or remove stocks by modifying the tickers dictionary:

```bash
tickers = {
    'Apple': 'AAPL',
    'AMD': 'AMD',
    # Add more stocks here
}
```