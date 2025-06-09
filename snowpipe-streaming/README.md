# Streaming example using Snowflake Ingest SDK

## Pre-requisites

### Locally
#### install snowflake-ingest-java
- Download https://github.com/snowflakedb/snowflake-ingest-java/releases
- Unzip and build the jar file `mvn clean package -DskipTests`
- Manually install the jar file to your local maven repository
```bash
 mvn install:install-file \
  -Dfile=target/snowflake-ingest-sdk.jar \
  -DgroupId=com.snowflake \
  -DartifactId=snowflake-ingest-sdk \
  -Dversion=4.0.1 \
  -Dpackaging=jar
```
#### Generate RSA key pair, format PKCS#8

```bash
  openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```
prepare public key snowsight upload
```bash
openssl rsa -in rsa_key.p8 -pubout -outform PEM | \
  sed -ne '/-BEGIN PUBLIC KEY-/,/-END PUBLIC KEY-/p' | \
  sed '/-BEGIN PUBLIC KEY-/d;/-END PUBLIC KEY-/d' | \
  tr -d '\n'
```


### In snowsight
#### Set roles and permissions

```sql
CREATE TABLE IF NOT EXISTS DEMO_DB.RAW.STREAM_CLICKS (
    event_id STRING,
    user_id INTEGER,
    event_type STRING,
    ts STRING
);

CREATE ROLE IF NOT EXISTS STREAMING_ROLE;

GRANT USAGE ON DATABASE DEMO_DB TO ROLE STREAMING_ROLE;
GRANT USAGE ON SCHEMA DEMO_DB.RAW TO ROLE STREAMING_ROLE;
GRANT INSERT, SELECT ON TABLE DEMO_DB.RAW.STREAM_CLICKS TO ROLE STREAMING_ROLE;


GRANT CREATE STAGE ON SCHEMA DEMO_DB.RAW TO ROLE STREAMING_ROLE;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE STREAMING_ROLE;

CREATE USER IF NOT EXISTS STREAMING_USER;

ALTER USER STREAMING_USER SET RSA_PUBLIC_KEY='<PUBLIC_KEY>';

CREATE ROLE IF NOT EXISTS STREAMING_ROLE;

GRANT USAGE ON DATABASE DEMO_DB TO ROLE STREAMING_ROLE;
GRANT USAGE ON SCHEMA DEMO_DB.RAW TO ROLE STREAMING_ROLE;
GRANT INSERT, SELECT ON TABLE DEMO_DB.RAW.STREAM_CLICKS TO ROLE STREAMING_ROLE;
GRANT CREATE STAGE ON SCHEMA DEMO_DB.RAW TO ROLE STREAMING_ROLE;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE STREAMING_ROLE;

GRANT ROLE STREAMING_ROLE TO USER STREAMING_USER;
ALTER USER STREAMING_USER SET DEFAULT_ROLE = STREAMING_ROLE;

```

## Run the example
### Build the project
`mvn clean package`

### Run the example
` mvn exec:java -Dexec.mainClass="com.example.ClickStreamIngest"`
