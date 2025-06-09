package com.example;

import java.io.BufferedReader;
import java.io.FileReader;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Base64;

public class IngestHelper {

    public static PrivateKey loadPrivateKey(String filePath) throws Exception {
        StringBuilder pemContent = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            boolean inKey = false;

            while ((line = reader.readLine()) != null) {
                if (line.contains("BEGIN PRIVATE KEY")) {
                    inKey = true;
                } else if (line.contains("END PRIVATE KEY")) {
                    break;
                } else if (inKey) {
                    pemContent.append(line.trim());
                }
            }
        }

        byte[] decoded = Base64.getDecoder().decode(pemContent.toString());
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(decoded);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");

        return keyFactory.generatePrivate(keySpec);
    }
}
