"""
Unit tests for the sat.sat.cli.setrev.main functions.

Copyright 2019-2020 Cray Inc. All Rights Reserved.
"""


from datetime import datetime
import os
import os.path
import unittest
from unittest import mock
from argparse import Namespace

import sat.cli.setrev.main


samples = os.path.join(os.path.dirname(__file__), 'samples')


# Helpers for mock-decorations.

class InputDict(dict):
    """For help with mocking the input builtin.

    When tests in this file mock input, they do it by replacing it with a
    lambda that points to a global instance of InputDict, which finds a field
    that is a substring of the prompt to input.
    """
    def __getitem__(self, super_):
        """Find first value whose key is in super_.

        Args:
            super_: A string that should contain one of the keys as a
                substring.

        Returns:
            Value if its key is a substring of super_.
            Returns empty string if no match.
        """

        for key, val in self.items():
            if key in super_:
                return val

        return ''


full = InputDict({
    'Serial number': '1234',
    'Site name': 'site name',
    'System name': 'system name',
    'System install date': '1993-05-07',
    'System type': 'fire type'})

empty_date = InputDict({
    'Serial number': '1234',
    'Site name': 'site name',
    'System name': 'system name',
    'System install date': '',
    'System type': 'fire type'})

empty_input = InputDict({})


class TestSetrev(unittest.TestCase):

    def test_is_valid_date_empty_string(self):
        """is_valid_date should return True on empty string.
        """
        self.assertTrue(sat.cli.setrev.main.is_valid_date(''))

    def test_is_valid_date_good_format(self):
        """is_valid_date should return True if format matches YYYY-mm-dd.
        """
        self.assertTrue(sat.cli.setrev.main.is_valid_date('2019-08-10'))

    def test_is_valid_date_bad_dates(self):
        """is_valid_date should not accept invalid dates.
        """
        self.assertFalse(sat.cli.setrev.main.is_valid_date('2019-13-10'))
        self.assertFalse(sat.cli.setrev.main.is_valid_date('2019-08-32'))

    def test_get_site_data_good_file(self):
        """get_site_data should return a dict after reading valid yaml.
        """
        path = '{}/good.yml'.format(samples)
        d = sat.cli.setrev.main.get_site_data(path)

        self.assertEqual(d['Serial number'], '12345shasdf')
        self.assertEqual(d['Site name'], 'site-name-with-spaces')
        self.assertEqual(d['System name'], 'my-sys')
        self.assertEqual(d['System install date'], '2019-10-08')
        self.assertEqual(d['System type'], 'fire-type')

    def test_get_site_data_only_strings(self):
        """The dict returned by get_site_data should only contain str types.
        """
        path = '{}/good.yml'.format(samples)
        d = sat.cli.setrev.main.get_site_data(path)

        for key, value in d.items():
            self.assertEqual(type(value), str)

    def test_get_site_data_file_not_found(self):
        """get_site_data should return empty dict if file doesn't exist.
        """
        path = 'idontexist.yml'
        d = sat.cli.setrev.main.get_site_data(path)
        self.assertEqual(d, {})

    def test_get_site_data_file_not_found(self):
        """get_site_data should return empty dict if file doesn't exist.
        """
        path = 'idontexist.yml'
        d = sat.cli.setrev.main.get_site_data(path)
        self.assertEqual(d, {})

    @mock.patch('sat.cli.setrev.main.open', side_effect=PermissionError)
    def test_get_site_data_permission_error(self, mockopen):
        """get_site_data should throw permission error if file had bad perms.
        """
        path = '{}/good.yml'.format(samples)
        with self.assertRaises(PermissionError):
            d = sat.cli.setrev.main.get_site_data(path)

    def test_get_site_data_empty_file(self):
        """get_site_data should return empty dict if file was empty
        """
        path = '{}/empty'.format(samples)
        d = sat.cli.setrev.main.get_site_data(path)
        self.assertEqual(d, {})

    def test_get_site_data_non_yaml(self):
        """get_site_data should return empty dict if the file was non-yaml.
        """
        path = '{}/non-yaml.yml'.format(samples)
        d = sat.cli.setrev.main.get_site_data(path)
        self.assertEqual(d, {})

    @mock.patch('sat.cli.setrev.main.input', lambda x: full[x])
    def test_input_site_data_fresh(self):
        """input_site_data should insert vals to an empty dict.
        """
        d1 = {}
        sat.cli.setrev.main.input_site_data(d1)
        self.assertEqual(d1, full)

    @mock.patch('sat.cli.setrev.main.input', lambda x: empty_date[x])
    def test_input_site_data_empty_date(self):
        """input_site_data should default to today for 'System install date'.
        """
        d1 = {}
        d2 = {}
        d2.update(empty_date)
        d2['System install date'] = datetime.today().strftime('%Y-%m-%d')
        sat.cli.setrev.main.input_site_data(d1)
        self.assertEqual(d1, d2)

    @mock.patch('sat.cli.setrev.main.input', lambda x: empty_input[x])
    def test_input_site_data_preservation(self):
        """input_site_data should preserve non-empty entries of existing data.
        """
        d1 = {}
        d2 = {}
        d1.update(full)
        d2.update(d1)
        sat.cli.setrev.main.input_site_data(d1)

        self.assertEqual(d1, d2)

    @mock.patch('sat.cli.setrev.main.input', lambda x: full[x])
    def test_input_site_data_overwrite(self):
        """input_site_data should overwrite existing entries.
        """
        d1 = {}
        d1.update(full)
        d1['Serial number'] = 'new-serial-number'

        sat.cli.setrev.main.input_site_data(d1)
        self.assertEqual(d1, full)

    @mock.patch('sat.cli.setrev.main.input', lambda x: empty_input[x])
    def test_input_site_data_empty_input(self):
        """input_site_data should allow completely empty input.
        """
        d1 = {}
        expected = {
            'Serial number': '',
            'Site name': '',
            'System name': '',
            'System install date': datetime.today().strftime('%Y-%m-%d'),
            'System type': '',
        }

        sat.cli.setrev.main.input_site_data(d1)
        self.assertEqual(d1, expected)

    def test_write_site_data_newfile(self):
        """write_site_data should create the file if it doesn't exist.
        """
        sitefile = '{}/path/to/not/exist'.format(samples)
        d1 = {}

        m = mock.mock_open()
        with mock.patch('sat.cli.setrev.main.open', m):
            sat.cli.setrev.main.write_site_data(sitefile, d1)

        m.assert_called_once_with(sitefile, 'w')

    def test_write_site_data_readback(self):
        """write_site_data should read identically from data it's written.
        """
        try:
            sitefile = '{}/sitefile1.yml'.format(samples)
            d1 = full
            d2 = {}

            if os.path.exists(sitefile):
                os.remove(sitefile)

            # test that data is read the same as it is written
            sat.cli.setrev.main.write_site_data(sitefile, d1)
            d2 = sat.cli.setrev.main.get_site_data(sitefile)

            self.assertEqual(d1, d2)
        finally:
            if os.path.exists(sitefile):
                os.remove(sitefile)

    def test_write_site_data_overwrite(self):
        """write_site_data should overwrite existing entries
        """

        try:
            sitefile = '{}/sitefile1.yml'.format(samples)
            d1 = full
            sat.cli.setrev.main.write_site_data(sitefile, d1)
            sat.cli.setrev.main.write_site_data(sitefile, {})

            empty = {}
            result = sat.cli.setrev.main.get_site_data(sitefile)

            self.assertEqual(empty, empty)
        finally:
            if os.path.exists(sitefile):
                os.remove(sitefile)


