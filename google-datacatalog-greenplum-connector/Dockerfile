# docker build -t greenplum2datacatalog .
FROM python:3.7

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
# At run time, /data must be binded to a volume containing a valid Service Account credentials file
# named greenplum2dc-credentials.json.
ENV GOOGLE_APPLICATION_CREDENTIALS=/data/greenplum2dc-credentials.json

# Copy the local client library dependency and install it (temporary).
WORKDIR /lib

RUN pip install flake8
RUN pip install yapf

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

RUN yapf --diff --recursive src tests
RUN flake8 src tests

# Install google-datacatalog-greenplum-connector package from source files.
RUN pip install .

RUN python setup.py test

ENTRYPOINT ["google-datacatalog-greenplum-connector"]
