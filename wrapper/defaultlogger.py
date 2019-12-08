import logging


def set_default_logging_behavior(logfile):
    logger = logging.getLogger('ExerciseSheetManager')

    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('{0}.log'.format(logfile), mode='w')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    detailed_format = logging.Formatter('%(asctime)s: %(levelname)s in %(name)s: %(message)s')
    fh.setFormatter(detailed_format)
    simple_format = logging.Formatter('%(levelname)s: %(message)s')
    ch.setFormatter(simple_format)

    logger.addHandler(fh)
    logger.addHandler(ch)