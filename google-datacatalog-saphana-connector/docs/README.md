[Back to README.md](../README.md)

# Metrics

This execution was collected from a [SAP HANA EXPRESS 2.0 SP04](https://console.cloud.google.com/marketplace/product/sap-public/sap-hana-express) 
instance populated with 1020 tables and 1 function distributed into 4 schemas,
running the `google-datacatalog-saphana-connector` to ingest those entities into Data Catalog. 
The connector was executed in a local workstation to simulate the connection to a on-premise 
environment. This shows what the user might expect when running this connector.

The following metrics are not a guarantee, they are approximations that may change depending on the 
environment, network and execution.


| Metric                     | Description                                       | VALUE             |
| ---                        | ---                                               | ---               |
| **elapsed_time**           | Elapsed time from the execution.                  | 30 Minutes        |
| **entries_length**         | Number of entities ingested into Data Catalog.    | 1025              |
| **metadata_payload_bytes** | Amount of bytes processed from the source system. | 1325043 (1.32 MB) |
| **datacatalog_api_calls**  | Amount of Data Catalog API calls executed.        | 4117              |



### Data Catalog API calls drilldown

| Data Catalog API Method                                            | Calls |
| ---                                                                | --:   | 
| **google.cloud.datacatalog.v1.DataCatalog.CreateEntry#200**        | 1025  | 
| **google.cloud.datacatalog.v1.DataCatalog.CreateEntryGroup#200**   | 1     |
| **google.cloud.datacatalog.v1.DataCatalog.CreateEntryGroup#409**   | 3     |  
| **google.cloud.datacatalog.v1.DataCatalog.CreateTag#200**          | 1025  |
| **google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplate#200**  | 3     |
| **google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplate#409**  | 9     |
| **google.cloud.datacatalog.v1.DataCatalog.GetEntry#403**           | 1025  | 
| **google.cloud.datacatalog.v1.DataCatalog.ListTags#200**           | 1025  | 
| **google.cloud.datacatalog.v1.DataCatalog.SearchCatalog#200**      | 1     |  
