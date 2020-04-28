# rdbms2datacatalog

Common resources for Data Catalog RDBMS connectors.

**Disclaimer: This is not an officially supported Google product.**

## 1. Installable file build process

### 1.1. Get the code

````bash
git clone https://.../rdbms2datacatalog.git
cd rdbms2datacatalog
````

### 1.2. Virtualenv

Using *virtualenv* is optional, but strongly recommended.

##### 1.2.1. Install Python 3.5

##### 1.2.2. Create and activate a *virtualenv*

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

### 1.3. Generate a *wheel* file

```bash
python setup.py bdist_wheel
```

> The wheel file can used to install the package as a local pip dependency to
> other projects while it's not published to The Python Package Index (PyPI).

## 2. Developer environment

### 2.1. Install local dependencies

```bash
pip install ./lib/datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl
pip install --editable .
```

### 2.2. Install and run YAPF formatter

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

### 2.3. Install and run Flake8 linter

```bash
pip install --upgrade flake8
flake8 src tests
```

### 2.4. Install the package in editable mode (i.e. setuptools “develop mode”)

```bash
pip install --editable .
```

### 2.5. Run the unit tests

```bash
pip install ./lib/datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl
pip install pytest mock
python setup.py test
```

## 3. Setting up the RDBMS conenctor
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