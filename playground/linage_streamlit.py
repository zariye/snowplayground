import streamlit as st
from graphviz import Digraph
import snowflake.connector

try:
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        role=st.secrets["snowflake"].get("role", None),
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

    query = "SELECT SOURCE, TARGET FROM MANUAL_LINEAGE"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    dot = Digraph()
    for src, tgt in rows:
        dot.edge(src, tgt)

    st.title("📊 Snowflake Lineage (Live from Snowflake)")
    st.graphviz_chart(dot)

except Exception as e:
    st.error(f"Connection failed: {e}")


