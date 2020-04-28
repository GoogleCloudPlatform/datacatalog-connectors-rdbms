# docker build -t oracle2datacatalog .
FROM python:3.7

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
# At run time, /data must be binded to a volume containing a valid Service Account credentials file
# named oracle2dc-credentials.json.
ENV GOOGLE_APPLICATION_CREDENTIALS=/data/oracle2dc-credentials.json
ENV ORACLE_HOME=/opt/oracle/instantclient_19_5
ENV LD_LIBRARY_PATH=$ORACLE_HOME
ENV LD_RUN_PATH=$ORACLE_HOME

RUN curl https://download.oracle.com/otn_software/linux/instantclient/195000/instantclient-basic-linux.x64-19.5.0.0.0dbru.zip > instantclient-basic-linux.x64-19.5.0.0.0dbru.zip
RUN mkdir -p /opt/oracle && \
unzip "instantclient*.zip" -d /opt/oracle && \
ln -s $ORACLE_HOME 

RUN apt-get update \
 && apt-get install libaio1 -y 

# Copy the local client library dependency and install it (temporary).
WORKDIR /lib
COPY ./lib/datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl .
RUN pip install datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl

COPY ./lib/rdbms2datacatalog-1.0.0-py2.py3-none-any.whl .
RUN pip install rdbms2datacatalog-1.0.0-py2.py3-none-any.whl

COPY ./lib/datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl .
RUN pip install datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl

RUN pip install flake8
RUN pip install yapf

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

RUN yapf --diff --recursive src tests
RUN flake8 src tests

RUN python setup.py test

# Install oracle2datacatalog package from source files.
RUN pip install .


ENTRYPOINT ["oracle2datacatalog"]
