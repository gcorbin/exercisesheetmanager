#! /usr/bin/python
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
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        if not os.path.isfile(args.sheetinfo):
            logger.critical('The ini file %s does not exist', args.sheetinfo)
            raise OSError('File not found %s', args.sheetinfo)
        config.read(args.sheetinfo)
        sheetinfo = config['sheet_info']
        sheetinfo['language'] = sheetinfo.get('language', 'German')
        sheetinfo['disclaimer'] = sheetinfo.get('disclaimer', '')
        sheetinfo['build_folder'] = sheetinfo.get('build_folder', './build/')
        sheetinfo['ini_name'] = os.path.splitext(os.path.split(args.sheetinfo)[1])[0] 
        exercises = config['exercises']
    else:
        raise ValueError('Filename needs to be in the <myfile.ini>!!!')
    if not config.has_option('sheet_info', 'compilename'):
        raise KeyError("The 'sheet_info.compilename' option must be set in the config file")

    return sheetinfo, exercises, args

def load_texclass_wrapper( path ):
    
    logger.debug('Loading tex class info.')
    file = path + '/texclass_wrapper.ini'
    if os.path.isfile( file ): 
         cls_wrapper = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
         cls_wrapper.read(file)
    else:
        logger.critical('The ini file %s does not exist', file)
        raise OSError('File not found %s', file)
        
    return cls_wrapper

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
        assignment_path = os.path.abspath(os.path.join(sheetinfo['path_to_pool'], exercise_name))
        exercise_file = os.path.join(assignment_path, 'exercise.tex')
        solution_file = os.path.join(assignment_path, 'solution.tex')
        annotation_file = os.path.abspath(sheetinfo['ini_name'] + '_' + key + '.tex')
        
        if not os.path.isfile(exercise_file):
            logger.debug('%s: File not found: %.s', key, exercise_file)
            logger.error('Skipping nonexistent exercise: %s.', exercise_name)
            continue
        if not os.path.isfile(solution_file):
            logger.debug('%s: File not found: %s.', key, solution_file)
            logger.warning('The exercise %s does not have a solution.', exercise_name)
            solution_file = None
        if not os.path.isfile(annotation_file):
            logger.debug('%s: File not found: %s.', key, annotation_file)
            logger.debug('%s: No annotation is attached to exercise %s.', key, exercise_name)
            annotation_file = None
            
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
                              'assignment':assignment_path,
                              'exercise':exercise_file,
                              'solution':solution_file,
                              'annotation': annotation_file,
                              'points': exercise_points}
        exercise_list.append(exercise_info_dict)
    return exercise_list


def print_sheetinfo(sheetinfo, exercise_list):
    print('\n')
    print('lecture:\t\t' + sheetinfo.get('lecture', 'name of lecture'))
    print('lecturer:\t\t' + sheetinfo.get('lecturer', 'name of lecturer'))
    print('releasedate:\t\t' + sheetinfo.get('releasedate', 'released today'))
    print('deadline:\t\t' + sheetinfo.get('deadline', 'today'))
    print('sheetno:\t\t' + sheetinfo.get('sheetno', '0'))
    print('sheetname:\t\t' + sheetinfo.get('sheetname',  'Blatt'))
    print('disclaimer:\t\t' + sheetinfo.get('disclaimer', 'empty_disclaimer'))
    print('compilename:\t\t' + sheetinfo['compilename'])
    print('resource:\t\t' + sheetinfo['path_to_pool'])
    print('exercises:\t\t')
    for ex_info in exercise_list:
        print('\t\t\t' + ex_info['type'] + ' : ' + ex_info['title'])
    print('\n')

