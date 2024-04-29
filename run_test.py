import unittest
import logging
from tests.unit.test_database_setup import setup_database, teardown_database


if __name__ == '__main__':
    # Disbale logging while running unit test
    # logging.disable(logging.CRITICAL)

    # Set up the database before running tests
    setup_database()

    '''Run all tests'''
    test_suite = unittest.defaultTestLoader.discover(
        start_dir='test/unit/', pattern='test_*.py')

    '''Run tests of specific module'''
    # test_suite = unittest.defaultTestLoader.loadTestsFromName(
    #     'test.unit.test_account')

    # '''Run tests for specific test class'''
    # test_suite = unittest.defaultTestLoader.loadTestsFromName(
    #     'test.unit.test_account.TestAccountAPI')

    '''Run specific test case'''
    # test_suite = unittest.defaultTestLoader.loadTestsFromName(
    #     'test.unit.test_healthcheck.TestHealthcheck.test_healthcheck')

    '''Run multiple specific tests'''
    # test_suite = unittest.defaultTestLoader.loadTestsFromNames([
    #     'test.unit.test_healthcheck.TestHealthcheck.test_healthcheck',
    #     'test.unit.test_account.TestAccountAPI.test_unauthorized']
    #     )

    unittest.TextTestRunner(verbosity=2).run(test_suite)

    # Tear down the database after all tests have been executed
    teardown_database()
