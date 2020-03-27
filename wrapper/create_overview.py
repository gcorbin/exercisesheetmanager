#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

import os
import os_utils
from defaultlogger import set_default_logging_behavior
import exercisesheetmanager as esm

logger = logging.getLogger('ExerciseSheetManager.create_overview')

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    set_default_logging_behavior(logfile='create_overview')

    logger.debug('parsing args')
    parser = argparse.ArgumentParser(description='Create an exercise sheet that contains all exercises in the course pool')
    parser.add_argument('-c', '--clean-after-build', action='store_true',
                        help='removes files created during building LaTex. Only pdf files remain.')
    parser.add_argument('--course-config', help='read in course config file', type=str, default='course.ini')
    args = parser.parse_args()

    try:
        config = esm.make_config()
        esm.load_course_data(config, args.course_config)
        sheet_info = config['sheet_info']
        sheet_info['compilename'] = 'overview'

        exercise_list = []
        exercises = os.listdir(sheet_info['path_to_pool'])
        for ex in exercises:
            ex_path = os.path.abspath(os.path.join(sheet_info['path_to_pool'], ex))
            if os.path.isdir(ex_path):
                task_tex_file = os.path.join(ex_path, 'task.tex')
                if not os.path.isfile(task_tex_file):
                    logger.debug('%s: File not found: %.s', key, task_tex_file)
                    logger.error('Skipping nonexistent exercise: %s.', exercise_name)
                    continue
                exercise_info_dict = {'id': ex,
                                      'name': ex,
                                      'type': 'inclass',
                                      'title': ex,
                                      'root_dir': ex_path,
                                      'task': task_tex_file,
                                      'solution': None,
                                      'annotation': None,
                                      'points': ''}
                exercise_list.append(exercise_info_dict)

        esm.print_sheet_info(sheet_info, exercise_list)
        os_utils.make_directories_if_nonexistent(sheet_info['build_folder'])

        sheet = esm.ExerciseSheet(sheet_info, exercise_list)

        compile_name = sheet.render_latex_template(mode='exercise')
        sheet.build_latex_document(compile_name, args.clean_after_build)

        logger.info('Creation of %s successfull', sheet_info['compilename'])
    except Exception as ex:
        logger.critical('', exc_info=ex)
        sys.exit(1)