import TestSetup
import os
import unittest
import datetime
import mock

import Testing.Test_Utils.test_utils as test_utils
import Main.config as config
import Internals.Utils.wlogger as wlogger


class TestWLogger(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = os.path.join(config.test_data_dir, self.__class__.__name__, self.id().split('.')[-1])
        test_utils.clear_temp(self.test_data_dir)

    @mock.patch('Internals.Utils.wlogger.wtime.WTime.get_now')
    def test_basic_log(self, mock_get_now):
        mock_get_now = mock.Mock.return_value = datetime.datetime(1960, 1, 1, 8, 10, 10)
        wlogger.setup_loggers(os.path.join(self.test_data_dir, 'Temp'), test_mode_on=True, name='test_basic_log')
        wlogger.log_info('First Info Message',  name='test_basic_log')
        wlogger.log_info('Second Info Message',  name='test_basic_log')
        wlogger.log_info('Third Info Message',  name='test_basic_log')
        wlogger.tear_down_loggers(name='test_basic_log')
        self.log_test_compare()
        
    @mock.patch('Internals.Utils.wlogger.wtime.WTime.get_now')
    def test_dir_and_log_already_exist(self, mock_get_now):
        mock_get_now = mock.Mock.return_value = datetime.datetime(1960, 1, 1, 8, 10, 10)

        # Set up a logger and write out some messages.
        wlogger.setup_loggers(os.path.join(self.test_data_dir, 'Temp'),
                              test_mode_on=True,
                              name='test_dir_and_log_already_exist')

        wlogger.log_info('First Info Message - Logger 1', name='test_dir_and_log_already_exist')
        wlogger.log_info('Second Info Message - Logger 1', name='test_dir_and_log_already_exist')
        wlogger.log_info('Third Info Message - Logger 1', name='test_dir_and_log_already_exist')
        wlogger.tear_down_loggers(name='test_dir_and_log_already_exist')

        wlogger.setup_loggers(os.path.join(self.test_data_dir, 'Temp'),
                              test_mode_on=True,
                              name='test_dir_and_log_already_exist_2')
        wlogger.log_info('First Info Message - Logger 2', name='test_dir_and_log_already_exist_2')
        wlogger.log_info('Second Info Message - Logger 2', name='test_dir_and_log_already_exist_2')
        wlogger.log_info('Third Info Message - Logger 2', name='test_dir_and_log_already_exist_2')
        wlogger.tear_down_loggers(name='test_dir_and_log_already_exist_2')

        self.log_test_compare()

    @mock.patch('Internals.Utils.wlogger.wtime.WTime.get_now')
    def test_dir_does_not_exist(self, mock_get_now):
        mock_get_now = mock.Mock.return_value = datetime.datetime(1960, 1, 1, 8, 10, 10)

        # Extend filepath required to check that sub directories are created.
        file_path = os.path.join(self.test_data_dir, 'Temp', 'SubDirectory', 'SubSubDirectory')
        wlogger.setup_loggers(file_path,
                              test_mode_on=True,
                              name='test_dir_does_not_exist')

        wlogger.log_info('First Info Message', name='test_dir_does_not_exist')
        wlogger.log_info('Second Info Message', name='test_dir_does_not_exist')
        wlogger.log_info('Third Info Message', name='test_dir_does_not_exist')
        wlogger.tear_down_loggers(name='test_dir_does_not_exist')

        self.log_test_compare()

    @mock.patch('Internals.Utils.wlogger.wtime.WTime.get_now')
    def test_message_levels_debug_on(self, mock_get_now):
        mock_get_now = mock.Mock.return_value = datetime.datetime(1960, 1, 1, 8, 10, 10)
        wlogger.setup_loggers(os.path.join(self.test_data_dir, 'Temp'),
                              debug_on=True,
                              test_mode_on=True,
                              name='test_message_levels_debug_on')

        wlogger.log_info('Info Message',        name='test_message_levels_debug_on')
        wlogger.log_debug('Debug Message',      name='test_message_levels_debug_on')
        wlogger.log_error('Error Message',      name='test_message_levels_debug_on')
        wlogger.log_info('Info Message',        name='test_message_levels_debug_on')
        wlogger.log_debug('Debug Message',      name='test_message_levels_debug_on')
        wlogger.log_warning('Warning Message',  name='test_message_levels_debug_on')
        wlogger.tear_down_loggers(name='test_message_levels_debug_on')

        self.log_test_compare()


    @mock.patch('Internals.Utils.wlogger.wtime.WTime.get_now')
    def test_message_levels_debug_off(self, mock_get_now):
        mock_get_now = mock.Mock.return_value = datetime.datetime(1960, 1, 1, 8, 10, 10)
        wlogger.setup_loggers(os.path.join(self.test_data_dir, 'Temp'),
                              debug_on=False,
                              test_mode_on=True,
                              name='test_message_levels_debug_off')

        wlogger.log_info('Info Message',        name='test_message_levels_debug_off')
        wlogger.log_debug('Debug Message',      name='test_message_levels_debug_off')
        wlogger.log_error('Error Message',      name='test_message_levels_debug_off')
        wlogger.log_info('Info Message',        name='test_message_levels_debug_off')
        wlogger.log_debug('Debug Message',      name='test_message_levels_debug_off')
        wlogger.log_warning('Warning Message',  name='test_message_levels_debug_off')
        wlogger.tear_down_loggers(name='test_message_levels_debug_off')

        self.log_test_compare()


    @mock.patch('Internals.Utils.wlogger.wtime.WTime.get_now')
    def test_file_rotation(self, mock_get_now):
        mock_get_now = mock.Mock.return_value = datetime.datetime(1960, 1, 1, 8, 10, 10)
        wlogger.setup_loggers(os.path.join(self.test_data_dir, 'Temp'),
                              debug_on=True,
                              test_mode_on=True,
                              name='test_file_rotation',
                              maxBytes=1000)

        for i in range(0, 1000):
            wlogger.log_info('Info Message ' + str(i),        name='test_file_rotation')
            wlogger.log_debug('Debug Message ' + str(i),      name='test_file_rotation')
            wlogger.log_error('Error Message ' + str(i),      name='test_file_rotation')

        wlogger.tear_down_loggers(name='test_file_rotation')
        self.log_test_compare()


    def log_test_compare(self):
        # Should be commented out unless baselining
        # test_utils.overwrite_expected_results_dir(self.test_data_dir)

        # Compare folders.
        dir_equal, message = test_utils.are_dir_trees_equal(os.path.join(self.test_data_dir, 'Temp'),
                                                            os.path.join(self.test_data_dir,
                                                            'Outputs'))

        self.assertTrue(dir_equal, 'FAILED - Directory Comparison: ' + message)


if __name__ == '__main__':
    unittest.main()
