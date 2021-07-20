"""
Entry point for the status subcommand.

(C) Copyright 2019-2021 Hewlett Packard Enterprise Development LP.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
from collections import OrderedDict
import logging

from sat.apiclient import APIError, HSMClient
from sat.config import get_config_value
from sat.constants import MISSING_VALUE
from sat.report import Report
from sat.session import SATSession
from sat.xname import XName

API_KEYS_TO_HEADERS = OrderedDict([
    ('ID', 'xname'),
    ('Type', 'Type'),
    ('NID', 'NID'),
    ('State', 'State'),
    ('Flag', 'Flag'),
    ('Enabled', 'Enabled'),
    ('Arch', 'Arch'),
    ('Class', 'Class'),
    ('Role', 'Role'),
    ('SubRole', 'Subrole'),
    ('NetType', 'Net Type')
])

LOGGER = logging.getLogger(__name__)


class UsageError(Exception):
    pass


def make_raw_table(components):
    """Obtains node status from a list of components.

    Args:
        components (list): A list of dictionaries representing the components
            in the system along with information about their state.

    Returns:
        A list-of-lists table of strings, each row representing
        the status of a node.
    """
    def get_component_value(component, api_key):
        value = component.get(api_key, MISSING_VALUE)
        if api_key == 'ID' and value != MISSING_VALUE:
            value = XName(value)
        elif all([api_key == 'SubRole', value == MISSING_VALUE, component.get('Role') == 'Compute']):
            # For SubRole, some types of nodes (specifically Compute nodes) are expected to
            # not have a SubRole, so 'None' looks a little more appropriate.
            value = 'None'
        return value

    return [[get_component_value(component, api_key) for api_key in API_KEYS_TO_HEADERS]
            for component in components]


def do_status(args):
    """Displays node status.

    Results are sorted by the "sort_column" member of args, which defaults
    to xname. xnames are tokenized for the purposes of sorting, so that their
    numeric elements are sorted by their value, not lexicographically. Sort
    order is reversed if the "reverse" member of args is True.

    Args:
        args: The argparse.Namespace object containing the parsed arguments
            passed to this subcommand.

    Returns:
        None

    Raises:
        UsageError: if an argument is invalid
    """
    api_client = HSMClient(SATSession())
    if 'all' in args.types:
        args.types = []

    try:
        response = api_client.get('State', 'Components', params={'type': args.types})
    except APIError as err:
        LOGGER.error('Request to HSM API failed: %s', err)
        raise SystemExit(1)

    try:
        response_json = response.json()
    except ValueError as err:
        LOGGER.error('Failed to parse JSON from component state response: %s', err)
        raise SystemExit(1)

    try:
        components = response_json['Components']
    except KeyError as err:
        LOGGER.error("Key '%s' not present in API response JSON.", err)
        raise SystemExit(1)

    raw_table = make_raw_table(components)
    report = Report(
        list(API_KEYS_TO_HEADERS.values()), None,
        args.sort_by, args.reverse,
        get_config_value('format.no_headings'),
        get_config_value('format.no_borders'),
        filter_strs=args.filter_strs,
        display_headings=args.fields,
        print_format=args.format)

    report.add_rows(raw_table)

    print(report)
