#! /usr/bin/env python
import os
import json
from unittest import TestCase
from pandashells.lib import arg_lib, config_lib
import argparse
from mock import patch, MagicMock, call

from pandashells.bin.p_df import (
    needs_show,
    get_modules_and_shortcuts,
    ensure_modules_installed,
)


class NeedsShowTests(TestCase):
    def test_doesnt_need_show(self):
        command_list = ['df.reset_index()', 'df.head()']
        self.assertFalse(needs_show(command_list))
    def test_needs_show(self):
        command_list = ['set_xlim([1, 2])']
        self.assertTrue(needs_show(command_list))


class GetModulesAndShortcutsTests(TestCase):
    def test_none_needed(self):
        command_list = ['df.reset_index()', 'df.head()']
        self.assertEqual(get_modules_and_shortcuts(command_list), [])

    def test_get_extra_import_all_needed(self):
        command_list = [
            'pl.plot(df.x)',
            'sns.distplot(df.x)',
            'scp.stats.norm(1, 1)',
            'np.random.randn(1)'
        ]
        self.assertEqual(
            set(get_modules_and_shortcuts(command_list)),
            {
                ('scipy', 'scp'),
                ('pylab', 'pl'),
                ('seaborn', 'sns'),
                ('numpy', 'np'),
            },
        )

class EnsureModulesInstalledTests(TestCase):
    @patch('pandashells.bin.p_df.sys.exit')
    @patch('pandashells.bin.p_df.module_checker_lib.check_for_modules')
    def test_modules_installed(self, checker_mock, exit_mock):
        checker_mock.return_value = True
        ensure_modules_installed()
        self.assertFalse(exit_mock.called)

    @patch('pandashells.bin.p_df.sys.exit')
    @patch('pandashells.bin.p_df.module_checker_lib.check_for_modules')
    def test_modules_not_installed(self, checker_mock, exit_mock):
        checker_mock.return_value = False
        ensure_modules_installed()
        self.assertTrue(exit_mock.called)


