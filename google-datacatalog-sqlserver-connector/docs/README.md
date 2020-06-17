[Back to README.md](../README.md)

# Metrics

This execution was collected from a SQL Server 2017 Standard instance populated with 1008 tables distributed into 4 schemas, running the sqlserver2datacatalog connector to ingest
those entities into Data Catalog. This shows what the user might expect when running this connector.

The following metrics are not a guarantee, they are approximations that may change depending on the environment, network and execution.


| Metric                     | Description                                       | VALUE             |
| ---                        | ---                                               | ---               |
| **elapsed_time**           | Elapsed time from the execution.                  | 27 Minutes        |
| **entries_length**         | Number of entities ingested into Data Catalog.    | 1012              |
| **metadata_payload_bytes** | Amount of bytes processed from the source system. | 1284742 (1.12 MB) |
| **datacatalog_api_calls**  | Amount of Data Catalog API calls executed.        | 4061              |



### Data Catalog API calls drilldown

| Data Catalog API Method                                                 | Calls |
| ---                                                                     | ---   | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateEntry#200**        | 1012  | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateEntryGroup#200**   | 1     |
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateEntryGroup#409**   | 3     |  
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateTag#200**          | 1012  |
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateTagTemplate#200**  | 2     |
| **google.cloud.datacatalog.v1beta1.DataCatalog.CreateTagTemplate#409**  | 6     |
| **google.cloud.datacatalog.v1beta1.DataCatalog.GetEntry#403**           | 1012  | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.ListTags#200**           | 1012  | 
| **google.cloud.datacatalog.v1beta1.DataCatalog.SearchCatalog#200**      | 1     |  
