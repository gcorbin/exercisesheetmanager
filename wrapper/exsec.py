#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 09:10:53 2020

@author: Armin Corbin
"""

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import *
from whoosh import highlight

import argparse
import os
import re
import sys

import textwrap

import datetime
from dateutil.parser import parse as parse_date

import logging
from defaultlogger import set_default_logging_behavior
logger = logging.getLogger('ExerciseSheetManager.exsec')


class EscapeSeqFormatter(highlight.Formatter):
    """ highlights with unicode escape sequence (bold)
    """

    def format_token(self, text, token, replace=False):
        # Use the get_text function to get the text corresponding to the
        # token
        tokentext = highlight.get_text(text, token, replace)

        # Return the text as you want it to appear in the highlighted
        # string
        return "\x1b[1;4m%s\x1b[22;24m" % tokentext
        

def hf(res, field):
    """
    returns the contnet of a filed where the matching part is highlighted
    :param res: whoosh hit object
    :param field: field name
    """
    return res.highlights(field, minscore=0)


def parseTaskFile(task_file):
    logger.debug('parsing task file ' + task_file)
    
    metaKey = ['author', 'date', 'language', 'keywords']
    
    metaDataRe = re.compile('^\s*%\s*@(' + '|'.join(metaKey) + '):\s*(.*)')
    
    metaData = dict.fromkeys(metaKey, '')
    
    texcode = []
    
    with open(task_file, 'r') as f:
        for line in f:
            m = metaDataRe.match(line)
            if m:
                metaData[m.group(1)] = m.group(2)
            else:
                texcode.append(line)
    
    return metaData, '\n'.join(texcode)                


def updateIndex(ix, pool_path):
    """
    parses the files in the pool and adds the entries to the whoosh index 
    :param ix: whoosh index object
    :param pool_path: path to the pool
    """
    
    logger.debug('updating search index')
    writer = ix.writer()
    
    exercise_list = [f.name for f in os.scandir(pool_path) if f.is_dir()]
    for ex in exercise_list:
        if ex == '.search_index':
            continue
        task_file = os.path.abspath(os.path.join(pool_path, ex, 'task.tex'))
        if os.path.isfile(task_file):
            logger.info('parsing ' + task_file)
            metaData, task_texcode = parseTaskFile(task_file)
        else:
            logger.warning(ex + ' does not include a task.tex file. skipping entry')
            continue
        
        solution_file = os.path.abspath(os.path.join(pool_path, ex, 'solution.tex'))
        if os.path.isfile(solution_file):
            with open(solution_file, 'r') as f:
                solution_texcode = f.read()
        else:
            logger.warning(ex + ' does not include a solution.tex file')
            solution_texcode = ''
            
        if metaData['date'] == '':
            lastupdate = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
        else:
            lastupdate = parse_date(metaData['date'])

        writer.add_document(
            folder_name=ex,
            task=task_texcode,
            solution=solution_texcode,
            language=metaData['language'],
            maintainer=metaData['author'],
            lastupdate=lastupdate,
            keywords=re.sub(r',\s+', ',', metaData['keywords'])
        )

    writer.commit()


if __name__ == '__main__':
    
    set_default_logging_behavior(logfile='exsec')
    
    # parse input arguments ---------------------------------------------------
    parser = argparse.ArgumentParser(description='advanced search an exercise pool')
    parser.add_argument('-p', '--path-to-pool', action="store", help='path to pool')
    parser.add_argument('-u', '--update', action="store_true", help='update the index')
    parser.add_argument('-n', action="store", help='maximal number of printed results (default=10)', default=10)
    parser.add_argument('-q', action="store", help='query in fields: "name","description","language","keywords","format". \
                        Query syntax: https://whoosh.readthedocs.io/en/latest/querylang.html \ ')
    
    args = parser.parse_args()
    
    # define index schema ------------------------------------------------------
    schema = Schema(folder_name=NGRAM(stored=True, minsize=2, maxsize=10),
                    task=TEXT(stored=True),
                    solution=TEXT(stored=True),
                    language=TEXT(stored=True),
                    maintainer=TEXT(stored=True),
                    lastupdate=DATETIME(stored=True),
                    keywords=KEYWORD(stored=True, lowercase=True, scorable=True, commas=True)
                    )
    
    # create or open existing index
    
    if not os.path.exists(args.path_to_pool):
        logger.fatal('pool ' + args.path_to_pool + ' does not exist.')
        sys.exit(1)
    
    index_dir = os.path.join(args.path_to_pool, '.search_index')
    
    if args.update:
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)

        ix = create_in(index_dir, schema)
        updateIndex(ix, args.path_to_pool)
    else:
        if not os.path.exists(index_dir):
            logger.fatal('%s does not exist. create is with -u option', index_dir)
            sys.exit(1)
        ix = open_dir(index_dir)
        
    # perform search ---------------------------------------------------------
    if args.q:
    
        with ix.searcher() as searcher:
                    
            parser = MultifieldParser(["folder_name", "task", "solution", "language", "keywords"], ix.schema)
        
            parser.add_plugin(FuzzyTermPlugin())
            
            myquery = parser.parse(args.q)
            
            results = searcher.search(myquery, limit=int(args.n))
            
            results.formatter = EscapeSeqFormatter()
            
            # first run to extract context from tex files
            results.fragmenter = highlight.ContextFragmenter(maxchars=50, surround=20)
            task_hl = []
            solution_hl = []
            
            wrapper = textwrap.TextWrapper(initial_indent='\t', subsequent_indent='\t')
            
            for i, res in enumerate(results, start=1):
                task_hl.append(wrapper.fill(hf(res, "task")))
                solution_hl.append(wrapper.fill(hf(res, "solution")))

            results.fragmenter = highlight.WholeFragmenter(charlimit=300)
                     
            print('-'*60)
            print('found \x1b[37;1m%u\x1b[37;0m matching entries for query:\x1b[92;2m %s\x1b[0m\n' % (len(results), args.q))
            for i, res in enumerate(results, start=1):
                datestr = ''
                if res["lastupdate"] is not None:
                    datestr = res["lastupdate"].strftime("%Y-%m-%d")
                
                print('\x1b[37;1m(%2u) \x1b[91;22m%s \x1b[0m%s:' % (i, hf(res, "folder_name"), hf(res, "maintainer")))
                print('\t\x1b[36m%s\x1b[33m %s\x1b[0m' % (hf(res, "language"), datestr))
                
                if task_hl[i-1] != '':
                    print('\x1b[94m%s \x1b[33;2m' % (task_hl[i-1]))
                    
                if solution_hl[i-1] != '':
                    print('\x1b[93m%s \x1b[33;2m' % (solution_hl[i-1]))
                print('\t\x1b[37;22m%s ' % ('   '.join(hf(res, "keywords").split(','))))
                print('\x1b[0m')
