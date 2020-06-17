# google-datacatalog-rdbms-connector

Common resources for Data Catalog RDBMS connectors.

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
- [2. Install from source](#2-install-from-source)
  * [2.1. Get the code](#21-get-the-code)
  * [2.2. Virtualenv](#22-virtualenv)
      - [2.2.1. Install Python 3.6](#221-install-python-36)
      - [2.2.2. Create and activate a *virtualenv*](#222-create-and-activate-a-virtualenv)
      - [2.2.3. Install](#223-install)
- [3. Developer environment](#3-developer-environment)
  * [3.1. Install and run YAPF formatter](#31-install-and-run-yapf-formatter)
  * [3.2. Install and run Flake8 linter](#32-install-and-run-flake8-linter)
  * [3.3. Install the package in editable mode (i.e. setuptools “develop mode”)](#33-install-the-package-in-editable-mode-ie-setuptools-develop-mode)
  * [3.4. Run the unit tests](#34-run-the-unit-tests)
- [4. Setting up the RDBMS on a new connector](#4-setting-up-the-rdbms-on-a-new-connector)

<!-- tocstop -->

-----

## 1. Installation

Install this library in a [virtualenv][1] using pip. [virtualenv][1] is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With [virtualenv][1], it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.


### 1.1. Mac/Linux

```bash
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install google-datacatalog-rdbms-connector
```


### 1.2. Windows

```bash
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-datacatalog-rdbms-connector
```

## 2. Install from source

### 2.1. Get the code

````bash
git clone https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/
cd google-datacatalog-rdbms-connector
````

### 2.2. Virtualenv

Using *virtualenv* is optional, but strongly recommended.

##### 2.2.1. Install Python 3.6

##### 2.2.2. Create and activate a *virtualenv*

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

##### 2.2.3. Install

```bash
pip install .
```

## 3. Developer environment

### 3.1. Install and run YAPF formatter

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

### 3.2. Install and run Flake8 linter

```bash
pip install --upgrade flake8
flake8 src tests
```

### 3.3. Install the package in editable mode (i.e. setuptools “develop mode”)

```bash
pip install --editable .
```

### 3.4. Run the unit tests

```bash
python setup.py test
```

## 4. Setting up the RDBMS on a new connector
To set up the RDBMS connector to work with a Relational Database 3 files are needed.
* `metadata_definition.json`
* `metadata_query.sql`
* Extending the `metadata_scraper` class and implementing your rdbms connection method: `_create_rdbms_connection`

for the metadata_definition file your have fields available for 3 levels:
* `table_container_def`
* `table_def`
* `column_def`

If you want working examples please take a look at the already implemented connectors for: Oracle, Teradata, MySQL,
PostgreSQL, Greenplum, Redshift and SQLServer.

For the `metadata_defition` target fields you have the following options as `target`:

| Level               | Target          | Description                                 | Mandatory | 
| ---                 | ---             | ---                                         | ---       | 
| table_container_def | **creator**     | Creator of the Table Container.             |  N        |
| table_container_def | **owner**       | Owner of the Table Container.               |  N        | 
| table_container_def | **update_user** | Last user that updated the Table Container. |  N        | 
| table_container_def | **desc**        | Table Container Description.                |  N        | 
| table_def           | **num_rows**    | Number of rows contained in the Table.      |  N        | 
| table_def           | **creator**     | Creator of the Table.                       |  N        | 
| table_def           | **owner**       | Owner of the Table.                         |  N        | 
| table_def           | **update_user** | Last user that updated the Table.           |  N        | 
| table_def           | **desc**        | Table Description.                          |  N        | 


If those fields are configured they will be used to create Tags.


For columns they are used to create the Data Catalog Entry schema, two `target` fields are used:

| Level      | Target   | Description         | Mandatory | 
| ---        | ---      | ---                 | ---       |  
| column_def | **type** | Column type.        |  Y        | 
| column_def | **desc** | Column description. |  N        |


[1]: https://virtualenv.pypa.io/en/latest/