import jinja2
import sys
import os
import configparser
import logging
import subprocess

import tex_utils
import os_utils

logger = logging.getLogger('ExerciseSheetManager')

def is_valid_ini_file(file_name):
    return os.path.splitext(file_name)[1] == '.ini' and os.path.isfile(file_name)


def load_sheet_data(args):
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    if args.course_config is not None and is_valid_ini_file(args.course_config):
        logger.info('Loading default options from %s', args.course_config)
        config.read(args.course_config)
    else:
        logger.info('Did not find a valid course config file. Skipping.')
    logger.info('Loading sheet data.')
    if not is_valid_ini_file(args.sheetinfo):
        logger.critical('The file %s does not exist or is not an .ini file', args.sheetinfo)
        raise OSError('Invalid file %s: does not exist or is not a .ini file', args.sheetinfo)
    config.read(args.sheetinfo)
    sheet_info = config['sheet_info']
    sheet_info['language'] = sheet_info.get('language', 'german')
    sheet_info['disclaimer'] = sheet_info.get('disclaimer', '')
    sheet_info['build_folder'] = sheet_info.get('build_folder', './build/')
    sheet_info['ini_name'] = os.path.splitext(os.path.split(args.sheetinfo)[1])[0]
    exercises_info = config['exercises']

    if not config.has_option('sheet_info', 'compilename'):
        raise KeyError("The 'sheet_info.compilename' option must be set in the config file")

    return sheet_info, exercises_info


def make_exercise_list(sheet_info, exercises_info):
    exercise_list = []
    for (key, value) in exercises_info.items():
        exercise = [x.strip() for x in value.split('&&')]
        if len(exercise) < 2:
            logger.error('Skipping exercise %s due to incomplete specification.', key)
            continue
        task_type = exercise[0]
        if task_type != 'homework' and task_type != 'inclass':
            logger.error('%s: Unsupported task type "%s". Fallback to inclass.', key, task_type)
            task_type = 'inclass'

        exercise_name = exercise[1]
        exercise_dir = os.path.abspath(os.path.join(sheet_info['path_to_pool'], exercise_name))

        task_tex_file = os.path.join(exercise_dir, 'task.tex')
        if not os.path.isfile(task_tex_file):
            logger.debug('%s: File not found: %.s', key, task_tex_file)
            logger.error('Skipping nonexistent exercise: %s.', exercise_name)
            continue

        solution_tex_file = os.path.join(exercise_dir, 'solution.tex')
        if not os.path.isfile(solution_tex_file):
            logger.debug('%s: File not found: %s.', key, solution_tex_file)
            logger.warning('The exercise %s does not have a solution.', exercise_name)
            solution_tex_file = None

        annotation_tex_file = os.path.abspath(sheet_info['ini_name'] + '_' + key + '.tex')
        if not os.path.isfile(annotation_tex_file):
            logger.debug('%s: File not found: %s.', key, annotation_tex_file)
            logger.debug('%s: No annotation is attached to exercise %s.', key, exercise_name)
            annotation_tex_file = None

        if len(exercise) >= 3:
            task_title = exercise[2]
        else:
            task_title = ''
        if len(exercise) >= 4:
            task_points = exercise[3]
            if task_type == 'inclass':
                logger.warning('%s: Points given for "inclass" task %s will be ignored.', key, exercise_name)
        else:
            task_points = ''
        if len(exercise) > 4:
            logger.warning('%s: Extra arguments will be ignored.', key)
        exercise_info_dict = {'id': key,
                              'name': exercise_name,
                              'type': task_type,
                              'title': task_title,
                              'root_dir': exercise_dir,
                              'task': task_tex_file,
                              'solution': solution_tex_file,
                              'annotation': annotation_tex_file,
                              'points': task_points}
        exercise_list.append(exercise_info_dict)
    return exercise_list


