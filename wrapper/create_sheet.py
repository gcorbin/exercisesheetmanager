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


def load_sheet_data(args):
    logger.info('Loading sheet data.')
    
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
        tasks = config['tasks']
    else:
        raise ValueError('Filename needs to be in the <myfile.ini>!!!')
    if not config.has_option('sheet_info', 'compilename'):
        raise KeyError("The 'sheet_info.compilename' option must be set in the config file")

    return sheetinfo, tasks

def make_task_list(sheetinfo, tasks):
    task_list = []
    for (key, value) in tasks.items():
        task_info = [x.strip() for x in value.split('&&')]
        if len(task_info) < 2: 
            logger.error('Skipping task %s due to incomplete specification.', key)
            continue
        task_type = task_info[0]
        if task_type != 'homework' and task_type != 'inclass':
            logger.error('%s: Unsupported task type "%s". Fallback to inclass.', key, task_type)
            task_type = 'inclass'
            
        task_name = task_info[1]            
        task_dir = os.path.abspath(os.path.join(sheetinfo['path_to_pool'], task_name))
        task_tex_file = os.path.join(task_dir, 'exercise.tex')
        solution_tex_file = os.path.join(task_dir, 'solution.tex')
        annotation_tex_file = os.path.abspath(sheetinfo['ini_name'] + '_' + key + '.tex')
        
        if not os.path.isfile(task_tex_file):
            logger.debug('%s: File not found: %.s', key, task_tex_file)
            logger.error('Skipping nonexistent task: %s.', task_name)
            continue
        if not os.path.isfile(solution_tex_file):
            logger.debug('%s: File not found: %s.', key, solution_tex_file)
            logger.warning('The task %s does not have a solution.', task_name)
            solution_tex_file = None
        if not os.path.isfile(annotation_tex_file):
            logger.debug('%s: File not found: %s.', key, annotation_tex_file)
            logger.debug('%s: No annotation is attached to task %s.', key, task_name)
            annotation_tex_file = None
            
        if len(task_info) >= 3: 
            task_title = task_info[2]
        else:
            task_title = ''
        if len(task_info) >= 4: 
            task_points = task_info[3]
            if task_type == 'inclass':
                logger.warning('%s: Points given for "inclass" task %s will be ignored.', key, task_name)
        else:
            task_points = ''
        if len(task_info) > 4: 
            logger.warning('%s: Extra arguments will be ignored.', key)
        # TODO key exercise no longer needed
        # solution key only relvant if value is none or not 
        task_info_dict = {'type': task_type, 
                              'title': task_title,
                              'root_dir':task_dir,
                              'exercise':task_tex_file,
                              'solution':solution_tex_file,
                              'annotation': annotation_tex_file,
                              'points': task_points}
        task_list.append(task_info_dict)
    return task_list


def print_sheetinfo(sheetinfo, task_list):
    print('\n')
    print('lecture:\t\t' + sheetinfo.get('lecture', 'name of lecture'))
    print('lecturer:\t\t' + sheetinfo.get('lecturer', 'name of lecturer'))
    print('releasedate:\t\t' + sheetinfo.get('releasedate', 'released today'))
    print('deadline:\t\t' + sheetinfo.get('deadline', 'today'))
    print('sheetno:\t\t' + sheetinfo.get('sheetno', '0'))
    print('sheetname:\t\t' + sheetinfo.get('sheetname',  'exercise'))
    print('disclaimer:\t\t' + sheetinfo.get('disclaimer', 'empty_disclaimer'))
    print('compilename:\t\t' + sheetinfo['compilename'])
    print('resource:\t\t' + sheetinfo['path_to_pool'])
    print('tasks:\t\t')
    for task_info in task_list:
        print('\t\t\t' + task_info['type'] + ' : ' + task_info['title'])
    print('\n')

class ExerciseSheet:
    def __init__(self, sheetinfo,
                 task_list):
        self.sheetinfo = sheetinfo
        self.task_list = task_list
        
    def fill_latex_task_macro(self, task_info):
        if task_info['type'] == 'homework':
            return tex_utils.tex_command('inputHomework', [task_info['root_dir'], task_info['title'], task_info['points']])
        elif task_info['type'] == 'inclass':
            return tex_utils.tex_command('inputInclass', [task_info['root_dir'], task_info['title']])
        else:
            raise ValueError('Unsupported task type %s', task_info['type'])


    def fill_latex_solution_macro(self, task_info):
        if task_info['solution'] is not None:
            return tex_utils.tex_command('inputSolution', [task_info['root_dir']])
        return ''


    def fill_latex_annotation_macro(self, task_info): 
        if task_info['annotation'] is not None:
            return tex_utils.tex_command('inputAnnotation', [task_info['annotation']])
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

        task_list_tex = ''
        for task_info in self.task_list:
            task_list_tex += self.fill_latex_task_macro(task_info)+'\n'
            if render_solution: 
                task_list_tex += self.fill_latex_solution_macro(task_info)+'\n'
            if render_annotations: 
                task_list_tex += self.fill_latex_annotation_macro(task_info)+'\n'
                
        class_options_list = []
        # TODO english class options
        if render_solution: 
            class_options_list.append('Loesungen')
        if render_annotations: 
            class_options_list.append('Punkte')
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
                                                        inputlist=task_list_tex)
    
        # remove old files from build folder
        old_files = os.listdir(self.sheetinfo['build_folder'])
        for item in old_files:
            if item.startswith(self.compilename + '.'):
                os.remove(os.path.join(self.sheetinfo['build_folder'], item))
    
        # write to new file
        with open(os.path.join(self.sheetinfo['build_folder'], self.compilename + '.tex'), 'w') as fh:
            fh.write(output_from_rendered_template)
            
    def clear_dir(self):
        old_files = os.listdir(self.sheetinfo['build_folder'])
        for item in old_files:
            if not item.endswith('.pdf'):
                os.remove(os.path.join(self.sheetinfo['build_folder'], item))


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
    
    logger.debug('parsing args')
    parser = argparse.ArgumentParser(description='Create exercise sheet.')
    parser.add_argument('sheetinfo', type=str,
                        help='py file containing sheet information')
    parser.add_argument('-t', '--build-task', action='store_true')
    parser.add_argument('-s', '--build-solution', action='store_true')
    parser.add_argument('-a', '--build-annotation', action='store_true')
    parser.add_argument('-c', '--clean-after-build', action='store_true',
                        help='removes files created during building LaTex. Only pdf files remain.')
    args = parser.parse_args()
    if not args.build_task and not args.build_solution and not args.build_annotation: 
        args.build_task = True
    
    try: 
        sheetinfo, tasks = load_sheet_data(args)
        task_list = make_task_list(sheetinfo, tasks)
        print_sheetinfo(sheetinfo, task_list)
        
        os_utils.make_directories_if_nonexistent(sheetinfo['build_folder'])
         
        sheet = ExerciseSheet(sheetinfo, task_list)
        
        if args.build_task: 
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
            
        if args.clean_after_build:
            sheet.clear_dir()
            
        logger.info('Creation of %s successfull', sheetinfo['compilename'])
    except Exception as ex:
        logger.critical('', exc_info=ex)
        sys.exit(1)