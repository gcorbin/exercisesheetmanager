#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

import os_utils
from defaultlogger import set_default_logging_behavior
import exercisesheetmanager as esm

logger = logging.getLogger('ExerciseSheetManager.create_overview')

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    set_default_logging_behavior(logfile='create_overview')

    logger.debug('parsing args')
    parser = argparse.ArgumentParser(description='Create an exercise sheet '
                                                 'that contains all exercises in the course pool')
    parser.add_argument('-c', '--clean-after-build', action='store_true',
                        help='removes files created during building LaTex. Only pdf files remain.')
    parser.add_argument('--course-config', help='read in course config file', type=str, default='course.ini')

    build_sequence_group = parser.add_mutually_exclusive_group()
    build_sequence_group.add_argument('-b', '--build-sequence', type=str, default=None,
                                      help='The order in which latex("l") and bibtex("b") are called.')
    build_sequence_group.add_argument('-f', '--full', action='store_true', help='Equivalent to "-b lbll"')
    build_sequence_group.add_argument('-q', '--quick', action='store_true', help='Equivalent to "-b l"')
    build_sequence_group.add_argument('-n', '--no-build', action='store_true',
                                      help='Do not build anything. Equivalent to "-b"'
                                           'In combination with the "-c" option this is useful for cleaning up' 
                                           'auxiliary files from a previous run')
    args = parser.parse_args()
    build_sequence = esm.make_build_sequence(args)

    try:
        sheet_info = esm.load_course_info(args.course_config)
        sheet_info['compilename'] = 'overview'

        exercise_list = esm.list_pool(sheet_info['path_to_pool'])
        os_utils.make_directories_if_nonexistent(sheet_info['build_folder'])

        sheet = esm.ExerciseSheet(sheet_info, exercise_list)
        sheet.print_info()

        compile_name = sheet.render_latex_template(mode='exercise')
        sheet.build_latex_document(compile_name, build_sequence, args.clean_after_build)

        logger.info('Creation of %s successfull', sheet_info['compilename'])
    except Exception as ex:
        logger.critical('', exc_info=ex)
        sys.exit(1)
