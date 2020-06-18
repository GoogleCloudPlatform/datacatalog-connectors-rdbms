# google-datacatalog-vertica-connector

Package for ingesting Vertica metadata into Google Cloud Data Catalog.

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
- [3. Run entry point](#3-run-entry-point)
  * [3.1. Run Python entry point](#31-run-python-entry-point)
  * [3.2. Run Docker entry point](#32-run-docker-entry-point)
- [4. Developer environment](#4-developer-environment)
  * [4.1. Install and run Yapf formatter](#41-install-and-run-yapf-formatter)
  * [4.2. Install and run Flake8 linter](#42-install-and-run-flake8-linter)
  * [4.3. Run Tests](#43-run-tests)
- [5. Troubleshooting](#5-troubleshooting)

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
<your-env>/bin/pip install google-datacatalog-vertica-connector
```

### 1.2. Windows

```bash
pip3 install virtualenv
virtualenv --python python3.6 <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-datacatalog-vertica-connector
```

### 1.3. Install from source

#### 1.3.1. Get the code

````bash
git clone https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/
cd datacatalog-connectors-rdbms/google-datacatalog-vertica-connector
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
- `<YOUR-CREDENTIALS_FILES_FOLDER>/vertica2dc-datacatalog-credentials.json`

**Please notice this folder and file will be required in next steps.**

### 2.2. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file
```

## 3. Run entry point

### 3.1. Run Python entry point

- Virtualenv

Connect to a server:

```bash
vertica2datacatalog \
  --vertica-host <VERTICA-HOST-IP> \
  --vertica-user <VERTICA-USER> \
  --vertica-pass <VERTICA-PASSWORD> \
  --datacatalog-project-id <YOUR-DATACATALOG-PROJECT-ID> \
  --datacatalog-location-id <YOUR-DATACATALOG-LOCATION-ID>
```

Read metadata from a CSV file:

```bash
vertica2datacatalog \
  --raw-metadata-csv <PATH-TO-A-FULL-DUMP-CSV-FILE> \
  --datacatalog-project-id <YOUR-DATACATALOG-PROJECT-ID> \
  --datacatalog-location-id <YOUR-DATACATALOG-LOCATION-ID>
```

### 3.2. Run Docker entry point

```bash
docker build --rm --tag vertica2datacatalog .
```

Connect to a server:

```bash
docker run --rm --tty -v <YOUR-CREDENTIALS_FILES_FOLDER>:/data \
  vertica2datacatalog \ 
  --vertica-host <VERTICA-HOST-IP> \
  --vertica-user <VERTICA-USER> \
  --vertica-pass <VERTICA-PASSWORD> \
  --datacatalog-project-id <YOUR-DATACATALOG-PROJECT-ID> \
  --datacatalog-location-id <YOUR-DATACATALOG-LOCATION-ID>
```

Read metadata from a CSV file:

```bash
docker run --rm --tty -v <YOUR-CREDENTIALS_FILES_FOLDER>:/data \
  vertica2datacatalog \ 
  --raw-metadata-csv /data/<PATH-TO-A-FULL-DUMP-CSV-FILE> \
  --datacatalog-project-id <YOUR-DATACATALOG-PROJECT-ID> \
  --datacatalog-location-id <YOUR-DATACATALOG-LOCATION-ID>
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

[1]: https://virtualenv.pypa.io/en/latest/
[2]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/workflows/Python%20package/badge.svg?branch=master
[3]: https://img.shields.io/pypi/v/google-datacatalog-vertica-connector.svg
[4]: https://pypi.org/project/google-datacatalog-vertica-connector/
[5]: https://img.shields.io/github/license/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[6]: https://img.shields.io/github/issues/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[7]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/issues