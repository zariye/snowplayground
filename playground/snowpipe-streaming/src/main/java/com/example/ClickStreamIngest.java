package com.example;

import net.snowflake.ingest.streaming.*;
import java.security.PrivateKey;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.UUID;


public class ClickStreamIngest {
    public static void main(String[] args) throws Exception {

        PrivateKey privateKey = IngestHelper.loadPrivateKey("/Users/zara/Projects/studying/stockpipeline/playground/snowpipe-streaming/rsa_key.p8");



        Properties props = new Properties();
        props.put("account", System.getenv("ACCOUNT"));
        props.put("user", "STREAMING_USER");
        props.put("privateKey", privateKey);
        props.put("role", "STREAMING_ROLE");
        props.put("warehouse", "COMPUTE_WH");
        props.put("database", "DEMO_DB");
        props.put("schema", "RAW");

        SnowflakeStreamingIngestClient client = SnowflakeStreamingIngestClientFactory.builder("your_client_name")
            .setProperties(props)
            .build();

        SnowflakeStreamingIngestChannel channel = client.openChannel(OpenChannelRequest.builder("channel_name")
                .setDBName("your_DEMO_DBdb")
                .setSchemaName("RAW")
                .setTableName("STREAM_CLICKS")
                .build());

       for (int i = 0; i < 10; i++) {
            Map<String, Object> row = new HashMap<>();
            row.put("id", UUID.randomUUID().toString());
            row.put("value", i);
            channel.insertRow(row, UUID.randomUUID().toString());
        }

        channel.close().get();
        client.close();
    }
}
