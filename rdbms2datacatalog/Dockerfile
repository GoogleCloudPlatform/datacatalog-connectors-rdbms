# docker build -t rdbms2datacatalog .
FROM python:3.5 as builder

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .
# This line fixes the importlib-metadata library
RUN pip install virtualenv

# QUALITY ASSURANCE
FROM builder as qa

# Run static code checks.
RUN pip install flake8 yapf
RUN yapf --diff --recursive src tests
RUN flake8 src tests

RUN pip install ./lib/datacatalog_connectors_commons-1.0.0-py2.py3-none-any.whl
RUN pip install ./lib/datacatalog_connectors_commons_test-1.0.0-py2.py3-none-any.whl

# Run the unit tests.
RUN pip install pytest mock pytest-cov
RUN python setup.py test
# END OF QUALITY ASSURANCE STEPS


# RESUME THE IMAGE BUILD PROCESS
FROM builder as run

# Generate a wheel file
RUN python setup.py bdist_wheel --universal
