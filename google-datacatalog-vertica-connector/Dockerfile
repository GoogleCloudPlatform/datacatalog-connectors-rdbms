# docker build -t vertica2datacatalog .
FROM python:3.6 as builder

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
# At run time, /data must be binded to a volume containing a valid Service
# Account credentials file named vertica2dc-datacatalog-credentials.json.
ENV GOOGLE_APPLICATION_CREDENTIALS=/data/vertica2dc-datacatalog-credentials.json

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

# QUALITY ASSURANCE
FROM builder as qa

# Run static code checks.
RUN pip install flake8 yapf
RUN yapf --diff --recursive src tests
RUN flake8 src tests

# Install the connector from source files.
RUN pip install .

# Run the unit tests.
RUN python setup.py test
# END OF QUALITY ASSURANCE STEPS

# RESUME THE IMAGE BUILD PROCESS
FROM builder as run

# Install the connector from source files.
RUN pip install .

ENTRYPOINT ["google-datacatalog-vertica-connector"]
