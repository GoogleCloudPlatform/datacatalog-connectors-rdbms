# docker build -t postgresql2datacatalog .
FROM python:3.7

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
# At run time, /data must be binded to a volume containing a valid Service Account credentials file
# named postgresql2dc-credentials.json.
ENV GOOGLE_APPLICATION_CREDENTIALS=/data/postgresql2dc-credentials.json

# Copy the local client library dependency and install it (temporary).
WORKDIR /lib

RUN pip install flake8
RUN pip install yapf

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

RUN pip install .

RUN yapf --diff --recursive src tests
RUN flake8 src tests

RUN python setup.py test

# Install google-datacatalog-postgresql-connector package from source files.
RUN python setup.py bdist_wheel --universal

RUN pip install dist/google_datacatalog_postgresql_connector-0.5.0-py2.py3-none-any.whl

ENTRYPOINT ["google-datacatalog-postgresql-connector"]
