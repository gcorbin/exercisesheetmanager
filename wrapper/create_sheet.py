# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# 1: load sheet data
# 2: parse latex template
# 3: compile latex file and create pdf

# additional parameters: config file, solutions n/y
# execute in command line:
# $ python create_sheet.py  SS18_inclass_sheet1.py -s n/y

import jinja2
import sys
import os
import argparse
import configparser


# -----------------------------------------------------------------------------


def load_sheet_data():
    parser = argparse.ArgumentParser(description='Create exercise sheet.')
    parser.add_argument('sheetinfo', type=str,
                        help='py file containing sheet information')
    parser.add_argument('-s', '--solutionflag', type=str, default='n',
                        help='n/y, if solution should be printed or not;\
                        default is n')
    args = parser.parse_args()

    if os.path.splitext(args.sheetinfo)[1] == '.ini':

        config = configparser.ConfigParser()
        config.read(args.sheetinfo)
        sheetinfo = config['sheet_info']
        inclass = config['inclass']
        homework = config['homework']
    else:
        raise ValueError('Filename needs to be in the <myfile.ini>!!!')
    try:
        sheetinfo['compilename']
        if args.solutionflag == 'y':
            sheetinfo['compilename'] += '_solution'
    except KeyError:
        print('You have to specify a filename for the compiled document!')
        sys.exit()

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
        inclass_list_extended.append(make_exercise_info(title,
                                                        sheetinfo['path_to_ex'] + filename + '.tex',
                                                        sheetinfo['path_to_sol'] + filename + '_solution.tex',
                                                        '0'))

    for (key, value) in homework.items():
        title, filename, points = [x.strip() for x in value.split('&&')]
        homework_list_extended.append(make_exercise_info(title,
                                                         sheetinfo['path_to_ex'] + filename + '.tex',
                                                         sheetinfo['path_to_sol'] + filename + '_solution.tex',
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
    # inserts inclass-block in latex document
    filled_string = '\\begin{Aufgabe}{' + ex_name + '} \n' \
                    + '\input{' + ex_source + '} \n \\end{Aufgabe} \n\n'
    return filled_string


def fill_latex_homework_macro(ex_name, ex_source, ex_points):
    # inserts homework-block in latex document
    if ex_points == 'no_discussion':
        filled_string = '\\begin{HausaufgabeNoDiscussion}{' + ex_name + '}' \
                     + ' \n \input{' + ex_source + '} \n \\end{Hausaufgabe} \n\n'
    else:
        filled_string = '\\begin{Hausaufgabe}{' + ex_name + '}{' + ex_points + '}' \
                        + ' \n \input{' + ex_source + '} \n \\end{Hausaufgabe} \n\n'
    return filled_string


def fill_latex_solution_macro(ex_source):
    # inserts solution-block in latex document
    filled_string = '\\begin{Loesung} \n' \
                    + '\input{' + ex_source + '} \n \\end{Loesung} \n\n'
    return filled_string


def render_latex_template(sheetinfo, inclass_list_extended, homework_list_extended, args):
    # Jinja2 magic to parse latex template
    latex_jinja_env = jinja2.Environment(variable_start_string='\VAR{',
                                         variable_end_string='}',
                                         autoescape=False,
                                         loader=jinja2.FileSystemLoader(os.path.abspath('.')))
    template = latex_jinja_env.get_template(sheetinfo['main_template'])

    inclass_list_tex = ''
    homework_list_tex = ''
    if args.solutionflag == 'y':
        # print also solutions
        for inclass_ex in inclass_list_extended:
            inclass_list_tex += fill_latex_inclass_macro(inclass_ex['title'],
                                                         inclass_ex['ex'])
            inclass_list_tex += fill_latex_solution_macro(inclass_ex['sol'])

        for homework_ex in homework_list_extended:
            homework_list_tex += fill_latex_homework_macro(homework_ex['title'],
                                                           homework_ex['ex'],
                                                           homework_ex['pt'])
            homework_list_tex += fill_latex_solution_macro(homework_ex['sol'])

    else:
        for inclass_ex in inclass_list_extended:
            inclass_list_tex += fill_latex_inclass_macro(inclass_ex['title'],
                                                         inclass_ex['ex'])
        for homework_ex in homework_list_extended:
            homework_list_tex += fill_latex_homework_macro(homework_ex['title'],
                                                           homework_ex['ex'],
                                                           homework_ex['pt'])

    # parse template
    output_from_rendered_template = template.render(course=sheetinfo.get('lecture', 'name of lecture'),
                                                    lecturer=sheetinfo.get('lecturer', 'name of lecturer'),
                                                    releasedate=sheetinfo.get('releasedate', 'released today'),
                                                    deadline=sheetinfo.get('deadline', 'today'),
                                                    sheetno=sheetinfo.get('sheetno', '0'),
                                                    sheetname=sheetinfo.get('sheetname', 'Blatt'),
                                                    disclaimer=sheetinfo.get('disclaimer', 'empty_disclaimer'),
                                                    deadlinetext=sheetinfo.get('deadlinetext', 'deadline: '),
                                                    path_to_sol=sheetinfo.get('path_to_sol', './'),
                                                    path_to_ex=sheetinfo.get('path_to_ex', './'),
                                                    inputlist=inclass_list_tex
                                                              + homework_list_tex)

    # remove old files from built folder
    old_files = os.listdir(sheetinfo.get('build_folder', './bld/'))
    for item in old_files:
        if item.startswith(sheetinfo['compilename'] + '.'):
            os.remove(os.path.join(sheetinfo.get('build_folder', './bld/'), item))

    # write to new file
    with open(sheetinfo.get('build_folder', './bld/') + sheetinfo['compilename'] + '.tex', 'w') as fh:
        fh.write(output_from_rendered_template)


def build_latex_document(sheetinfo):
    # build latex document
    latex_command = 'pdflatex -synctex=1 -interaction=nonstopmode ' \
              + ' --shell-escape --output-directory=' + sheetinfo.get('build_folder', './bld/') + ' ' \
              + sheetinfo.get('build_folder', './bld/') + sheetinfo['compilename'] + '.tex' + ' >/dev/null '
    bibtex_command =  'bibtex ' + sheetinfo.get('build_folder', './bld/') + sheetinfo['compilename'] + '.tex' +  '>/dev/null '
    print(latex_command)
    os.system(latex_command)
    print(bibtex_command)
    os.system(bibtex_command)
    print('compiled to: ' + sheetinfo['compilename'])

    print(latex_command)
    os.system(latex_command)
    print(latex_command)
    os.system(latex_command)

def cwd(path):
        print('hello')

        print(os.getcwd())
# -------- run script --------------------------------------------------------


if __name__ == '__main__':
    sheetinfo, inclass, homework, args = load_sheet_data()
    inclass_list_extended, homework_list_extended = make_exercise_lists(sheetinfo, inclass, homework)
    print_sheetinfo(sheetinfo, inclass_list_extended, homework_list_extended)
    oldpwd=os.getcwd()
    os.chdir(sheetinfo['tex_root'])
    try:
        if not os.path.exists(sheetinfo.get('build_folder', './bld/')):
            os.makedirs(sheetinfo.get('build_folder', './bld/'))
        render_latex_template(sheetinfo, inclass_list_extended, homework_list_extended, args)
        build_latex_document(sheetinfo)
    finally:
        os.chdir(oldpwd)

    print('\nScript finished :) \n')
