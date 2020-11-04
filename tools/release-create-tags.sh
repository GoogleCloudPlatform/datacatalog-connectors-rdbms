#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
SETUP_FILENAME="setup.py"
CONNECTOR_NAME_REGEXP="^google-datacatalog-([a-zA-Z]+)-connector$"

release-create-tags::main(){

    if [[ -z "${GITHUB_TOKEN}" ]]; then
        echo "Undefined GITHUB_TOKEN variable"
        release-create-tags::usage
    fi

    echo "START release tagging script"
    echo ""

    for connector_dir in `ls ${CURRENT_DIR} | grep connector`; do
        echo " running on: ${connector_dir}"

        setup_path=${CURRENT_DIR}/${connector_dir}/${SETUP_FILENAME}

        release_version=$(sed -n "s/^ *version=['\'']//p" ${setup_path} | sed -n "s/['\'',]*$//p")

        [[ ${connector_dir} =~ ${CONNECTOR_NAME_REGEXP} ]]
        connector_simple_name="${BASH_REMATCH[1]}"

        echo " tagging ${connector_simple_name} with release version: ${release_version}"

        tag_name="${connector_simple_name}-${release_version}"

        git tag ${tag_name}

        if [[ $? -eq 0 ]]
            then
                echo " tag: ${tag_name} created"
                git_remote_url="$(git remote get-url origin).git"
                git_auth_remote_url="${git_remote_url/github.com/${GITHUB_TOKEN}@github.com}"
                git push ${git_auth_remote_url} ${tag_name}
                echo " tag: ${tag_name} pushed!"
            else
                echo " tag: ${tag_name} failed!"
        fi

        echo ""
    done

    echo 'END release tagging script'
}

release-create-tags::usage(){
  echo 'SET: "GITHUB_TOKEN" environment variable'
  exit 2
}

release-create-tags::main "$@"