# class ArgLibTests(TestCase):
#     def setUp(self):
#         pass
# 
#     def test_check_for_recognized_args_bad_args(self):
#         """
#         _check_for_recognized_args() properly recognizes bad arguments
#         """
#         with self.assertRaises(ValueError):
#             arg_lib._check_for_recognized_args('unrecognized', 'args')
# 
#     def test_check_for_recognized_args_good_args(self):
#         """
#         _check_for_recognized_args() properly accepts good args
#         """
#         args = [
#             'io_in',
#             'io_out',
#             'example',
#             'xy_plotting',
#             'decorating',
#         ]
#         arg_lib._check_for_recognized_args(*args)
# 
#     def test_io_in_adder_inactive(self):
#         """
#         _io_in_adder() doesn't do anything when io_in not specified
#         """
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
#         args = []
#         arg_lib._io_in_adder(parser, {}, *args)
#         self.assertFalse(parser.add_argument.called)
# 
#     def test_io_in_adder_active(self):
#         """
#         _io_in_adder() adds proper arguments
#         """
#         # --- set up mock parser
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
# 
#         # --- create a list of expected call signatures
#         calls = []
#         msg = 'Overwrite column names with list of names'
#         calls.append(call('--names', nargs='+', type=str,
#                           dest='names', metavar="name", help=msg))
#         default_for_input = ['csv', 'header']
#         io_opt_list = ['csv', 'table', 'header', 'noheader']
#         calls.append(call('-i', '--input_options', nargs='+',
#                           type=str, dest='input_options', metavar='option',
#                           default=default_for_input, choices=io_opt_list,
#                           help='Input Options'))
# 
#         # --- run the code under test
#         args = ['io_in']
#         config_dict = {'io_input_type': 'csv', 'io_input_header': 'header'}
#         arg_lib._io_in_adder(parser, config_dict, *args)
# 
#         # --- make sure proper calls were made
#         self.assertEqual(parser.add_argument.call_args_list, calls)
# 
#     def test_io_out_adder_inactive(self):
#         """
#         _io_out_adder() doesn't do anything when io_out not specified
#         """
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
#         args = []
#         arg_lib._io_out_adder(parser, {}, *args)
#         self.assertFalse(parser.add_argument.called)
# 
#     def test_io_out_adder_active(self):
#         """
#         _io_out_adder() adds proper arguments
#         """
#         # --- set up mock parser
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
# 
#         # --- create  expected call signature
#         io_opt_list = ['csv', 'table', 'html',
#                        'header', 'noheader', 'index', 'noindex']
#         # --- define the current defaults
#         default_for_output = ['csv', 'header', 'noindex']
#         msg = 'Options taken from {}'.format(repr(io_opt_list))
#         call_obj = call('-o', '--output_options', nargs='+',
#                         type=str, dest='output_options', metavar='option',
#                         default=default_for_output, help=msg)
# 
#         # --- run the code under test
#         args = ['io_out']
#         config_dict = {
#             'io_output_type': 'csv',
#             'io_output_header': 'header',
#             'io_output_index': 'noindex'
#         }
#         arg_lib._io_out_adder(parser, config_dict, *args)
# 
#         # --- make sure proper calls were made
#         self.assertEqual(parser.add_argument.call_args_list, [call_obj])
# 
#     def test_decorating_adder_inactive(self):
#         """
#         _decorating_adder() doesn't do anything when decorating not specified
#         """
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
#         args = []
#         arg_lib._decorating_adder(parser, *args)
#         self.assertFalse(parser.add_argument.called)
# 
#     def test_decorating_adder_active(self):
#         """
#         _decorating_adder() adds proper arguments
#         """
#         # --- set up mock parser
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
# 
#         # --- create a list of expected call signatures
#         calls = []
# 
#         context_list = [t for t in config_lib.CONFIG_OPTS if
#                         t[0] == 'plot_context'][0][1]
#         theme_list = [t for t in config_lib.CONFIG_OPTS if
#                       t[0] == 'plot_theme'][0][1]
#         palette_list = [t for t in config_lib.CONFIG_OPTS if
#                         t[0] == 'plot_palette'][0][1]
# 
#         msg = "Set the x-limits for the plot"
#         calls.append(call('--xlim', nargs=2, type=float, dest='xlim',
#                           metavar=('XMIN', 'XMAX'), help=msg))
# 
#         msg = "Set the y-limits for the plot"
#         calls.append(call('--ylim', nargs=2, type=float, dest='ylim',
#                           metavar=('YMIN', 'YMAX'), help=msg))
# 
#         msg = "Set the x-label for the plot"
#         calls.append(call('--xlabel', nargs=1, type=str, dest='xlabel',
#                           help=msg))
# 
#         msg = "Set the y-label for the plot"
#         calls.append(call('--ylabel', nargs=1, type=str, dest='ylabel',
#                           help=msg))
# 
#         msg = "Set the title for the plot"
#         calls.append(call('--title', nargs=1, type=str, dest='title', help=msg))
# 
#         msg = "Specify legend location"
#         calls.append(call('--legend', nargs=1, type=str, dest='legend',
#                           choices=['1', '2', '3', '4', 'best'], help=msg))
# 
#         msg = "Specify whether hide the grid or not"
#         calls.append(call('--nogrid',  action='store_true', dest='no_grid',
#                           default=False,  help=msg))
# 
#         msg = "Specify plot context. Default = '{}' ".format(context_list[0])
#         calls.append(call('--context', nargs=1, type=str, dest='plot_context',
#                           default=[context_list[0]], choices=context_list,
#                           help=msg))
# 
#         msg = "Specify plot theme. Default = '{}' ".format(theme_list[0])
#         calls.append(call('--theme', nargs=1,
#                           type=str, dest='plot_theme', default=[theme_list[0]],
#                           choices=theme_list, help=msg))
# 
#         msg = "Specify plot palette. Default = '{}' ".format(palette_list[0])
#         calls.append(call('--palette', nargs=1, type=str, dest='plot_palette',
#                           default=[palette_list[0]], choices=palette_list,
#                           help=msg))
# 
#         msg = "Save the figure to this file"
#         calls.append(call('--savefig', nargs=1, type=str, help=msg))
# 
#         # --- run the code under test
#         args = ['decorating']
#         arg_lib._decorating_adder(parser, *args)
# 
#         # --- make sure proper calls were made
#         self.assertEqual(parser.add_argument.call_args_list, calls)
# 
#     def test_xy_adder_inactive(self):
#         """
#         _xy_adder() doesn't do anything when xy_plotting not specified
#         """
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
#         args = []
#         arg_lib._xy_adder(parser, *args)
#         self.assertFalse(parser.add_argument.called)
# 
#     def test_xy_adder_active(self):
#         """
#         _xy_adder() adds proper arguments
#         """
#         # --- set up mock parser
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
# 
#         # --- create a list of expected call signatures
#         calls = []
#         msg = 'Column to plot on x-axis'
#         calls.append(call('-x', nargs=1, type=str, dest='x', metavar='col',
#                      help=msg))
# 
#         msg = 'List of columns to plot on y-axis'
#         calls.append(call('-y', nargs='+', type=str, dest='y',
#                      metavar='col', help=msg))
# 
#         msg = "Plot style defaults to .-"
#         calls.append(call('-s', '--style', nargs=1, type=str, dest='style',
#                      default=['.-'], help=msg))
# 
#         # --- run the code under test
#         args = ['xy_plotting']
#         arg_lib._xy_adder(parser, *args)
# 
#         # --- make sure proper calls were made
#         self.assertEqual(parser.add_argument.call_args_list, calls)
# 
#     def test_example_adder_inactive(self):
#         """
#         _example_adder() doesn't do anything when example not specified
#         """
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
#         args = []
#         arg_lib._example_adder(parser, *args)
#         self.assertFalse(parser.add_argument.called)
# 
#     def test_example_adder_active(self):
#         """
#         _example_adder() adds proper arguments
#         """
#         # --- set up mock parser
#         parser = MagicMock()
#         parser.add_argument = MagicMock()
# 
#         msg = "Show a usage example and exit"
#         call_obj = call('--example', action='store_true', dest='example',
#                         default=False,  help=msg)
# 
#         args = ['example']
#         arg_lib._example_adder(parser, *args)
# 
#         # --- make sure proper calls were made
#         self.assertEqual(parser.add_argument.call_args_list, [call_obj])
# 
#     @patch('pandashells.lib.arg_lib._example_adder')
#     @patch('pandashells.lib.arg_lib._xy_adder')
#     @patch('pandashells.lib.arg_lib._decorating_adder')
#     @patch('pandashells.lib.arg_lib._io_out_adder')
#     @patch('pandashells.lib.arg_lib._io_in_adder')
#     @patch('pandashells.lib.arg_lib._check_for_recognized_args')
#     @patch('pandashells.lib.arg_lib.config_lib.get_config')
#     def test_add_args(self,
#                       get_config_mock,
#                       _check_for_recognized_args_mock,
#                       _io_in_adder_mock,
#                       _io_out_adder_mock,
#                       _decorating_adder_mock,
#                       _xy_adder_mock,
#                       _example_adder_mock):
#         # --- set up the mocks
#         parser = MagicMock()
#         get_config_mock.return_value = {}
# 
#         # --- define expected call signatures
#         plain_call_list = [call(parser)]
#         config_call_list = [call(parser, {})]
# 
#         # --- call the code under test
#         arg_lib.add_args(parser)
# 
#         # --- assert the proper call signatures
#         self.assertEqual(get_config_mock.call_args_list, [call()])
#         self.assertEqual(_check_for_recognized_args_mock.call_args_list,
#                          [call()])
#         self.assertEqual(_io_in_adder_mock.call_args_list, config_call_list)
#         self.assertEqual(_io_out_adder_mock.call_args_list, config_call_list)
#         self.assertEqual(_decorating_adder_mock.call_args_list, plain_call_list)
#         self.assertEqual(_xy_adder_mock.call_args_list, plain_call_list)
#         self.assertEqual(_example_adder_mock.call_args_list, plain_call_list)
