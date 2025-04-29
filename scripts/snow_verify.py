import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    account=os.getenv("ACCOUNT"),
    warehouse=os.getenv("WAREHOUSE"),
    database=os.getenv("DATABASE"),
    schema=os.getenv("SCHEMA")
)


cur = conn.cursor()
cur.execute("SHOW TABLES")
print(cur.fetchall())
cur.close()
conn.close()
