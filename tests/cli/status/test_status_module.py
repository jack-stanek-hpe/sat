"""
Tests for the sat.cli.status.status_module module.

(C) Copyright 2022 Hewlett Packard Enterprise Development LP.

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

import unittest
from unittest.mock import MagicMock, patch

from sat.cli.status.status_module import StatusModule, StatusModuleException
from sat.constants import MISSING_VALUE


class TestStatusModuleSubclassing(unittest.TestCase):
    """Tests for the subclassing StatusModule."""
    def test_status_modules_added(self):
        """Test that StatusModule subclasses are registered"""
        class TestStatusModule(StatusModule):
            pass  # Don't need to define methods, no instances are created.

        self.assertIn(TestStatusModule, StatusModule.modules)


class BaseStatusModuleTestCase(unittest.TestCase):
    def setUp(self):
        patch('sat.cli.status.status_module.StatusModule.__init_subclass__').start()
        if hasattr(self, 'modules'):
            patch('sat.cli.status.status_module.StatusModule.modules', self.modules).start()

    def tearDown(self):
        patch.stopall()


class TestStatusModuleGettingModules(BaseStatusModuleTestCase):
    """Tests for retrieving specific modules"""
    def setUp(self):
        class NodeTestModule(StatusModule):
            component_types = {'Node'}
        self.NodeTestModule = NodeTestModule

        class NodeBMCTestModule(StatusModule):
            component_types = {'NodeBMC'}
        self.NodeBMCTestModule = NodeBMCTestModule

        class PrimaryTestModule(StatusModule):
            primary = True
        self.PrimaryTestModule = PrimaryTestModule

        self.modules = [NodeTestModule, NodeBMCTestModule, PrimaryTestModule]
        super().setUp()

    def test_getting_relevant_modules(self):
        """Test that relevant modules are returned by get_relevant_modules()"""
        self.assertIn(self.NodeTestModule, StatusModule.get_relevant_modules(component_type='Node'))

    def test_irrelevant_modules_ignored(self):
        """Test that irrelevant modules are ignored by get_relevant_modules()"""
        self.assertNotIn(self.NodeBMCTestModule, StatusModule.get_relevant_modules(component_type='Node'))

    def test_all_modules_returned_no_component_types(self):
        """Test that all modules are returned if no component types specified"""
        self.assertEqual(self.modules, StatusModule.get_relevant_modules())

    def test_limit_subset_of_modules_returned(self):
        """Test that a limited subset of modules can be returned by get_relevant_modules()"""
        self.assertEqual([self.NodeTestModule],
                         StatusModule.get_relevant_modules(limit_modules=[self.NodeTestModule]))

    def test_getting_primary_module(self):
        """Test getting the primary module"""
        self.assertEqual(StatusModule.get_primary(), self.PrimaryTestModule)

    def test_can_only_get_one_primary_module(self):
        """Test that there can only be one primary module"""
        class AnotherPrimaryModule(StatusModule):
            primary = True
        self.modules.append(AnotherPrimaryModule)

        with self.assertRaises(ValueError):
            StatusModule.get_primary()


class TestStatusModuleHeadings(BaseStatusModuleTestCase):
    """Tests for getting lists of table headings"""
    def setUp(self):
        class SomeTestStatusModule(StatusModule):
            headings = ['xname', 'some_attribute']
        self.SomeTestStatusModule = SomeTestStatusModule

        class AnotherTestStatusModule(StatusModule):
            headings = ['xname', 'another_attribute', 'one_more_attribute']
        self.AnotherTestStatusModule = AnotherTestStatusModule

        self.modules = [SomeTestStatusModule, AnotherTestStatusModule]
        super().setUp()

    def test_get_all_headings(self):
        """Test getting headings for all StatusModules"""
        self.assertEqual(StatusModule.get_all_headings(primary_key='xname'),
                         ['xname', 'some_attribute', 'another_attribute', 'one_more_attribute'])

    def test_get_all_headings_initial(self):
        """Test ordering StatusModule headings manually with initial_headings"""
        self.assertEqual(StatusModule.get_all_headings(primary_key='xname',
                                                       initial_headings=['another_attribute']),
                         ['xname', 'another_attribute', 'some_attribute', 'one_more_attribute'])

    def test_get_all_headings_from_some_modules(self):
        """Test getting the headings from a subset of modules"""
        self.assertEqual(StatusModule.get_all_headings(primary_key='xname',
                                                       limit_modules=[self.SomeTestStatusModule]),
                         self.SomeTestStatusModule.headings)

    def test_get_all_headings_subset_with_manual_order(self):
        """Test ordering headings manually with a subset of modules"""
        self.assertEqual(StatusModule.get_all_headings(primary_key='xname',
                                                       limit_modules=[self.AnotherTestStatusModule],
                                                       initial_headings=['one_more_attribute']),
                         ['xname', 'one_more_attribute', 'another_attribute'])


class TestGettingRows(BaseStatusModuleTestCase):
    """Tests for getting populated rows"""
    def setUp(self):
        self.all_rows = [
            {'xname': 'x3000c0s1b0n0',
             'state': 'on',
             'config': 'some_config'},
            {'xname': 'x3000c0s1b0n1',
             'state': 'off',
             'config': 'another_config'},
        ]
        outer_self = self

        class RowTestStatusModule(StatusModule):
            source_name = 'test'

            @property
            def rows(self):
                return [{key: row[key] for key in self.headings}
                        for row in outer_self.all_rows]

        class TestStatusModuleOne(RowTestStatusModule):
            primary = True
            headings = ['xname', 'state']
        self.TestStatusModuleOne = TestStatusModuleOne

        class TestStatusModuleTwo(RowTestStatusModule):
            headings = ['xname', 'config']
        self.TestStatusModuleTwo = TestStatusModuleTwo

        self.modules = [TestStatusModuleOne, TestStatusModuleTwo]
        super().setUp()

    def test_getting_populated_rows(self):
        """Test getting rows in the successful case"""
        for row in StatusModule.get_populated_rows(primary_key='xname', session=MagicMock()):
            self.assertIn(row, self.all_rows)

    def test_getting_populated_rows_fails(self):
        """Test that columns from failing modules are omitted"""
        bad_key = 'irrelevant information'

        class TestStatusModuleFails(StatusModule):
            source_name = 'failure'
            headings = ['xname', bad_key]

            @property
            def rows(self):
                raise StatusModuleException('Information is irrelevant!')

        self.modules.append(TestStatusModuleFails)
        with self.assertLogs(level='WARNING'):
            rows = StatusModule.get_populated_rows(primary_key='xname', session=MagicMock())

        for row in rows:
            for heading, value in row.items():
                if heading == bad_key:
                    self.assertEqual(value, MISSING_VALUE)
                else:
                    self.assertNotEqual(value, MISSING_VALUE)

    def test_getting_populated_rows_subset_of_modules(self):
        """Test that rows can be retrieved with a subset of modules"""
        rows = StatusModule.get_populated_rows(primary_key='xname', session=MagicMock(),
                                               limit_modules=[self.TestStatusModuleOne])
        for populated_row, original_row in zip(rows, self.all_rows):
            for heading in self.TestStatusModuleOne.headings:
                self.assertEqual(populated_row[heading], original_row[heading])
            self.assertNotIn('config', populated_row)
