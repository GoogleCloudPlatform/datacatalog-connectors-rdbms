# google-datacatalog-oracle-connector

Library for ingesting Oracle metadata into Google Cloud Data Catalog.

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
  * [2.2 Set up Oracle Driver (Optional)](#22-set-up-oracle-driver--optional)
    + [2.2.1 Set Oracle client for Linux (Cloud Shell)](#221-set-oracle-client-for-linux-cloud-shell)
    + [2.2.2 Set Oracle client for Mac](#222--set-oracle-client-for-mac)
  * [2.3. Set environment variables](#23-set-environment-variables)
- [3. Run entry point](#3-run-entry-point)
  * [3.1. Run Python entry point](#31-run-python-entry-point)
  * [3.2. Run Docker entry point](#32-run-docker-entry-point)
- [4 Scripts inside tools](#4-scripts-inside-tools)
  * [4.1. Run clean up](#41-run-clean-up)
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
<your-env>/bin/pip install google-datacatalog-oracle-connector
```

### 1.2. Windows

```bash
pip3 install virtualenv
virtualenv --python python3.6 <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-datacatalog-oracle-connector
```

### 1.3. Install from source

#### 1.3.1. Get the code

````bash
git clone https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/
cd datacatalog-connectors-rdbms/google-datacatalog-oracle-connector
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
- `<YOUR-CREDENTIALS_FILES_FOLDER>/oracle2dc-datacatalog-credentials.json`

> Please notice this folder and file will be required in next steps.

### 2.2 Set up Oracle Driver  (Optional)
This is step is needed when you are running the connector on a machine that does not have the Oracle installation.

#### 2.2.1 Set Oracle client for Linux (Cloud Shell)
Download the zip file:
https://oracle.github.io/odpi/doc/installation.html#linux

```bash
# Unzip it
unzip instantclient-basic-linux.x64-19.5.0.0.0dbru.zip
# Set Oracle library ENV Var on the unzip dir
export LD_LIBRARY_PATH=/oracle2datacatalog/bin/instantclient_19_5
```

#### 2.2.2  Set Oracle client for Mac
Download the zip file:
https://oracle.github.io/odpi/doc/installation.html#macos

```bash
# Unzip it
unzip instantclient-basic-macos.x64-19.3.0.0.0dbru.zip
# Set Oracle library ENV Var on the unzip dir
export LD_LIBRARY_PATH=/oracle2datacatalog/bin/instantclient_19_3
```

### 2.3. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file

export ORACLE2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export ORACLE2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export ORACLE2DC_ORACLE_SERVER=oracle_server
export ORACLE2DC_ORACLE_SERVER_PORT=oracle_server_port
export ORACLE2DC_ORACLE_USERNAME=oracle_username
export ORACLE2DC_ORACLE_PASSWORD=oracle_password
export ORACLE2DC_ORACLE_DATABASE_SERVICE=oracle_db_service
export ORACLE2DC_RAW_METADATA_CSV=oracle_raw_csv (If supplied ignores the Oracle server credentials)

```

## 3. Run entry point

### 3.1. Run Python entry point

- Virtualenv

```bash
google-datacatalog-oracle-connector \
--datacatalog-project-id=$ORACLE2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$ORACLE2DC_DATACATALOG_LOCATION_ID \
--oracle-host=$ORACLE2DC_ORACLE_SERVER \
--oracle-port=$ORACLE2DC_ORACLE_SERVER_PORT \
--oracle-user=$ORACLE2DC_ORACLE_USERNAME \
--oracle-pass=$ORACLE2DC_ORACLE_PASSWORD \
--oracle-db-service=$ORACLE2DC_ORACLE_DATABASE_SERVICE \
--raw-metadata-csv=$ORACLE2DC_RAW_METADATA_CSV
```

### 3.2. Run Docker entry point

```bash
docker build -t oracle2datacatalog .
docker run --rm --tty -v YOUR-CREDENTIALS_FILES_FOLDER:/data oracle2datacatalog \
--datacatalog-project-id=$ORACLE2DC_DATACATALOG_PROJECT_ID  \
--datacatalog-location-id=$ORACLE2DC_DATACATALOG_LOCATION_ID \
--oracle-host=$ORACLE2DC_ORACLE_SERVER \
--oracle-port=$ORACLE2DC_ORACLE_SERVER_PORT  \
--oracle-user=$ORACLE2DC_ORACLE_USERNAME \
--oracle-pass=$ORACLE2DC_ORACLE_PASSWORD \
--oracle-db-service=$ORACLE2DC_ORACLE_DATABASE_SERVICE \
--raw-metadata-csv=$ORACLE2DC_RAW_METADATA_CSV
```

## 4 Scripts inside tools

### 4.1. Run clean up

```bash
# List of projects split by comma. Can be a single value without comma
export ORACLE2DC_DATACATALOG_PROJECT_IDS=my-project-1,my-project-2
```

```bash
# Run the clean up
python tools/cleanup_datacatalog.py --datacatalog-project-ids=$ORACLE2DC_DATACATALOG_PROJECT_IDS 

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
[3]: https://img.shields.io/pypi/v/google-datacatalog-oracle-connector.svg
[4]: https://pypi.org/project/google-datacatalog-oracle-connector/
[5]: https://img.shields.io/github/license/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[6]: https://img.shields.io/github/issues/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[7]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/issues