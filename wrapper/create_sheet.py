# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# 1: load sheet data
# 2: parse latex template
# 3: compile latex file and create pdf

import jinja2
import sys
import os
import argparse
import configparser
import logging 
import subprocess

import tex_utils
import os_utils
from defaultlogger import set_default_logging_behavior

logger = logging.getLogger('ExerciseSheetManager.create_sheet')

# -----------------------------------------------------------------------------


def load_sheet_data():
    logger.info('Loading sheet data.')
    parser = argparse.ArgumentParser(description='Create exercise sheet.')
    parser.add_argument('sheetinfo', type=str,
                        help='py file containing sheet information')
    parser.add_argument('-e', '--build-exercise', action='store_true')
    parser.add_argument('-s', '--build-solution', action='store_true')
    parser.add_argument('-a', '--build-annotation', action='store_true')
    args = parser.parse_args()
    if not args.build_exercise and not args.build_solution and not args.build_annotation: 
        args.build_exercise = True

    if os.path.splitext(args.sheetinfo)[1] == '.ini':
        config = configparser.SafeConfigParser(interpolation=configparser.BasicInterpolation())
        if not os.path.isfile(args.sheetinfo):
            logger.critical('The ini file %s does not exist', args.sheetinfo)
            raise OSError('File not found %s', args.sheetinfo)
        config.read(args.sheetinfo)
        sheetinfo = config['sheet_info']
        sheetinfo['build_folder'] = sheetinfo.get('build_folder', './build/')
        sheetinfo['ini_name'] = os.path.splitext(os.path.split(args.sheetinfo)[1])[0] 
        exercises = config['exercises']
    else:
        raise ValueError('Filename needs to be in the <myfile.ini>!!!')
    if not config.has_option('sheet_info', 'compilename'):
        raise KeyError("The 'sheet_info.compilename' option must be set in the config file")

    return sheetinfo, exercises, args


def make_exercise_info_dict(title, ex, sol, pt, an):
    # data structure for exercise, consisting of
    # title, exercise file, solution file, string with points (e.g. 2+2)
    return {'title': title, 'ex': ex, 'sol': sol, 'pt': pt, 'annotation':an}


def make_exercise_lists(sheetinfo, exercises):
    exercise_list = []
    for (key, value) in exercises.items():
        exercise_info = [x.strip() for x in value.split('&&')]
        if len(exercise_info) < 2: 
            logger.error('Skipping exercise %s due to incomplete specification.', key)
            continue
        ex_type = exercise_info[0]
        if ex_type != 'homework' and ex_type != 'inclass':
            logger.error('%s: Unsupported exercise type "%s". Fallback to inclass.', key, ex_type)
            ex_type = 'inclass'
            
        exercise_name = exercise_info[1]            
        path_to_ex = os.path.abspath(os.path.join(sheetinfo['path_to_res'], exercise_name, 'exercise.tex'))
        path_to_sol = os.path.abspath(os.path.join(sheetinfo['path_to_res'], exercise_name, 'solution.tex'))
        path_to_ann = os.path.abspath(sheetinfo['ini_name'] + '_' + key + '.tex')
        
        if not os.path.isfile(path_to_ex): 
            logger.debug('%s: File not found: %.s', key, path_to_ex)
            logger.error('Skipping nonexistent exercise: %s.', exercise_name)
            continue
        if not os.path.isfile(path_to_sol): 
            logger.debug('%s: File not found: %s.', key, path_to_sol)
            logger.warning('The exercise %s does not have a solution.', exercise_name)
            path_to_sol = None
        if not os.path.isfile(path_to_ann): 
            logger.debug('%s: File not found: %s.', key, path_to_ann)
            logger.debug('%s: No annotation is attached to exercise %s.', key, exercise_name)
            path_to_ann = None
            
        if len(exercise_info) >= 3: 
            exercise_title = exercise_info[2]
        else:
            exercise_title = ''
        if len(exercise_info) >= 4: 
            exercise_points = exercise_info[3]
            if ex_type == 'inclass':
                logger.warning('%s: Points given for "inclass" exercise %s will be ignored.', key, exercise_name)
        else:
            exercise_points = ''
        if len(exercise_info) > 4: 
            logger.warning('%s: Extra arguments will be ignored.', key)
        exercise_info_dict = {'type': ex_type, 
                              'title': exercise_title,
                              'exercise': path_to_ex, 
                              'solution': path_to_sol,
                              'annotation': path_to_ann, 
                              'points': exercise_points}
        exercise_list.append(exercise_info_dict)
    return exercise_list


