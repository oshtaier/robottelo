# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai
"""Test class for Host CLI"""

from ddt import ddt
from fauxfactory import gen_string
from robottelo.cli.factory import (
    make_lifecycle_environment, make_org, CLIFactoryError)
from robottelo.cli.lifecycleenvironment import LifecycleEnvironment
from robottelo.common.decorators import data, run_only_on
from robottelo.test import CLITestCase


@run_only_on('sat')
@ddt
class TestLifeCycleEnvironment(CLITestCase):
    """Test class for Lifecycle Environment CLI"""

    org = None

    def setUp(self):  # noqa
        """Tests for Lifecycle Environment via Hammer CLI"""

        super(TestLifeCycleEnvironment, self).setUp()

        if TestLifeCycleEnvironment.org is None:
            TestLifeCycleEnvironment.org = make_org()

    # Issues validation
    def test_bugzilla_1077386(self):
        """@Test: List subcommand returns standard output

        @Feature: Lifecycle Environment

        @Assert: There should not be an error returned

        """

        # List avaialble lifecycle environments using default Table
        # output
        cmd = u"lifecycle-environment list --organization-id=\"%s\""
        result = LifecycleEnvironment.execute(
            cmd % self.org['id'],
            None,
            None,
            False
        )

        self.assertEqual(
            result.return_code, 0, "Could not find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")
        self.assertGreater(
            len(result.stdout), 0, "No output was returned"
        )

    def test_bugzilla_1077333(self):
        """@Test: Search lifecycle environment via its name containing UTF-8 chars

        @Feature: Lifecycle Environment

        @Assert: Can get info for lifecycle by its name

        """

        payload = {
            'organization-id': self.org['id'],
            'name': gen_string('utf8', 15),
        }

        new_obj = make_lifecycle_environment(payload)
        self.assertIsNotNone(
            new_obj, "Could not create lifecycle environment.")

        # Can we find the new object
        result = LifecycleEnvironment.info(
            {
                'organization-id': self.org['id'],
                'name': new_obj['name'],
            }
        )

        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")
        self.assertGreater(
            len(result.stdout), 0, "No output was returned"
        )
        self.assertEqual(
            new_obj['name'],
            result.stdout['name'],
            "Could not find lifecycle environment \'%s\'" % new_obj['name']
        )

    # CRUD
    @data(
        {'name': gen_string("alpha", 15)},
        {'name': gen_string("alphanumeric", 15)},
        {'name': gen_string("numeric", 15)},
        {'name': gen_string("latin1", 15)},
        {'name': gen_string("utf8", 15)},
        {'name': gen_string("html", 15)},
    )
    def test_positive_create_1(self, test_data):
        """@Test: Create lifecycle environment with valid name, prior to Library

        @Feature: Lifecycle Environment

        @Assert: Lifecycle environment is created with Library as prior

        """

        payload = {
            'organization-id': self.org['id'],
            'name': test_data['name'],
        }

        new_obj = make_lifecycle_environment(payload)
        self.assertIsNotNone(
            new_obj, "Could not create lifecycle environment.")

        # Can we find the new object
        result = LifecycleEnvironment.info(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
            }
        )

        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")
        self.assertGreater(
            len(result.stdout), 0, "No output was returned"
        )
        self.assertEqual(
            new_obj['name'],
            result.stdout['name'],
            "Could not find lifecycle environment \'%s\'" % new_obj['name']
        )

    @data(
        {'name': gen_string("alpha", 15)},
        {'name': gen_string("alphanumeric", 15)},
        {'name': gen_string("numeric", 15)},
        {'name': gen_string("latin1", 15)},
        {'name': gen_string("utf8", 15)},
        {'name': gen_string("html", 15)},
    )
    def test_positive_create_2(self, test_data):
        """@Test: Create lifecycle environment with valid name and description,
        prior to Library

        @Feature: Lifecycle Environment

        @Assert: Lifecycle environment is created with Library as prior

        """

        payload = {
            'organization-id': self.org['id'],
            'name': test_data['name'],
            'description': test_data['name'],
        }

        new_obj = make_lifecycle_environment(payload)
        self.assertIsNotNone(
            new_obj, "Could not create lifecycle environment.")

        # Can we find the new object
        result = LifecycleEnvironment.info(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
            }
        )

        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")
        self.assertGreater(
            len(result.stdout), 0, "No output was returned"
        )
        self.assertEqual(
            new_obj['name'],
            result.stdout['name'],
            "Could not find lifecycle environment \'%s\'" % new_obj['name']
        )
        self.assertEqual(
            new_obj['description'],
            result.stdout['description'],
            "Descriptions don't match"
        )

    @data(
        {'name': gen_string("alpha", 15)},
        {'name': gen_string("alphanumeric", 15)},
        {'name': gen_string("numeric", 15)},
        {'name': gen_string("latin1", 15)},
        {'name': gen_string("utf8", 15)},
        {'name': gen_string("html", 15)},
    )
    def test_positive_delete_1(self, test_data):
        """@Test: Create lifecycle environment with valid name, prior to Library

        @Feature: Lifecycle Environment

        @Assert: Lifecycle environment is deleted

        """

        payload = {
            'organization-id': self.org['id'],
            'name': test_data['name'],
        }

        new_obj = make_lifecycle_environment(payload)
        self.assertIsNotNone(
            new_obj, "Could not create lifecycle environment.")

        # Can we find the new object
        result = LifecycleEnvironment.info(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
            }
        )

        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")
        self.assertGreater(
            len(result.stdout), 0, "No output was returned"
        )
        self.assertEqual(
            new_obj['name'],
            result.stdout['name'],
            "Could not find lifecycle environment \'%s\'" % new_obj['name']
        )

        # Delete the lifecycle environment
        result = LifecycleEnvironment.delete({'id': new_obj['id']})

        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")

        # Can we find the object
        result = LifecycleEnvironment.info(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
            }
        )

        self.assertGreater(
            result.return_code, 0, "Should not find the lifecycle environment"
        )
        self.assertGreater(
            len(result.stderr), 0, "There should be an error here"
        )

    @data(
        {'name': gen_string("alpha", 15)},
        {'name': gen_string("alphanumeric", 15)},
        {'name': gen_string("numeric", 15)},
        {'name': gen_string("latin1", 15)},
        {'name': gen_string("utf8", 15)},
        {'name': gen_string("html", 15)},
    )
    def test_positive_update_1(self, test_data):
        """@Test: Create lifecycle environment then update its name

        @Feature: Lifecycle Environment

        @Assert: Lifecycle environment name is updated

        """

        payload = {
            'organization-id': self.org['id'],
        }

        new_obj = make_lifecycle_environment(payload)
        self.assertIsNotNone(
            new_obj, "Could not create lifecycle environment.")

        # Update its name
        result = LifecycleEnvironment.update(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
                'new-name': test_data['name'],
            }
        )
        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")

        # Fetch the object
        result = LifecycleEnvironment.info(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
            }
        )
        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")
        self.assertGreater(
            len(result.stdout), 0, "No output was returned"
        )
        self.assertEqual(
            test_data['name'],
            result.stdout['name'],
            "Name was not updated"
        )
        self.assertNotEqual(
            new_obj['name'],
            result.stdout['name'],
            "Name should have been updated"
        )

    @data(
        {'description': gen_string("alpha", 15)},
        {'description': gen_string("alphanumeric", 15)},
        {'description': gen_string("numeric", 15)},
        {'description': gen_string("latin1", 15)},
        {'description': gen_string("utf8", 15)},
        {'description': gen_string("html", 15)},
    )
    def test_positive_update_2(self, test_data):
        """@Test: Create lifecycle environment then update its description

        @Feature: Lifecycle Environment

        @Assert: Lifecycle environment description is updated

        """

        payload = {
            'organization-id': self.org['id'],
        }

        new_obj = make_lifecycle_environment(payload)
        self.assertIsNotNone(
            new_obj, "Could not create lifecycle environment.")

        # Update its description
        result = LifecycleEnvironment.update(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
                'description': test_data['description'],
            }
        )
        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")

        # Fetch the object
        result = LifecycleEnvironment.info(
            {
                'organization-id': self.org['id'],
                'id': new_obj['id'],
            }
        )
        self.assertEqual(
            result.return_code, 0, "Could find the lifecycle environment"
        )
        self.assertEqual(
            len(result.stderr), 0, "There should not be an error here.")
        self.assertGreater(
            len(result.stdout), 0, "No output was returned"
        )
        self.assertEqual(
            test_data['description'],
            result.stdout['description'],
            "Description was not updated"
        )
        self.assertNotEqual(
            new_obj['description'],
            result.stdout['description'],
            "Description should have been updated"
        )

    def test_environment_paths(self):
        """@Test: List the environment paths under a given organization

        @Feature: Lifecycle Environment

        @Assert: Lifecycle environment paths listed

        """
        try:
            org = make_org()
            test_env = make_lifecycle_environment({
                'organization-id': org['id'],
            })
        except CLIFactoryError as err:
            self.fail(err)

        # Add paths to lifecycle environments
        result = LifecycleEnvironment.paths({
            'organization-id': org['id'],
            'permission-type': 'readable',
        })
        self.assertEqual(result.return_code, 0)
        self.assertEqual(len(result.stderr), 0)
        self.assertIn(
            u'Library >> {0}'.format(test_env['name']),
            u''.join(result.stdout)
        )
