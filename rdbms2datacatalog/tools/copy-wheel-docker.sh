#!/usr/bin/env bash
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The first sed command returns "1.1.0'," (or a newest version number).
# The second sed command removes "'," from previous result.
VERSION=$(sed -n 's/^ *version=['\'']//p' setup.py | sed -n 's/['\'',]*$//p')

docker build --rm --tag rdbms2datacatalog .
docker create --name dc-rdbms-commons-wheel rdbms2datacatalog
mkdir -p dist
docker cp dc-rdbms-commons-wheel:/app/dist/rdbms2datacatalog-"$VERSION"-py2.py3-none-any.whl ./dist/.
docker rm -fv dc-rdbms-commons-wheel