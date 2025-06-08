def main(session):
    import pandas as pd

    lineage_data = [
        {"SOURCE": "RAW.JSON_DATA", "TARGET": "RAW.CLEAN_CAR_SPECS"},
        {"SOURCE": "RAW.CLEAN_CAR_SPECS", "TARGET": "MARTS.VEHICLE_OVERVIEW"},
        {"SOURCE": "MARTS.VEHICLE_OVERVIEW", "TARGET": "DASHBOARDS.FLEET_ANALYTICS"},
        {"SOURCE": "RAW.JSON_DATA", "TARGET": "RAW.ERROR_LOGS"},
    ]

    df = pd.DataFrame(lineage_data)
    df_snowflake = session.create_dataframe(df)
    df_snowflake.write.save_as_table("DEMO_DB.RAW.MANUAL_LINEAGE", mode="overwrite")

    return session.create_dataframe(df)