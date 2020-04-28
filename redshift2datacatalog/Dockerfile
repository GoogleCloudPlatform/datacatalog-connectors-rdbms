# docker build -t redshift2datacatalog .
FROM python:3.7

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
# At run time, /data must be binded to a volume containing a valid Service Account credentials file
# named redshift2dc-credentials.json.
ENV GOOGLE_APPLICATION_CREDENTIALS=/data/redshift2dc-credentials.json

# Copy the local client library dependency and install it (temporary).
WORKDIR /lib

COPY ./lib/datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl .
RUN pip install datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl

COPY ./lib/rdbms2datacatalog-1.0.0-py2.py3-none-any.whl .
RUN pip install rdbms2datacatalog-1.0.0-py2.py3-none-any.whl

COPY ./lib/datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl .
RUN pip install datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl

COPY ./lib/postgresql2datacatalog-1.0.0-py2.py3-none-any.whl .
RUN pip install postgresql2datacatalog-1.0.0-py2.py3-none-any.whl

RUN pip install flake8
RUN pip install yapf

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

RUN yapf --diff --recursive src tests
RUN flake8 src tests

RUN python setup.py test

# Install redshift2datacatalog package from source files.
RUN pip install .

ENTRYPOINT ["redshift2datacatalog"]