def set_options(namespace):
    """Set default options for Namespace."""
    namespace.sitefile = '/sol/saturn/tethys_info.yml'
    namespace.no_borders = True
    namespace.no_headings = False
    namespace.format = 'pretty'
    namespace.reverse = object()
    namespace.sort_by = object()
    namespace.filter_strs = object()


class FakeStream:
    """Used for mocking the return from open."""
    def close(self):
        pass


class TestDoSetrev(unittest.TestCase):
    """Unit test for Setrev do_setrev()."""

    def setUp(self):
        """Mock functions called by do_setrev."""

        # Mock get_site_data to return site data. If a test wishes to
        # change the mock_site_data, the test should do something like:
        #     self.mock_site_data.return_value = {...}

        # The data returned by get_site_data:
        self.mock_site_data = {
            'Serial number': '2-4-8-16-32-64',
            'Site name': 'Saturn',
            'System name': 'Tethys',
            'System install': '',
            'System install date': datetime.today().strftime('%Y-%m-%d'),
            'System type': 'moon'
        }
        self.mock_get_site_data = mock.patch('sat.cli.setrev.main.get_site_data',
                                             return_value=self.mock_site_data,
                                             autospec=True).start()

        self.mock_input_site_data = mock.patch('sat.cli.setrev.main.input_site_data',
                                               autospec=True).start()
        self.mock_write_site_data = mock.patch('sat.cli.setrev.main.write_site_data',
                                               autospec=True).start()

        self.mock_get_config_value = mock.patch('sat.cli.setrev.main.get_config_value',
                                                return_value='/opt/cray/etc/site_info.yml',
                                                autospec=True).start()

        self.mock_os_path_dirname = mock.patch('os.path.dirname',
                                               return_value='/sol/saturn').start()
        self.mock_os_path_exists = mock.patch('os.path.exists',
                                              return_value=False).start()
        self.mock_os_makedirs = mock.patch('os.makedirs').start()

        self.mock_open = mock.patch('builtins.open', return_value=FakeStream(),
                                    autospec=True).start()

        self.parsed = Namespace()
        set_options(self.parsed)

    def tearDown(self):
        mock.patch.stopall()

    def test_opt_dir_missing(self):
        """Test setrev: do_setrev() option sitefile directory missing """
        sat.cli.setrev.main.do_setrev(self.parsed)
        self.mock_get_config_value.assert_not_called()
        self.mock_os_path_dirname.assert_called_once_with('/sol/saturn/tethys_info.yml')
        self.mock_os_path_exists.assert_called_once_with('/sol/saturn')
        self.mock_os_makedirs.assert_called_once_with('/sol/saturn')
        self.mock_open.assert_called_once_with('/sol/saturn/tethys_info.yml', 'a')

    def test_opt_dir_exists(self):
        """Test setrev: do_setrev() option sitefile directory exists """
        self.mock_os_path_exists.return_value = True
        sat.cli.setrev.main.do_setrev(self.parsed)
        self.mock_get_config_value.assert_not_called()
        self.mock_os_path_dirname.assert_called_once_with('/sol/saturn/tethys_info.yml')
        self.mock_os_path_exists.assert_called_once_with('/sol/saturn')
        self.mock_os_makedirs.assert_not_called()
        self.mock_open.assert_called_once_with('/sol/saturn/tethys_info.yml', 'a')

    def test_conf_dir_missing(self):
        """Test setrev: do_setrev() config sitefile directory missing """
        self.parsed.sitefile = None
        self.mock_os_path_dirname.return_value = '/opt/cray/etc'
        sat.cli.setrev.main.do_setrev(self.parsed)
        self.mock_get_config_value.assert_called_once()
        self.mock_os_path_dirname.assert_called_once_with('/opt/cray/etc/site_info.yml')
        self.mock_os_path_exists.assert_called_once_with('/opt/cray/etc')
        self.mock_os_makedirs.assert_called_once_with('/opt/cray/etc')
        self.mock_open.assert_called_once_with('/opt/cray/etc/site_info.yml', 'a')

    def test_conf_dir_exists(self):
        """Test setrev: do_setrev() config sitefile directory exists """
        self.parsed.sitefile = None
        self.mock_os_path_dirname.return_value = '/opt/cray/etc'
        self.mock_os_path_exists.return_value = True
        sat.cli.setrev.main.do_setrev(self.parsed)
        self.mock_get_config_value.assert_called_once()
        self.mock_os_path_dirname.assert_called_once_with('/opt/cray/etc/site_info.yml')
        self.mock_os_path_exists.assert_called_once_with('/opt/cray/etc')
        self.mock_os_makedirs.assert_not_called()
        self.mock_open.assert_called_once_with('/opt/cray/etc/site_info.yml', 'a')

    def test_no_sitefile_specified(self):
        """Test setrev: do_setrev() no sitefile specified """
        self.parsed.sitefile = None
        self.mock_get_config_value.return_value = {}
        with self.assertRaises(SystemExit):
            sat.cli.setrev.main.do_setrev(self.parsed)
        self.mock_get_config_value.assert_called_once()

    def test_file_permission_error(self):
        """Test setrev: do_setrev() sitefile permission error"""
        self.mock_os_path_exists.return_value = True
        self.mock_open.side_effect = PermissionError
        with self.assertRaises(SystemExit):
            sat.cli.setrev.main.do_setrev(self.parsed)
        self.mock_get_config_value.assert_not_called()
        self.mock_os_path_dirname.assert_called_once_with('/sol/saturn/tethys_info.yml')
        self.mock_os_path_exists.assert_called_once_with('/sol/saturn')
        self.mock_os_makedirs.assert_not_called()
        self.mock_open.assert_called_once_with('/sol/saturn/tethys_info.yml', 'a')


if __name__ == '__main__':
    unittest.main()
