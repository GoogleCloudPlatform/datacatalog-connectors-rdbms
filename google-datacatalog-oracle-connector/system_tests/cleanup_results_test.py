#!/usr/bin/python
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

import os
import unittest

from google.cloud import datacatalog

datacatalog_client = datacatalog.DataCatalogClient()


class CleanupResultsTest(unittest.TestCase):

    def test_entries_should_not_exist_after_cleanup(self):
        query = 'system=oracle'

        scope = datacatalog.SearchCatalogRequest.Scope()
        scope.include_project_ids.append(
            os.environ['ORACLE2DC_DATACATALOG_PROJECT_ID'])

        request = datacatalog.SearchCatalogRequest()
        request.scope = scope
        request.query = query
        request.page_size = 1000

        search_results = [
            result for result in datacatalog_client.search_catalog(request)
        ]
        self.assertEqual(len(search_results), 0)

