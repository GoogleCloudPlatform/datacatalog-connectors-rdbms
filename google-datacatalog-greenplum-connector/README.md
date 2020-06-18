# google-datacatalog-greenplum-connector

Library for ingesting Greenplum metadata into Google Cloud Data Catalog.

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
  * [2.2 Set environment variables](#22-set-environment-variables)
- [3. Run entry point](#3-run-entry-point)
  * [3.1. Run Python entry point](#31-run-python-entry-point)
  * [3.2. Run Docker entry point](#32-run-docker-entry-point)
- [4 Scripts inside tools](#4-scripts-inside-tools)
  * [4.1. Run clean up](#41-run-clean-up)
  * [4.2. Extract CSV](#42-extract-csv)
- [5. Developer environment](#5-developer-environment)
  * [5.1. Install and run Yapf formatter](#51-install-and-run-yapf-formatter)
  * [5.2. Install and run Flake8 linter](#52-install-and-run-flake8-linter)
  * [5.3. Run Tests](#53-run-tests)
- [6. Metrics](#6-metrics)
- [7. Troubleshooting](#7-troubleshooting)

<!-- tocstop -->

-----

## 1. Installation

Install this library in a [virtualenv][1] using pip. [virtualenv][1] is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With [virtualenv][1], it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies. Make sure you use Python 3.6+.


### 1.1. Mac/Linux

```bash
pip3 install virtualenv
virtualenv --python python3.6 <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install google-datacatalog-greenplum-connector
```

### 1.2. Windows

```bash
pip3 install virtualenv
virtualenv --python python3.6 <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-datacatalog-greenplum-connector
```

### 1.3. Install from source

#### 1.3.1. Get the code

````bash
git clone https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/
cd datacatalog-connectors-rdbms/google-datacatalog-greenplum-connector
````

#### 1.3.2. Create and activate a *virtualenv*

```bash
pip3 install virtualenv
virtualenv --python python3.6 <your-env>
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
- `<YOUR-CREDENTIALS_FILES_FOLDER>/greenplum2dc-credentials.json`

> Please notice this folder and file will be required in next steps.

### 2.2 Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file

export GREENPLUM2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export GREENPLUM2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export GREENPLUM2DC_GREENPLUM_SERVER=greenplum_server
export GREENPLUM2DC_GREENPLUM_USERNAME=greenplum_username
export GREENPLUM2DC_GREENPLUM_PASSWORD=greenplum_password
export GREENPLUM2DC_GREENPLUM_DATABASE=greenplum_database
export GREENPLUM2DC_RAW_METADATA_CSV=greenplum_raw_csv (If supplied ignores the GREENPLUM server credentials)

```

## 3. Run entry point

### 3.1. Run Python entry point

- Virtualenv

```bash
google-datacatalog-greenplum-connector \
--datacatalog-project-id=$GREENPLUM2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$GREENPLUM2DC_DATACATALOG_LOCATION_ID \
--greenplum-host=$GREENPLUM2DC_GREENPLUM_SERVER \
--greenplum-user=$GREENPLUM2DC_GREENPLUM_USERNAME \
--greenplum-pass=$GREENPLUM2DC_GREENPLUM_PASSWORD \
--greenplum-database=$GREENPLUM2DC_GREENPLUM_DATABASE \
--raw-metadata-csv=$GREENPLUM2DC_RAW_METADATA_CSV      
```

### 3.2. Run Docker entry point

```bash
docker build -t greenplum2datacatalog .
docker run --rm --tty -v YOUR-CREDENTIALS_FILES_FOLDER:/data greenplum2datacatalog \ --datacatalog-project-id=$GREENPLUM2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$GREENPLUM2DC_DATACATALOG_LOCATION_ID \
--greenplum-host=$GREENPLUM2DC_GREENPLUM_SERVER \
--greenplum-user=$GREENPLUM2DC_GREENPLUM_USERNAME \
--greenplum-pass=$GREENPLUM2DC_GREENPLUM_PASSWORD \
--greenplum-database=$GREENPLUM2DC_GREENPLUM_DATABASE  \
--raw-metadata-csv=$GREENPLUM2DC_RAW_METADATA_CSV       
```

## 4 Scripts inside tools

### 4.1. Run clean up

```bash
# List of projects split by comma. Can be a single value without comma
export GREENPLUM2DC_DATACATALOG_PROJECT_IDS=my-project-1,my-project-2
```

```bash
# Run the clean up
python tools/cleanup_datacatalog.py --datacatalog-project-ids=$TGREENPLUM2DC_DATACATALOG_PROJECT_IDS 

```

### 4.2. Extract CSV

```bash
# Run  inside your greenplum database instance

COPY (
    select t.table_schema as schema_name, t.table_name, t.table_type, c.column_name, c.column_default as column_default_value, c.is_nullable as column_nullable, c.data_type as column_type,
            c.character_maximum_length as column_char_length, c.numeric_precision as column_numeric_precision  
        from information_schema.tables t
            join  information_schema.columns c on c.table_name = t.table_name
        where t.table_schema not in ('pg_catalog', 'information_schema', 'pg_toast', 'gp_toolkit')
            and c.table_schema not in ('pg_catalog', 'information_schema', 'pg_toast', 'gp_toolkit')
    ) 
    TO '/home/gpadmin/greenplum_full_dump.csv'  CSV HEADER;

```

## 5. Developer environment

### 5.1. Install and run Yapf formatter

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

### 5.2. Install and run Flake8 linter

```bash
pip install --upgrade flake8
flake8 src tests
```

### 5.3. Run Tests

```bash
python setup.py test
```

## 6. Metrics

[Metrics README.md](docs/README.md)

## 7. Troubleshooting

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
[3]: https://img.shields.io/pypi/v/google-datacatalog-greenplum-connector.svg
[4]: https://pypi.org/project/google-datacatalog-greenplum-connector/
[5]: https://img.shields.io/github/license/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[6]: https://img.shields.io/github/issues/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[7]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/issues
