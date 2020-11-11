# google-datacatalog-saphana-connector

Library for ingesting SAP Hana Database metadata into Google Cloud Data Catalog.

[![Python package][2]][2] [![PyPi][3]][4] [![License][5]][5] [![Issues][6]][7]

**Disclaimer: This is not an officially supported Google product.**

<!--
  ⚠️ DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY ️️⚠️
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

## Table of Contents

<!-- toc -->

- [1. Installation](#1-installation)
  * [1.1. Mac/Linux](#11-maclinux)
  * [1.2. Windows](#12-windows)
  * [1.3. Install from source](#13-install-from-source)
    + [1.3.1. Get the code](#131-get-the-code)
    + [1.3.2. Create and activate a *virtualenv*](#132-create-and-activate-a-virtualenv)
    + [1.3.3. Install the library](#133-install-the-library)
- [2. Environment setup](#2-environment-setup)
  * [2.1. Auth credentials](#21-auth-credentials)
    + [2.1.1. Create a service account and grant it below roles](#211-create-a-service-account-and-grant-it-below-roles)
    + [2.1.2. Download a JSON key and save it as](#212-download-a-json-key-and-save-it-as)
  * [2.2. Set environment variables](#22-set-environment-variables)
- [3. Adapt user configurations](#3-adapt-user-configurations)
- [4. Run entry point](#4-run-entry-point)
  * [4.1. Run Python entry point](#41-run-python-entry-point)
  * [4.2. Run Docker entry point](#42-run-docker-entry-point)
- [5 Scripts inside tools](#5-scripts-inside-tools)
  * [5.1. Run clean up](#51-run-clean-up)
- [6. Developer environment](#6-developer-environment)
  * [6.1. Install and run Yapf formatter](#61-install-and-run-yapf-formatter)
  * [6.2. Install and run Flake8 linter](#62-install-and-run-flake8-linter)
  * [6.3. Run Tests](#63-run-tests)
- [7. Metrics](#7-metrics)
- [8. Troubleshooting](#8-troubleshooting)

<!-- tocstop -->

-----

## 1. Installation

Install this library in a [virtualenv][1] using pip. [virtualenv][1] is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With [virtualenv][1], it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies. Make sure you use Python 3.6+. This connector is tested in versions
3.6, 3.7, 3.8.


### 1.1. Mac/Linux

```shell script
pip3 install virtualenv
virtualenv --python python3.7 <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install google-datacatalog-saphana-connector
```

### 1.2. Windows

```bash
pip3 install virtualenv
virtualenv --python python3.7 <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-datacatalog-saphana-connector
```

### 1.3. Install from source

#### 1.3.1. Get the code

````bash
git clone https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/
cd datacatalog-connectors-rdbms/google-datacatalog-saphana-connector
````

#### 1.3.2. Create and activate a *virtualenv*

```bash
pip3 install virtualenv
virtualenv --python python3.7 <your-env>
source <your-env>/bin/activate
```

#### 1.3.3. Install the library

```bash
pip install .
```

## 2. Environment setup

### 2.1. Auth credentials

#### 2.1.1. Create a service account and grant it below roles

- Data Catalog Admin

#### 2.1.2. Download a JSON key and save it as
- `<YOUR-CREDENTIALS_FILES_FOLDER>/saphana2dc-credentials.json`

> Please notice this folder and file will be required in next steps.

### 2.2. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file

export SAPHANA2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export SAPHANA2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export SAPHANA2DC_SAPHANA_SERVER=saphana_server
export SAPHANA2DC_SAPHANA_USERNAME=saphana_username
export SAPHANA2DC_SAPHANA_PASSWORD=saphana_password
export SAPHANA2DC_SAPHANA_DATABASE=saphana_database
export SAPHANA2DC_RAW_METADATA_CSV=saphana_raw_csv (If supplied ignores the SAPHANA server credentials)

```

## 3. Adapt user configurations

Along with default metadata, the connector can enrich metadata with user provided values as well,
 such as adding a prefix to each schema and tables name. 
 
 The table below shows what metadata is scraped by default, and what is configurable.

| Metadata                     | Description                                        | Scraped by default | Config option                                |                    
| ---                          | ---                                                | ---                | ---                                          |                       
| schema_name                  | Name of the Schema                                 | Y                  | ---                                          | 
| schema_owner                 | Owner of the Schema                                | Y                  | ---                                          | 
| schema_create_time           | Schema creation time                               | Y                  | ---                                          | 
| table_name                   | Name of a table                                    | Y                  | ---                                          | 
| table_type                   | Type of the table (ROW or COLUMN oriented)         | Y                  | ---                                          | 
| has_primary_key              | Whether a Table has a primary key                  | Y                  | ---                                          | 
| table_description            | Table description                                  | Y                  | ---                                          | 
| table_create_time            | Table creation time                                | Y                  | ---                                          | 
| column_name                  | Name of a column                                   | Y                  | ---                                          | 
| column_type                  | Column data type                                   | Y                  | ---                                          | 
| column_nullable              | Whether a column is nullable                       | Y                  | ---                                          | 
| column_mask                  | Whether a column has data mask                     | Y                  | ---                                          | 
| column_mask_expression       | Column mask expression                             | Y                  | ---                                          |
| prefix                       | Prefix to be added to schema and tables name       | N/A                | enrich_metadata.entry_prefix                 | 
| entry_id_pattern_for_prefix  | Entry ID pattern which the prefix will be applied  | N/A                | enrich_metadata.entry_id_pattern_for_prefix  | 
| table_size_mb            | Size of a table, in MB                     | N                  | sync_row_counts         | 
|table_rows                | Number of rows in a table                  | N                  | sync_row_counts         |

 
 `prefix` should comply with Data Catalog `entryId`: 
 ```text
The ID must begin with a letter or underscore, contain only English letters, numbers and underscores, and have at most 64 characters (combined the prefix + the entryId).
```   

if the `entry_id_pattern_for_prefix` is supplied, the prefix will only be applied to this pattern.
 
Sample configuration file [ingest_cfg.yaml](https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/blob/master/google-datacatalog-saphana-connector/ingest_cfg.yaml) in the repository root shows what kind of configuration is expected. 

**If you want to enable the user defined config, please add ingest_cfg.yaml to the directory from which you execute the connector and adapt it to your needs.** 

## 4. Run entry point

### 4.1. Run Python entry point

- Virtualenv

```bash
google-datacatalog-saphana-connector \
--datacatalog-project-id=$SAPHANA2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$SAPHANA2DC_DATACATALOG_LOCATION_ID \
--saphana-host=$SAPHANA2DC_SAPHANA_SERVER \
--saphana-user=$SAPHANA2DC_SAPHANA_USERNAME \
--saphana-pass=$SAPHANA2DC_SAPHANA_PASSWORD \
--saphana-database=$SAPHANA2DC_SAPHANA_DATABASE  \
--raw-metadata-csv=$SAPHANA2DC_RAW_METADATA_CSV      
```

### 4.2. Run Docker entry point

```bash
docker build -t saphana2datacatalog .
docker run --rm --tty -v YOUR-CREDENTIALS_FILES_FOLDER:/data saphana2datacatalog \
--datacatalog-project-id=$SAPHANA2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$SAPHANA2DC_DATACATALOG_LOCATION_ID \
--saphana-host=$SAPHANA2DC_SAPHANA_SERVER \
--saphana-user=$SAPHANA2DC_SAPHANA_USERNAME \
--saphana-pass=$SAPHANA2DC_SAPHANA_PASSWORD \
--saphana-database=$SAPHANA2DC_SAPHANA_DATABASE  \
--raw-metadata-csv=$SAPHANA2DC_RAW_METADATA_CSV       
```

## 5 Scripts inside tools

### 5.1. Data Catalog clean up

```bash
# List of projects split by comma. Can be a single value without comma
export SAPHANA2DC_DATACATALOG_PROJECT_IDS=my-project-1,my-project-2
```

```bash
# Run the clean up
python tools/cleanup_datacatalog.py --datacatalog-project-ids=$SAPHANA2DC_DATACATALOG_PROJECT_IDS 

```

## 6. Developer environment

### 6.1. Install and run Yapf formatter

```bash
pip install --upgrade yapf

# Auto update files
yapf --in-place --recursive src tests

# Show diff
yapf --diff --recursive src tests

# Set up pre-commit hook
# From the root of your git project.
curl -o pre-commit.sh https://raw.githubusercontent.com/google/yapf/master/plugins/pre-commit.sh
chmod a+x pre-commit.sh
mv pre-commit.sh .git/hooks/pre-commit
```

### 6.2. Install and run Flake8 linter

```bash
pip install --upgrade flake8
flake8 src tests
```


### 6.3. Run Tests

```bash
python setup.py test
```

## 7. Metrics

[Metrics README.md](docs/README.md)

## 8. Troubleshooting

In the case a connector execution hits Data Catalog quota limit, an error will be raised and logged with the following detailement, depending on the performed operation READ/WRITE/SEARCH: 
```
status = StatusCode.RESOURCE_EXHAUSTED
details = "Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'."
debug_error_string = 
"{"created":"@1587396969.506556000", "description":"Error received from peer ipv4:172.217.29.42:443","file":"src/core/lib/surface/call.cc","file_line":1056,"grpc_message":"Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'.","grpc_status":8}"
```
For more info about Data Catalog quota, go to: [Data Catalog quota docs](https://cloud.google.com/data-catalog/docs/resources/quotas).

[1]: https://virtualenv.pypa.io/en/latest/
[2]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/workflows/Python%20package/badge.svg?branch=master
[3]: https://img.shields.io/pypi/v/google-datacatalog-saphana-connector.svg
[4]: https://pypi.org/project/google-datacatalog-saphana-connector/
[5]: https://img.shields.io/github/license/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[6]: https://img.shields.io/github/issues/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[7]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/issues
