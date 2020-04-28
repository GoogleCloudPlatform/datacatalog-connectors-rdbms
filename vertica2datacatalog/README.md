# vertica2datacatalog

Package for ingesting Vertica metadata into Google Cloud Data Catalog.

**Disclaimer: This is not an officially supported Google product.**

## 1. Environment setup

### 1.1. Get the code

````bash
git clone https://.../vertica2datacatalog.git
cd vertica2datacatalog
````

### 1.2. Auth credentials

##### 1.2.1. Create a service account and grant it below roles

- Data Catalog Admin

##### 1.2.2. Download a JSON key and save it as
- `<YOUR-CREDENTIALS_FILES_FOLDER>/vertica2dc-datacatalog-credentials.json`

**Please notice this folder and file will be required in next steps.**

### 1.3. Virtualenv

Using *virtualenv* is optional, but strongly recommended unless you use Docker
or a PEX file.

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
pip install ./lib/rdbms2datacatalog-1.0.0-py2.py3-none-any.whl
pip install --editable .
```

##### 1.3.4. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file
```

### 1.4. Docker

See instructions below.

## 2. Sample application entry point

### 2.1. Run the vertica2datacatalog script

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

- Or using Docker

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

## 3. Troubleshooting

In the case a connector execution hits Data Catalog quota limit, an error will be raised and logged with the following detailement, depending on the performed operation READ/WRITE/SEARCH: 
```
status = StatusCode.RESOURCE_EXHAUSTED
details = "Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'."
debug_error_string = 
"{"created":"@1587396969.506556000", "description":"Error received from peer ipv4:172.217.29.42:443","file":"src/core/lib/surface/call.cc","file_line":1056,"grpc_message":"Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'.","grpc_status":8}"
```
For more info about Data Catalog quota, go to: [Data Catalog quota docs](https://cloud.google.com/data-catalog/docs/resources/quotas).