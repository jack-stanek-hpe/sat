"""
Unit tests for sat.redfish

Copyright 2019 Cray Inc. All Rights Reserved.
"""

import os
import unittest
from collections import defaultdict
from unittest import mock

import sat.redfish
import sat.config


class InputDict(dict):
    """For help with mocking getpass.

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


# For mocking sat.config.get_config_value
full = defaultdict(lambda: '')
full['redfish.username'] = 'user'
full['redfish.password'] = 'pass'

withuser = defaultdict(lambda: '')
withuser['redfish.username'] = 'user'

withpass = defaultdict(lambda: '')
withpass['redfish.password'] = 'pass'

empty = defaultdict(lambda: '')


# for help with mocking getpass and pester, which require input over stdin.
passdict = InputDict({
    'User': 'prompted_user',
    'Pass': 'prompted_pass',
})


def fake_pester(message, valid_answer, human_readable_valid, parse_answer):
    """For mocking pester.

    Args:
        Just here to mirror the signature of sat.util.pester. Message is
        all we care about.
    """
    return passdict[message]


class TestRedfishAuth(unittest.TestCase):
    """Tests for redfish.get_username_and_pass function.
    """

    @mock.patch('sat.redfish.get_config_value', lambda x: full[x])
    def test_empty_suggestion(self):
        """It should use the values in the config if no suggestion.
        """
        u, p = sat.redfish.get_username_and_pass()
        self.assertEqual('user', u)
        self.assertEqual('pass', p)

    @mock.patch('sat.redfish.get_config_value', lambda x: full[x])
    @mock.patch('sat.redfish.getpass.getpass', lambda x: passdict[x])
    def test_suggestion_usage(self):
        """It should use the suggested username and prompt for a password.
        """
        u, p = sat.redfish.get_username_and_pass('suggestion')
        self.assertEqual('suggestion', u)
        self.assertEqual(passdict['Pass'], p)

    @mock.patch('sat.redfish.get_config_value', lambda x: empty[x])
    @mock.patch('sat.redfish.getpass.getpass', lambda x: passdict[x])
    @mock.patch('sat.redfish.pester', fake_pester)
    def test_empty_config(self):
        """It should prompt for both username and password if config empty.
        """
        u, p = sat.redfish.get_username_and_pass()
        self.assertEqual(passdict['User'], u)
        self.assertEqual(passdict['Pass'], p)

    @mock.patch('sat.redfish.get_config_value', lambda x: withuser[x])
    @mock.patch('sat.redfish.getpass.getpass', lambda x: passdict[x])
    def test_config_has_username(self):
        """It should only prompt for password if config has username.
        """
        u, p = sat.redfish.get_username_and_pass()
        self.assertEqual('user', u)
        self.assertEqual(passdict['Pass'], p)

    @mock.patch('sat.redfish.get_config_value', lambda x: withpass[x])
    @mock.patch('sat.redfish.getpass.getpass', lambda x: passdict[x])
    @mock.patch('sat.redfish.pester', fake_pester)
    def test_config_has_password(self):
        """It should prompt for both if config is missing username.
        """
        u, p = sat.redfish.get_username_and_pass()
        self.assertEqual(passdict['User'], u)
        self.assertEqual(passdict['Pass'], p)

    @mock.patch('sat.redfish.get_config_value', lambda x: withpass[x])
    @mock.patch('sat.redfish.getpass.getpass', lambda x: passdict[x])
    def test_config_has_password_with_suggestion(self):
        """It should just prompt for password if it has been given a suggestion.

        This should hold even if the config is missing a username.
        """
        u, p = sat.redfish.get_username_and_pass('suggestion')
        self.assertEqual('suggestion', u)
        self.assertEqual(passdict['Pass'], p)


if __name__ == '__main__':
    unittest.main()
