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

import unittest

from . import test_utils
import mock


@mock.patch('google.datacatalog_connectors.rdbms.sync.'
            'datacatalog_synchronizer.DataCatalogSynchronizer.__init__',
            lambda self, **kargs: None)
class DatacatalogCLITestCase(unittest.TestCase):

    @mock.patch('google.datacatalog_connectors.rdbms.sync.'
                'datacatalog_synchronizer.DataCatalogSynchronizer.run')
    def test_datacatalog_cli_run_should_not_raise_error(self, run):  # noqa

        cli = test_utils.FakeCLI()

        cli.run({})

        self.assertEqual(run.call_count, 1)
