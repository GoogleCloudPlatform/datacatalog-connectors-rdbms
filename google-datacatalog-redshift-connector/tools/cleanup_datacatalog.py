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

import argparse
import logging
import re
import sys

from google.api_core import exceptions
from google.cloud import datacatalog_v1beta1

datacatalog = datacatalog_v1beta1.DataCatalogClient()


def __delete_entries_and_groups(project_ids):
    logging.info('\nStarting to clean up the catalog...')

    query = 'system=redshift'

    scope = datacatalog_v1beta1.types.SearchCatalogRequest.Scope()
    scope.include_project_ids.extend(project_ids)

    search_results = datacatalog.search_catalog(scope=scope,
                                                query=query,
                                                order_by='relevance',
                                                page_size=1000)
    datacatalog_entry_name_pattern = '(?P<entry_group_name>.+?)/entries/(.+?)'

    entry_group_names = []
    for result in search_results:
        try:
            datacatalog.delete_entry(result.relative_resource_name)
            logging.info('Entry deleted: %s', result.relative_resource_name)
            entry_group_name = re.match(
                pattern=datacatalog_entry_name_pattern,
                string=result.relative_resource_name).group('entry_group_name')
            entry_group_names.append(entry_group_name)
        except exceptions.GoogleAPICallError as e:
            logging.warning('Exception deleting entry: %s', str(e))

    # Delete any pre-existing Entry Groups.
    for entry_group_name in set(entry_group_names):
        try:
            datacatalog.delete_entry_group(entry_group_name)
            logging.info('--> Entry Group deleted: %s', entry_group_name)
        except exceptions.GoogleAPICallError as e:
            logging.warning('Exception deleting entry group: %s', str(e))


def __delete_tag_templates(project_id, location_id):
    tag_template_id = 'redshift_schema_metadata'

    try:
        datacatalog.delete_tag_template(
            datacatalog_v1beta1.DataCatalogClient.tag_template_path(
                project=project_id,
                location=location_id,
                tag_template=tag_template_id),
            force=True)
        logging.info('--> Tag Template deleted: %s', tag_template_id)
    except exceptions.GoogleAPICallError as e:
        logging.warning('Exception deleting Tag Template: %s', str(e))

    tag_template_id = 'redshift_table_metadata'

    try:
        datacatalog.delete_tag_template(
            name=datacatalog_v1beta1.DataCatalogClient.tag_template_path(
                project=project_id,
                location=location_id,
                tag_template=tag_template_id),
            force=True)
        logging.info('--> Tag Template deleted: %s', tag_template_id)
    except exceptions.GoogleAPICallError as e:
        logging.warning('Exception deleting Tag Template: %s', str(e))


def __parse_args():
    parser = argparse.ArgumentParser(description='Command line to clean up all'
                                     ' Redshift metadata on Datacatalog')

    parser.add_argument(
        '--datacatalog-project-ids',
        help='List of Google Cloud project IDs split by comma, '
        'At least one must be specified',
        required=True)
    parser.add_argument(
        '--datacatalog-location-id',
        help='Location id which is the Region that your Datacatalog resides',
        default='us-central1')
    return parser.parse_args()


if __name__ == '__main__':
    args = __parse_args()

    # Enable logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Split multiple values separated by comma.
    datacatalog_project_ids = args.datacatalog_project_ids.split(',')

    __delete_entries_and_groups(datacatalog_project_ids)
    for datacatalog_project_id in datacatalog_project_ids:
        __delete_tag_templates(datacatalog_project_id,
                               args.datacatalog_location_id)
    logging.info('\nFinished to clean up the catalog')
