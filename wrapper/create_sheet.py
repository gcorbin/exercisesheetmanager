#! /usr/bin/python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# 1: load sheet data
# 2: parse latex template
# 3: compile latex file and create pdf

import sys
import argparse
import logging

import os_utils
from defaultlogger import set_default_logging_behavior
import exercisesheetmanager as esm

logger = logging.getLogger('ExerciseSheetManager.create_sheet')

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    set_default_logging_behavior(logfile='create_sheet')
    
    logger.debug('parsing args')
    parser = argparse.ArgumentParser(description='Create exercise sheet.')
    parser.add_argument('sheetinfo', type=str,
                        help='py file containing sheet information')
    parser.add_argument('-e', '--build-exercise', action='store_true')
    parser.add_argument('-s', '--build-solution', action='store_true')
    parser.add_argument('-a', '--build-annotation', action='store_true')
    parser.add_argument('-c', '--clean-after-build', action='store_true',
                        help='removes files created during building LaTex. Only pdf files remain.')
    parser.add_argument('--course-config', help='read in course config file', type=str, default='course.ini')
    parser.add_argument('-x', '--export', type=str, default=None, help='Export everything into the given folder')
    args = parser.parse_args()
    '''if not args.build_exercise and not args.build_solution and not args.build_annotation:
        args.build_exercise = True'''
    
    try:
        sheet_info, exercises_info = esm.load_sheet_and_exercise_info(args.course_config, args.sheetinfo)
        exercise_list = esm.make_exercise_list(sheet_info, exercises_info)

        if args.export is not None:
            logger.info('Exporting to %s', args.export)
            sheet_info_export = esm.patch_for_export(sheet_info, args.export)
            esm.export_data(sheet_info, sheet_info_export, exercise_list)
            sheet_info = dict(sheet_info_export)
            with os_utils.ChangedDirectory(sheet_info['export_root']):
                exercise_list = esm.make_exercise_list(sheet_info, exercises_info)

        os_utils.make_directories_if_nonexistent(sheet_info['build_folder'])

        sheet = esm.ExerciseSheet(sheet_info, exercise_list)
        sheet.print_info()

        if args.build_exercise:
            compile_name = sheet.render_latex_template(mode='exercise')
            sheet.build_latex_document(compile_name, args.clean_after_build)
        if args.build_solution:
            compile_name = sheet.render_latex_template(mode='solution')
            sheet.build_latex_document(compile_name, args.clean_after_build)
        if args.build_annotation:
            compile_name = sheet.render_latex_template(mode='annotation')
            sheet.build_latex_document(compile_name, args.clean_after_build)

        logger.info('Creation of %s successfull', sheet_info['compilename'])
    except Exception as ex:
        logger.critical('', exc_info=ex)
        sys.exit(1)
