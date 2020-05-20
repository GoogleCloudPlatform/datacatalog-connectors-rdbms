# rdbmscsv2datacatalog

Library for ingesting a CSV metadata extraction from a RDBMS into Google Cloud Data Catalog.

**Disclaimer: This is not an officially supported Google product.**

<!--
  ⚠️ DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY ️️⚠️
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

## Table of Contents

<!-- toc -->

- [1. Environment setup](#1-environment-setup)
  * [1.1. Get the code](#11-get-the-code)
  * [1.2. Auth credentials](#12-auth-credentials)
      - [1.2.1. Create a service account and grant it below roles](#121-create-a-service-account-and-grant-it-below-roles)
      - [1.2.2. Download a JSON key and save it as](#122-download-a-json-key-and-save-it-as)
  * [1.3. Virtualenv](#13-virtualenv)
      - [1.3.1. Install Python 3.6+](#131-install-python-36)
      - [1.3.2. Create and activate a *virtualenv*](#132-create-and-activate-a-virtualenv)
      - [1.3.3. Install the dependencies](#133-install-the-dependencies)
      - [1.3.5. Set environment variables](#135-set-environment-variables)
  * [1.4. Docker](#14-docker)
- [2. Sample application entry point](#2-sample-application-entry-point)
  * [2.1. Run main.py](#21-run-mainpy)
- [3 Scripts inside tools](#3-scripts-inside-tools)
  * [3.1. Run clean up](#31-run-clean-up)
- [4. Developer environment](#4-developer-environment)
  * [4.1. Install and run Yapf formatter](#41-install-and-run-yapf-formatter)
  * [4.2. Install and run Flake8 linter](#42-install-and-run-flake8-linter)
  * [4.3. Run Tests](#43-run-tests)
- [5. Troubleshooting](#5-troubleshooting)

<!-- tocstop -->

-----

## 1. Environment setup

### 1.1. Get the code

````bash
git clone https://.../rdbmscsv2datacatalog.git
cd rdbmscsv2datacatalog
````

### 1.2. Auth credentials

##### 1.2.1. Create a service account and grant it below roles

- Data Catalog Admin

##### 1.2.2. Download a JSON key and save it as
- `<YOUR-CREDENTIALS_FILES_FOLDER>/rdbmscsv2dc-credentials.json`

> Please notice this folder and file will be required in next steps.

### 1.3. Virtualenv

Using *virtualenv* is optional, but strongly recommended unless you use Docker or a PEX file.

##### 1.3.1. Install Python 3.6+

##### 1.3.2. Create and activate a *virtualenv*

```bash
pip install --upgrade virtualenv
virtualenv --python python3 env
source ./env/bin/activate
```

##### 1.3.3. Install the dependencies

```bash
pip install ./lib/datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl
pip install ./lib/rdbms2datacatalog-1.0.0-py2.py3-none-any.whl
pip install --editable .
```

##### 1.3.5. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file

export RDBMS2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export RDBMS2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export RDBMS2DC_SERVER=rdbms_server
export RDBMS2DC_TYPE=oracle
export RDBMS2DC_RAW_METADATA_CSV=rdms_raw_csv

```

### 1.4. Docker

See instructions below.

## 2. Sample application entry point

### 2.1. Run main.py

- Virtualenv

```bash
rdbmscsv2datacatalog \
--datacatalog-project-id=$RDBMS2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$RDBMS2DC_DATACATALOG_LOCATION_ID \
--rdbms-host=$RDBMS2DC_SERVER \
--rdbms-type=$RDBMS2DC_TYPE \
--raw-metadata-csv=$RDBMS2DC_RAW_METADATA_CSV
```

- Or using Docker

```bash
docker build -t rdbmscsv2datacatalog .
docker run --rm --tty -v YOUR-CREDENTIALS_FILES_FOLDER:/data rdbmscsv2datacatalog \
--datacatalog-project-id=$RDBMS2DC_DATACATALOG_PROJECT_ID  \
--datacatalog-location-id=$RDBMS2DC_DATACATALOG_LOCATION_ID \
--rdbms-host=$RDBMS2DC_SERVER \
--rdbms-type=$RDBMS2DC_TYPE \
--raw-metadata-csv=$RDBMS2DC_RAW_METADATA_CSV
```

## 3 Scripts inside tools

### 3.1. Run clean up

```bash
# List of projects split by comma. Can be a single value without comma
export RDBMS_DATACATALOG_PROJECT_IDS=my-project-1,my-project-2
export RDBMS2DC_TYPE=oracle
```

```bash
# Run the clean up
python tools/cleanup_datacatalog.py \
--datacatalog-project-ids=$RDBMS_DATACATALOG_PROJECT_IDS \
--rdbms-type=$RDBMS2DC_TYPE
```

## 4. Developer environment

### 4.1. Install and run Yapf formatter

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

### 4.2. Install and run Flake8 linter

```bash
pip install --upgrade flake8
flake8 src tests
```

### 4.3. Run Tests

```bash
pip install ./lib/datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl
pip install pytest mock
python setup.py test
```

## 5. Troubleshooting

In the case a connector execution hits Data Catalog quota limit, an error will be raised and logged with the following detailement, depending on the performed operation READ/WRITE/SEARCH: 
```
status = StatusCode.RESOURCE_EXHAUSTED
details = "Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'."
debug_error_string = 
"{"created":"@1587396969.506556000", "description":"Error received from peer ipv4:172.217.29.42:443","file":"src/core/lib/surface/call.cc","file_line":1056,"grpc_message":"Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'.","grpc_status":8}"
```
For more info about Data Catalog quota, go to: [Data Catalog quota docs](https://cloud.google.com/data-catalog/docs/resources/quotas).