class Sheet:
    def __init__(self, sheetinfo,
                 exercise_list, cls_wrapper):
        self.sheetinfo = sheetinfo
        self.exercise_list = exercise_list
        self.cls_wrapper = cls_wrapper
        
    def fill_latex_exercise_macro(self, ex_info):
        if ex_info['type'] == 'homework':
            return tex_utils.tex_command('inputHausaufgabe', [ex_info['assignment'], ex_info['title'], ex_info['points']])
        elif ex_info['type'] == 'inclass':
            return tex_utils.tex_command('inputAufgabe', [ex_info['assignment'], ex_info['title']])
        else:
            raise ValueError('Unsupported exercise type %s', ex_info['type'])


    def fill_latex_solution_macro(self, ex_info):
        if ex_info['solution'] is not None:
            return tex_utils.tex_command('inputLoesung', [ex_info['assignment']])
        return ''


    def fill_latex_annotation_macro(self, ex_info): 
        if ex_info['annotation'] is not None:
            return tex_utils.tex_command('inputPunkte', [ex_info['annotation']])
        return ''


    def render_latex_template(self, render_solution, render_annotations):
        # Jinja2 magic to parse latex template
        latex_jinja_env = jinja2.Environment(variable_start_string='\VAR{',
                                             variable_end_string='}',
                                             autoescape=False,
                                             loader=jinja2.FileSystemLoader(self.sheetinfo['tex_root']))
        template = latex_jinja_env.get_template(self.sheetinfo['main_template'])
        
        disclaimer_tex = ''
        if self.sheetinfo['disclaimer'] != '': 
            disclaimer_file = os.path.abspath(self.sheetinfo['disclaimer'])
            disclaimer_tex = tex_utils.tex_command('input', [disclaimer_file])
    
        exercise_list_tex = ''
        for ex_info in self.exercise_list:
            exercise_list_tex += self.fill_latex_exercise_macro(ex_info)
            if render_solution: 
                exercise_list_tex += self.fill_latex_solution_macro(ex_info)
            if render_annotations: 
                exercise_list_tex += self.fill_latex_annotation_macro(ex_info)
    
        class_options_list = []
        if render_solution: 
            class_options_list.append(self.cls_wrapper['class_option']['show_solution'])
        if render_annotations: 
            class_options_list.append(self.cls_wrapper['class_option']['show_annotation'])
        class_options_list.append(self.sheetinfo['language'])
        class_options = ','.join(class_options_list)
        # parse template
        output_from_rendered_template = template.render(classoptions=class_options,
                                                        course=self.sheetinfo.get('lecture', 'name of lecture'),
                                                        semester=self.sheetinfo.get('semester', 'semester'),
                                                        lecturer=self.sheetinfo.get('lecturer', 'name of lecturer'),
                                                        releasedate=self.sheetinfo.get('releasedate', 'released today'),
                                                        deadline=self.sheetinfo.get('deadline', 'today'),
                                                        sheetno=self.sheetinfo.get('sheetno', '0'),
                                                        sheetname=self.sheetinfo.get('sheetname', 'Blatt'),
                                                        disclaimer=disclaimer_tex,
                                                        path_to_pool=os.path.abspath(self.sheetinfo.get('path_to_pool', './')),
                                                        inputlist=exercise_list_tex)
    
        # remove old files from build folder
        old_files = os.listdir(self.sheetinfo['build_folder'])
        for item in old_files:
            if item.startswith(self.compilename + '.'):
                os.remove(os.path.join(self.sheetinfo['build_folder'], item))
    
        # write to new file
        with open(os.path.join(self.sheetinfo['build_folder'], self.compilename + '.tex'), 'w') as fh:
            fh.write(output_from_rendered_template)


    def build_latex_document(self):
        build_dir = os.path.abspath(self.sheetinfo['build_folder'])
        build_file = os.path.join(build_dir, self.compilename)
        latex_command = ['pdflatex', '-synctex=1', '-interaction=nonstopmode', '--shell-escape',
                        '--output-directory='+build_dir, build_file]    
        bibtex_command = ['bibtex', self.compilename]
        
        logger.info('Compiling Latex Document %s', self.compilename)
        logger.debug('Latex command %s', latex_command)
        logger.debug('bibtex_command %s', bibtex_command)
        
        try: 
            FNULL = open(os.devnull, 'w')
            with os_utils.ChangedDirectory(self.sheetinfo['tex_root']): 
                logger.info('Latex: first run')
                subprocess.check_call(latex_command, stdout=FNULL)
            with os_utils.ChangedDirectory(build_dir):
                logger.info('Bibtex')
                status = subprocess.call(bibtex_command, stdout=FNULL)
            if status != 0: 
                logger.warning('Bibtex command exited with error. Status %s', status)
            with os_utils.ChangedDirectory(self.sheetinfo['tex_root']): 
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
                logger.warning('Could not open tex log file %s', os.path.join(build_file,'.log'))
            raise ex


if __name__ == '__main__':
    set_default_logging_behavior(logfile='create_sheet')
    
    try: 
        sheetinfo, exercises, args = load_sheet_data()
        exercise_list = make_exercise_lists(sheetinfo, exercises)
        print_sheetinfo(sheetinfo, exercise_list)
        
        os_utils.make_directories_if_nonexistent(sheetinfo['build_folder'])
        
        cls_wrapper = load_texclass_wrapper(sheetinfo['tex_root'])
         
        sheet = Sheet(sheetinfo, exercise_list, cls_wrapper)
        
        if args.build_exercise: 
            sheet.compilename = sheetinfo['compilename']
            sheet.render_latex_template( render_solution=False,
                                         render_annotations=False)   
            sheet.build_latex_document()        
        if args.build_solution: 
            sheet.compilename = sheetinfo['compilename'] + '_solution'
            sheet.render_latex_template( render_solution=True,
                                         render_annotations=False)
            sheet.build_latex_document()    
        if args.build_annotation:
            sheet.compilename = sheetinfo['compilename'] + '_annotation'
            sheet.render_latex_template( render_solution=True,
                                         render_annotations=True)
            sheet.build_latex_document()
            
        logger.info('Creation of %s successfull', sheetinfo['compilename'])
    except Exception as ex:
        logger.critical('', exc_info=ex)
        sys.exit(1)