def print_sheetinfo(sheetinfo, exercise_list):
    # print information of sheet
    print('\n')
    print('lecture:\t\t' + sheetinfo.get('lecture', 'name of lecture'))
    print('lecturer:\t\t' + sheetinfo.get('lecturer', 'name of lecturer'))
    print('releasedate:\t\t' + sheetinfo.get('releasedate', 'released today'))
    print('deadlinetext:\t\t' + sheetinfo.get('deadlinetext', 'deadline: '))
    print('deadline:\t\t' + sheetinfo.get('deadline', 'today'))
    print('sheetno:\t\t' + sheetinfo.get('sheetno', '0'))
    print('sheetname:\t\t' + sheetinfo.get('sheetname',  'Blatt'))
    print('disclaimer:\t\t' + sheetinfo.get('disclaimer', 'empty_disclaimer'))
    print('compilename:\t\t' + sheetinfo['compilename'])
    print('resource:\t\t' + sheetinfo['path_to_res'])
    print('exercises:\t\t')
    for ex_info in exercise_list:
        print('\t\t\t' + ex_info['type'] + ' : ' + ex_info['title'])
    print('\n')


def fill_latex_exercise_macro(ex_info):
    if ex_info['type'] == 'homework': 
        return tex_utils.tex_environment('Hausaufgabe', 
                                         tex_utils.tex_command('input', [ex_info['exercise']]), 
                                         [ex_info['title'], ex_info['points']])
    elif ex_info['type'] == 'inclass': 
        return tex_utils.tex_environment('Aufgabe', 
                                         tex_utils.tex_command('input', [ex_info['exercise']]), 
                                         [ex_info['title']])
    else:
        raise ValueError('Unsupported exercise type %s', ex_info['type'])


def fill_latex_solution_macro(ex_info):
    if ex_info['solution'] is not None: 
        return tex_utils.tex_environment('Loesung',
                                         tex_utils.tex_command('input', [ex_info['solution']]))
    return ''


def fill_latex_annotation_macro(ex_info): 
    if ex_info['annotation'] is not None: 
        return tex_utils.tex_environment('Punkte', 
                                          tex_utils.tex_command('input', [ex_info['annotation']]))
    return ''


def render_latex_template(compilename, sheetinfo,
                          exercise_list,
                          render_solution, render_annotations):
    # Jinja2 magic to parse latex template
    latex_jinja_env = jinja2.Environment(variable_start_string='\VAR{',
                                         variable_end_string='}',
                                         autoescape=False,
                                         loader=jinja2.FileSystemLoader(sheetinfo['tex_root']))
    template = latex_jinja_env.get_template(sheetinfo['main_template'])

    exercise_list_tex = ''
    for ex_info in exercise_list:
        exercise_list_tex += fill_latex_exercise_macro(ex_info)
        if render_solution: 
            exercise_list_tex += fill_latex_solution_macro(ex_info)
        if render_annotations: 
            exercise_list_tex += fill_latex_annotation_macro(ex_info)

    class_options_list = []
    if render_solution: 
        class_options_list.append('Loesungen')
    if render_annotations: 
        class_options_list.append('Punkte')
    class_options = ','.join(class_options_list)
    # parse template
    output_from_rendered_template = template.render(classoptions=class_options,
                                                    course=sheetinfo.get('lecture', 'name of lecture'),
                                                    lecturer=sheetinfo.get('lecturer', 'name of lecturer'),
                                                    releasedate=sheetinfo.get('releasedate', 'released today'),
                                                    deadline=sheetinfo.get('deadline', 'today'),
                                                    sheetno=sheetinfo.get('sheetno', '0'),
                                                    sheetname=sheetinfo.get('sheetname', 'Blatt'),
                                                    disclaimer=sheetinfo.get('disclaimer', 'empty_disclaimer'),
                                                    deadlinetext=sheetinfo.get('deadlinetext', 'deadline: '),
                                                    path_to_res=os.path.abspath(sheetinfo.get('path_to_res', './')),
                                                    inputlist=exercise_list_tex)

    # remove old files from build folder
    old_files = os.listdir(sheetinfo['build_folder'])
    for item in old_files:
        if item.startswith(compilename + '.'):
            os.remove(os.path.join(sheetinfo['build_folder'], item))

    # write to new file
    with open(os.path.join(sheetinfo['build_folder'], compilename + '.tex'), 'w') as fh:
        fh.write(output_from_rendered_template)