def print_sheet_info(sheet_info, exercise_list):
    print('\n')
    print('lecture:\t\t' + sheet_info.get('lecture', 'name of lecture'))
    print('lecturer:\t\t' + sheet_info.get('lecturer', 'name of lecturer'))
    print('releasedate:\t\t' + sheet_info.get('releasedate', 'released today'))
    print('deadline:\t\t' + sheet_info.get('deadline', 'today'))
    print('sheetno:\t\t' + sheet_info.get('sheetno', '0'))
    print('sheetname:\t\t' + sheet_info.get('sheetname', 'exercise'))
    print('disclaimer:\t\t' + sheet_info.get('disclaimer', 'empty_disclaimer'))
    print('compilename:\t\t' + sheet_info['compilename'])
    print('resource:\t\t' + sheet_info['path_to_pool'])
    print('tasks:\t\t')
    for exercise_info in exercise_list:
        ex_info_str = exercise_info['id'] + ' : ' + exercise_info['name'] + ' : ' + exercise_info['type'] + '("' + \
                      exercise_info['title']
        if exercise_info['type'] == 'homework':
            ex_info_str += '" , "' + exercise_info['points']
        ex_info_str += '")' + ' : '
        if exercise_info['solution'] is not None:
            ex_info_str += 'solution'
        else:
            ex_info_str += 'no solution'
        ex_info_str += ' , '
        if exercise_info['annotation'] is not None:
            ex_info_str += 'annotation'
        else:
            ex_info_str += 'no annotation'
        print('\t\t\t' + ex_info_str)
    print('\n')


