#!/usr/bin/env bash

CURRENT_DIR=$(pwd)

publish-current-versions-pypi::main(){

    if [[ -z "${PYPI_DATACATALOG_MAINTAINER_USERNAME}" ]]; then
        publish-current-versions-pypi::usage
    fi

    if [[ -z "${PYPI_DATACATALOG_MAINTAINER_PASSWORD}" ]]; then
        publish-current-versions-pypi::usage
    fi

    echo "START publish to pypi current versions script"
    echo ""

    # Ignore error message if dir does not exist
    rm -rf publish_pypi_env 2> /dev/null || echo > /dev/null

    virtualenv publish_pypi_env --python python3

    source publish_pypi_env/bin/activate

    pip install twine

    for connector_dir in `ls ${CURRENT_DIR} | grep connector`; do
        cd ${CURRENT_DIR}/${connector_dir}
        echo " running on: ${connector_dir}"

        rm -rf dist && \
        python3 setup.py sdist bdist_wheel --universal && \
        twine upload dist/* \
        -u ${PYPI_DATACATALOG_MAINTAINER_USERNAME} \
        -p ${PYPI_DATACATALOG_MAINTAINER_PASSWORD}

        if [[ $? -eq 0 ]]
            then
                echo " ${connector_dir} published to PyPI!"
            else
                echo " ${connector_dir} publishing failed!"
        fi

        echo ""
    done

    echo "END publish to pypi current versions script"
}

publish-current-versions-pypi::usage(){
  echo 'Please set the "PYPI_DATACATALOG_MAINTAINER_USERNAME" and "PYPI_DATACATALOG_MAINTAINER_PASSWORD" environment variables before running this script'
  exit 2
}

publish-current-versions-pypi::main "$@"