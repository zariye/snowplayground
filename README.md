# Stock Pipeline & snowflake playground

This is a sample project to demonstrate a stock data pipeline that fetches historical stock data, calculates moving averages, generates trading recommendations, and visualizes the results using Streamlit.

In the subfolder playground is another example to play with different features of Snowflake, such as analyzing linage or streaming.

----

## Setup Stock Pipeline

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

--- 
## Snowflake Playground

### Sync with Snowflake
using the `abctl` tool, you can sync your GitHub repository with Snowflake.

```bash
curl -LsfS https://get.airbyte.com | bash -
abctl local install
abctl local credentials
```