def build_latex_document(compilename, sheetinfo):
    build_dir = os.path.abspath(sheetinfo['build_folder'])
    build_file = os.path.join(build_dir, compilename)
    
    # build latex document
    latex_command = ['pdflatex', '-synctex=1', '-interaction=nonstopmode', '--shell-escape',
                    '--output-directory='+build_dir, build_file]
    
    bibtex_command = ['bibtex', compilename]
    
    logger.info('Compiling Latex Document %s', compilename)
    logger.debug('Latex command %s', latex_command)
    logger.debug('bibtex_command %s', bibtex_command)
    
    try: 
        FNULL = open(os.devnull, 'w')
        with os_utils.ChangedDirectory(sheetinfo['tex_root']): 
            logger.info('Latex: first run')
            subprocess.check_call(latex_command, stdout=FNULL)
        with os_utils.ChangedDirectory(build_dir):
            logger.info('Bibtex')
            status = subprocess.call(bibtex_command, stdout=FNULL)
        if status != 0: 
            logger.warning('Bibtex command exited with error. Status %s', status)
        with os_utils.ChangedDirectory(sheetinfo['tex_root']): 
            logger.info('Latex: second run')
            subprocess.check_call(latex_command, stdout=FNULL)
            logger.info('Latex: third run')
            subprocess.check_call(latex_command, stdout=FNULL)
        
    except subprocess.CalledProcessError as ex:
        logger.error('Error during compilation of latex document. Exit status: %s', ex.returncode)
        logger.info('Errors from latex log file follow:')
        try: 
            with open(build_file + '.log', 'r') as texlog: 
                try: 
                    while True: 
                        line = texlog.next()
                        if line.startswith('!'): 
                            logger.info(line.strip())
                            i = 0
                            while i < 5: 
                                line = texlog.next()
                                logger.info(line.strip())
                                if line.startswith('!'):
                                    i = 0
                                else: 
                                    i += 1
                except StopIteration:
                    pass
        except OSError: 
            logger.warning('Could not open tex log file %s', os.path.join(build_file,'.log'))
        raise ex


if __name__ == '__main__':
    set_default_logging_behavior(logfile='create_sheet')
    
    try: 
        sheetinfo, exercises, args = load_sheet_data()
        exercise_list = make_exercise_lists(sheetinfo, exercises)
        print_sheetinfo(sheetinfo, exercise_list)
        
        os_utils.make_directories_if_nonexistent(sheetinfo['build_folder'])
        
        if args.build_exercise: 
            compilename = sheetinfo['compilename']
            render_latex_template(compilename, sheetinfo, exercise_list,
                                  render_solution=False, render_annotations=False)   
            build_latex_document(compilename, sheetinfo)        
        if args.build_solution: 
            compilename = sheetinfo['compilename'] + '_solution'
            render_latex_template(compilename, sheetinfo, exercise_list, 
                                  render_solution=True, render_annotations=False)
            build_latex_document(compilename, sheetinfo)
        if args.build_annotation:
            compilename = sheetinfo['compilename'] + '_annotation'
            render_latex_template(compilename, sheetinfo, exercise_list, 
                                  render_solution=True, render_annotations=True)
            build_latex_document(compilename, sheetinfo)
            
        logger.info('Creation of %s successfull', sheetinfo['compilename'])
    except Exception as ex:
        logger.critical('', exc_info=ex)
        sys.exit(1)