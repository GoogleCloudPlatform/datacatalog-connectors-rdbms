# postgresql2datacatalog

Library for ingesting PostgreSQL metadata into Google Cloud Data Catalog.

**Disclaimer: This is not an officially supported Google product.**

## 1. Environment setup

### 1.1. Get the code

````bash
git clone https://.../postgresql2datacatalog.git
cd postgresql2datacatalog
````

### 1.2. Auth credentials

##### 1.2.1. Create a service account and grant it below roles

- Data Catalog Admin

##### 1.2.2. Download a JSON key and save it as
- `<YOUR-CREDENTIALS_FILES_FOLDER>/postgresql2dc-credentials.json`

> Please notice this folder and file will be required in next steps.

### 1.3. Virtualenv

Using *virtualenv* is optional, but strongly recommended unless you use Docker or a PEX file.

##### 1.3.1. Install Python 3.6+

##### 1.3.2. Create and activate a *virtualenv*

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

##### 1.3.3. Install the dependencies

```bash
pip install ./lib/datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl
pip install ./lib/rdbms2datacatalog-1.1.0-py2.py3-none-any.whl
pip install --editable .
```

##### 1.3.4. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file

export POSTGRESQL2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export POSTGRESQL2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export POSTGRESQL2DC_POSTGRESQL_SERVER=postgresql_server
export POSTGRESQL2DC_POSTGRESQL_USERNAME=postgresql_username
export POSTGRESQL2DC_POSTGRESQL_PASSWORD=postgresql_password
export POSTGRESQL2DC_POSTGRESQL_DATABASE=postgresql_database
export POSTGRESQL2DC_RAW_METADATA_CSV=postgresql_raw_csv (If supplied ignores the POSTGRESQL server credentials)

```

### 1.4. Docker

See instructions below.

## 2. Sample application entry point

### 2.1. Run main.py

- Virtualenv

```bash
postgresql2datacatalog --datacatalog-project-id=$POSTGRESQL2DC_DATACATALOG_PROJECT_ID --datacatalog-location-id=$POSTGRESQL2DC_DATACATALOG_LOCATION_ID --postgresql-host=$POSTGRESQL2DC_POSTGRESQL_SERVER --postgresql-user=$POSTGRESQL2DC_POSTGRESQL_USERNAME --postgresql-pass=$POSTGRESQL2DC_POSTGRESQL_PASSWORD --postgresql-database=$POSTGRESQL2DC_POSTGRESQL_DATABASE  --raw-metadata-csv=$POSTGRESQL2DC_RAW_METADATA_CSV      
```

- Or using Docker

```bash
docker build -t postgresql2datacatalog .
docker run --rm --tty -v YOUR-CREDENTIALS_FILES_FOLDER:/data postgresql2datacatalog --datacatalog-project-id=$POSTGRESQL2DC_DATACATALOG_PROJECT_ID --datacatalog-location-id=$POSTGRESQL2DC_DATACATALOG_LOCATION_ID --postgresql-host=$POSTGRESQL2DC_POSTGRESQL_SERVER --postgresql-user=$POSTGRESQL2DC_POSTGRESQL_USERNAME --postgresql-pass=$POSTGRESQL2DC_POSTGRESQL_PASSWORD --postgresql-database=$POSTGRESQL2DC_POSTGRESQL_DATABASE  --raw-metadata-csv=$POSTGRESQL2DC_RAW_METADATA_CSV       
```

##### 3. Generate wheel file

```bash
python setup.py bdist_wheel
```

## 4 Scripts inside tools

### 4.1. Run clean up

```bash
# List of projects split by comma. Can be a single value without comma
export POSTGRESQL2DC_DATACATALOG_PROJECT_IDS=my-project-1,my-project-2
```

```bash
# Run the clean up
python tools/cleanup_datacatalog.py --datacatalog-project-ids=$POSTGRESQL2DC_DATACATALOG_PROJECT_IDS 

```

### 4.2. Extract CSV

```bash
# Run  inside your postgresql database instance

COPY (
    select t.table_schema as schema_name, t.table_name, t.table_type, c.column_name, c.column_default as column_default_value, c.is_nullable as column_nullable, c.data_type as column_type,
            c.character_maximum_length as column_char_length, c.numeric_precision as column_numeric_precision  
        from information_schema.tables t
            join  information_schema.columns c on c.table_name = t.table_name
        where t.table_schema not in ('pg_catalog', 'information_schema', 'pg_toast', 'gp_toolkit')
            and c.table_schema not in ('pg_catalog', 'information_schema', 'pg_toast', 'gp_toolkit')
    ) 
    TO '/home/postgre/postgresql_full_dump.csv'  CSV HEADER;

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
pip install ./lib/datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl
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