class ExerciseSheet:
    def __init__(self, sheet_info, exercise_list):
        self.sheet_info = sheet_info
        self.exercise_list = exercise_list

    def fill_latex_task_macro(self, exercise_info):
        if exercise_info['type'] == 'homework':
            return tex_utils.tex_command('inputHomework',
                                         [exercise_info['root_dir'], exercise_info['title'], exercise_info['points']])
        elif exercise_info['type'] == 'inclass':
            return tex_utils.tex_command('inputInclass', [exercise_info['root_dir'], exercise_info['title']])
        else:
            raise ValueError('Unsupported task type %s', exercise_info['type'])

    def fill_latex_solution_macro(self, exercise_info):
        if exercise_info['solution'] is not None:
            return tex_utils.tex_command('inputSolution', [exercise_info['root_dir']])
        return ''

    def fill_latex_annotation_macro(self, exercise_info):
        if exercise_info['annotation'] is not None:
            return tex_utils.tex_command('inputAnnotation', [exercise_info['annotation']])
        return ''

    def render_latex_template(self, mode='exercise'):
        render_solution = False
        render_annotation = False
        if mode == 'exercise':
            compile_name = self.sheet_info['compilename']
        elif mode == 'solution':
            compile_name = self.sheet_info['compilename'] + '_solution'
            render_solution = True
        elif mode == 'annotation':
            compile_name = self.sheet_info['compilename'] + '_annotation'
            render_solution = True
            render_annotation = True
        else:
            raise ValueError('Unknown mode "%s". Mode must be exercise, solution, or annotation', mode)

        # Jinja2 magic to parse latex template
        latex_jinja_env = jinja2.Environment(variable_start_string='\VAR{',
                                             variable_end_string='}',
                                             autoescape=False,
                                             loader=jinja2.FileSystemLoader(self.sheet_info['tex_root']))
        template = latex_jinja_env.get_template(self.sheet_info['main_template'])

        disclaimer_tex = ''
        if self.sheet_info['disclaimer'] != '':
            disclaimer_file = os.path.abspath(self.sheet_info['disclaimer'])
            disclaimer_tex = tex_utils.tex_command('input', [disclaimer_file])

        exercise_list_tex = ''
        for exercise_info in self.exercise_list:
            exercise_list_tex += self.fill_latex_task_macro(exercise_info) + '\n'
            if render_solution:
                exercise_list_tex += self.fill_latex_solution_macro(exercise_info) + '\n'
            if render_annotation:
                exercise_list_tex += self.fill_latex_annotation_macro(exercise_info) + '\n'

        class_options_list = []
        if render_solution:
            class_options_list.append('solutions')
        if render_annotation:
            class_options_list.append('annotations')
        class_options_list.append(self.sheet_info['language'])
        class_options = ','.join(class_options_list)
        # parse template
        output_from_rendered_template = template.render(classoptions=class_options,
                                                        course=self.sheet_info.get('lecture', 'name of lecture'),
                                                        semester=self.sheet_info.get('semester', 'semester'),
                                                        lecturer=self.sheet_info.get('lecturer', 'name of lecturer'),
                                                        releasedate=self.sheet_info.get('releasedate',
                                                                                        'released today'),
                                                        deadline=self.sheet_info.get('deadline', 'today'),
                                                        sheetno=self.sheet_info.get('sheetno', '0'),
                                                        sheetname=self.sheet_info.get('sheetname', 'Blatt'),
                                                        disclaimer=disclaimer_tex,
                                                        path_to_pool=os.path.abspath(
                                                            self.sheet_info.get('path_to_pool', './')),
                                                        inputlist=exercise_list_tex)

        self.clear_dir(compile_name, except_pdf=False)
        # write to new file
        tex_file = os.path.join(self.sheet_info['build_folder'], compile_name + '.tex')
        with open(tex_file, 'w') as fh:
            fh.write(output_from_rendered_template)
        return compile_name

    def build_latex_document(self, compile_name, clean_after_build=False):
        build_dir = os.path.abspath(self.sheet_info['build_folder'])
        build_file = os.path.join(build_dir, compile_name)
        latex_command = ['pdflatex', '-synctex=1', '-interaction=nonstopmode', '--shell-escape',
                         '--output-directory=' + build_dir, build_file]
        bibtex_command = ['bibtex', compile_name]

        logger.info('Compiling Latex Document %s', compile_name)
        logger.debug('Latex command %s', latex_command)
        logger.debug('bibtex_command %s', bibtex_command)

        try:
            FNULL = open(os.devnull, 'w')
            with os_utils.ChangedDirectory(self.sheet_info['tex_root']):
                logger.info('Latex: first run')
                subprocess.check_call(latex_command, stdout=FNULL)
            with os_utils.ChangedDirectory(build_dir):
                logger.info('Bibtex')
                status = subprocess.call(bibtex_command, stdout=FNULL)
            if status != 0:
                logger.warning('Bibtex command exited with error. Status %s', status)
            with os_utils.ChangedDirectory(self.sheet_info['tex_root']):
                logger.info('Latex: second run')
                subprocess.check_call(latex_command, stdout=FNULL)
                logger.info('Latex: third run')
                subprocess.check_call(latex_command, stdout=FNULL)

        except subprocess.CalledProcessError as ex:
            logger.error('Error during compilation of latex document. Exit status: %s', ex.returncode)
            logger.info('Errors from latex log file follow:')
            try:
                # go through the latex log file line by line
                # when a line starts with '!', it is a latex error
                # display the line and the following lines for context
                with open(build_file + '.log', 'r', encoding="utf8", errors='ignore') as texlog:

                    line = texlog.readline()
                    while line:
                        if line.startswith('!'):
                            logger.info(line.strip())
                            i = 0
                            while i < 5:
                                line = texlog.readline()
                                logger.info(line.strip())
                                if line.startswith('!'):
                                    i = 0
                                else:
                                    i += 1
                        line = texlog.readline()
                sys.exit(1)
            except OSError:
                logger.warning('Could not open tex log file %s', os.path.join(build_file, '.log'))
            raise ex

        if clean_after_build:
            self.clear_dir(compile_name, except_pdf=True)

    def clear_dir(self, compile_name, except_pdf=False):
        logger.debug('Removing files for %s. Keep pdf = %s. Folder: %s', compile_name, except_pdf,
                     self.sheet_info['build_folder'])
        old_files = os.listdir(self.sheet_info['build_folder'])
        for item in old_files:
            item_name, item_ext = os.path.splitext(item)
            if item.startswith(compile_name + '.'):
                if not except_pdf or not item_ext == '.pdf':
                    os.remove(os.path.join(self.sheet_info['build_folder'], item))
