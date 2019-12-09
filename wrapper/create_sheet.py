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
        config = configparser.SafeConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read(args.sheetinfo)
        sheetinfo = config['sheet_info']
        sheetinfo['build_folder'] = sheetinfo.get('build_folder', './build/')
        inclass = config['inclass']
        homework = config['homework']
    else:
        raise ValueError('Filename needs to be in the <myfile.ini>!!!')
    if not config.has_option('sheet_info', 'compilename'):
        raise KeyError("The 'sheet_info.compilename' option must be set in the config file")

    return sheetinfo, inclass, homework, args


def make_exercise_info(title, ex, sol, pt):
    # data structure for exercise, consisting of
    # title, exercise file, solution file, string with points (e.g. 2+2)
    return {'title': title, 'ex': ex, 'sol': sol, 'pt': pt}


def make_exercise_lists(sheetinfo, inclass, homework):
    # empty dictionary, for extended dictionary with solution
    # 0 points for inclass, won't be printed paths
    inclass_list_extended = []
    homework_list_extended = []
    for (key, value) in inclass.items():
        title, filename = [x.strip() for x in value.split('&&')]        
        path_to_ex = os.path.abspath(os.path.join(sheetinfo['path_to_res'], filename, 'exercise.tex'))
        path_to_sol = os.path.abspath(os.path.join(sheetinfo['path_to_res'], filename, 'solution.tex'))
        inclass_list_extended.append(make_exercise_info(title,
                                                        path_to_ex,
                                                        path_to_sol,
                                                        '0'))

    for (key, value) in homework.items():
        title, filename, points = [x.strip() for x in value.split('&&')]
        path_to_ex = os.path.abspath(os.path.join(sheetinfo['path_to_res'], filename, 'exercise.tex'))
        path_to_sol = os.path.abspath(os.path.join(sheetinfo['path_to_res'], filename, 'solution.tex'))
        homework_list_extended.append(make_exercise_info(title,
                                                         path_to_ex,
                                                         path_to_sol,
                                                         points))

    return inclass_list_extended, homework_list_extended


def print_sheetinfo(sheetinfo, inclass_list_extended, homework_list_extended):
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
    print('inclass_src:\t\t')
    for inclass_ex in inclass_list_extended:
        print('\t\t\t' + inclass_ex['ex'])
    print('homework_src:\t\t')
    for homework_ex in homework_list_extended:
        print('\t\t\t' + homework_ex['ex'])
    print('\n')


def fill_latex_inclass_macro(ex_name, ex_source):
    return tex_utils.tex_environment('Aufgabe',
                                 [tex_utils.tex_command('input', [ex_source])],
                                 [ex_name])


def fill_latex_homework_macro(ex_name, ex_source, ex_points):
    if ex_points == 'no_discussion': 
       return tex_utils.tex_environment('HausaufgabeNoDiscussion', 
                                  tex_utils.tex_command('input', [ex_source]), 
                                  [ex_name])
    else:
        return tex_utils.tex_environment('Hausaufgabe', 
                                  tex_utils.tex_command('input', [ex_source]), 
                                  [ex_name, ex_points])


def fill_latex_solution_macro(ex_source):
    return tex_utils.tex_environment('Loesung',
                                     tex_utils.tex_command('input', [ex_source]))
                                     

def render_latex_template(compilename, sheetinfo, inclass_list_extended, homework_list_extended, render_solution):
    # Jinja2 magic to parse latex template
    latex_jinja_env = jinja2.Environment(variable_start_string='\VAR{',
                                         variable_end_string='}',
                                         autoescape=False,
                                         loader=jinja2.FileSystemLoader(sheetinfo['tex_root']))
    template = latex_jinja_env.get_template(sheetinfo['main_template'])

    inclass_list_tex = ''
    homework_list_tex = ''
    for inclass_ex in inclass_list_extended:
        inclass_list_tex += fill_latex_inclass_macro(inclass_ex['title'],
                                                        inclass_ex['ex'])
        if render_solution:
            inclass_list_tex += '\n'
            inclass_list_tex += fill_latex_solution_macro(inclass_ex['sol'])

    for homework_ex in homework_list_extended:
        homework_list_tex += fill_latex_homework_macro(homework_ex['title'],
                                                        homework_ex['ex'],
                                                        homework_ex['pt'])
        if render_solution:
            homework_list_tex += '\n'
            homework_list_tex += fill_latex_solution_macro(homework_ex['sol'])

    # parse template
    output_from_rendered_template = template.render(course=sheetinfo.get('lecture', 'name of lecture'),
                                                    lecturer=sheetinfo.get('lecturer', 'name of lecturer'),
                                                    releasedate=sheetinfo.get('releasedate', 'released today'),
                                                    deadline=sheetinfo.get('deadline', 'today'),
                                                    sheetno=sheetinfo.get('sheetno', '0'),
                                                    sheetname=sheetinfo.get('sheetname', 'Blatt'),
                                                    disclaimer=sheetinfo.get('disclaimer', 'empty_disclaimer'),
                                                    deadlinetext=sheetinfo.get('deadlinetext', 'deadline: '),
                                                    path_to_res=os.path.abspath(sheetinfo.get('path_to_res', './')),
                                                    inputlist=inclass_list_tex
                                                              + homework_list_tex)

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
        sheetinfo, inclass, homework, args = load_sheet_data()
        inclass_list_extended, homework_list_extended = make_exercise_lists(sheetinfo, inclass, homework)
        print_sheetinfo(sheetinfo, inclass_list_extended, homework_list_extended)
        
        os_utils.make_directories_if_nonexistent(sheetinfo['build_folder'])
        
        if args.build_exercise: 
            compilename = sheetinfo['compilename']
            render_latex_template(compilename, sheetinfo, inclass_list_extended, homework_list_extended, render_solution=False)   
            build_latex_document(compilename, sheetinfo)        
        if args.build_solution: 
            compilename = sheetinfo['compilename'] + '_solution'
            render_latex_template(compilename, sheetinfo, inclass_list_extended, homework_list_extended, render_solution=True)
            build_latex_document(compilename, sheetinfo)
        if args.build_annotation:
            logger.warning('Annotation not implemented yet')
            
        logger.info('Creation of %s successfull', sheetinfo['compilename'])
    except Exception as ex:
        logger.critical('', exc_info=ex)
        sys.exit(1)