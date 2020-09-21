[Back to README.md](../README.md)

# Metrics

This execution was collected from a PostgreSQL 9.6 instance populated with 1001 tables, running the postgresql2datacatalog connector to ingest
those entities into Data Catalog. This shows what the user might expect when running this connector.

The following metrics are not a guarantee, they are approximations that may change depending on the environment, network and execution.


| Metric                     | Description                                       | VALUE            |
| ---                        | ---                                               | ---              |
| **elapsed_time**           | Elapsed time from the execution.                  | 29 Minutes       |
| **entries_length**         | Number of entities ingested into Data Catalog.    | 1001             |
| **metadata_payload_bytes** | Amount of bytes processed from the source system. | 877566 (0.88 MB) |
| **datacatalog_api_calls**  | Amount of Data Catalog API calls executed.        | 4008             |

Refreshing metadata slows down the ingestion by factor of 2.3. Read more about toggling refreshing on/off in the Adapt User Configuration section of [README.md](../README.md).  

### Data Catalog API calls drilldown

| Data Catalog API Method                                                 | Calls |
| ---                                                                     | ---   | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateEntry#200**        | 1001  | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateEntryGroup#200**   | 1     | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateTag#200**          | 1001  |
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateTagTemplate#200**  | 2     |
| **google.cloud.datacatalog.v1beta1.DataCatalog.GetEntry#403**           | 1001  | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.ListTags#200**           | 1001  | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.SearchCatalog#200**      | 1     |  
