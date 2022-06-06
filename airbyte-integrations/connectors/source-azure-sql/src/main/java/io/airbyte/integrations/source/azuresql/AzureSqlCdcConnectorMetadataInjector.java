/*
 * Copyright (c) 2022 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.integrations.source.azuresql;

import static io.airbyte.integrations.source.azuresql.AzureSqlSource.CDC_LSN;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import io.airbyte.integrations.debezium.CdcMetadataInjector;

public class AzureSqlCdcConnectorMetadataInjector implements CdcMetadataInjector {

  @Override
  public void addMetaData(final ObjectNode event, final JsonNode source) {
    final String commitLsn = source.get("commit_lsn").asText();
    event.put(CDC_LSN, commitLsn);
  }

  @Override
  public String namespace(final JsonNode source) {
    return source.get("schema").asText();
  }

}