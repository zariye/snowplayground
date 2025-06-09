from contextlib import contextmanager

import snowflake.connector
from dotenv import load_dotenv
import os
import  pandas as pd
import logging

class Snowflake:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    @staticmethod
    def connect():
        load_dotenv()
        logging.info("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            account=os.getenv('ACCOUNT'),
            warehouse='COMPUTE',
            database='STOCKDATA',
            schema='PUBLIC',
            role='ACCOUNTADMIN'
        )
        return conn

    def update(self, df, ticker):
        conn = self.connect()
        cs = conn.cursor()

        self.create_table(cs, ticker)
        self.insert_data(cs, df, ticker)

        cs.close()
        conn.close()

    @staticmethod
    def insert_data(cs, df, ticker):
        df_clean = df.copy()
        numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        df_clean = df_clean.replace([float('inf'), -float('inf')], None)
        df_clean = df_clean.where(pd.notna(df_clean), None)

        for date, row in df_clean.iterrows():
            query = f"""
                INSERT INTO {ticker} (
                    Date, Open, High, Low, Close, Volume,
                    Dividends, Stock_Splits, MA5, MA20,
                    MA_Diff, Signal_Strength
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = [
                date.date(),
                float(row['Open']) if pd.notna(row['Open']) else None,
                float(row['High']) if pd.notna(row['High']) else None,
                float(row['Low']) if pd.notna(row['Low']) else None,
                float(row['Close']) if pd.notna(row['Close']) else None,
                float(row['Volume']) if pd.notna(row['Volume']) else None,
                float(row['Dividends']) if pd.notna(row['Dividends']) else None,
                float(row['Stock Splits']) if pd.notna(row['Stock Splits']) else None,
                float(row['MA5']) if pd.notna(row['MA5']) else None,
                float(row['MA20']) if pd.notna(row['MA20']) else None,
                float(row['MA_Diff']) if pd.notna(row['MA_Diff']) else None,
                float(row['Signal_Strength']) if pd.notna(row['Signal_Strength']) else None
            ]
            cs.execute(query, values)


    @staticmethod
    def create_table(cs, ticker):
        cs.execute(f"""
        CREATE OR REPLACE TABLE {ticker} (
            Date DATE,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Close FLOAT,
            Volume FLOAT,
            Dividends FLOAT,
            Stock_Splits FLOAT,
            MA5 FLOAT,
            MA20 FLOAT,
            MA_Diff FLOAT,
            Signal_Strength FLOAT
        )
        """)
