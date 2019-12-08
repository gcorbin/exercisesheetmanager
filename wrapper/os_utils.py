import os
import logging

class ChangedDirectory:

    def __init__(self, path):
        self._path = path
        self._cwd = None

    def __enter__(self):
        self._cwd = os.getcwd()
        newdir = os.path.join(self._cwd, self._path)
        logger.debug('Entering working directory %s', newdir)
        os.chdir(self._path)
        return newdir

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug('Changing working directory back to %s', self._cwd)
        os.chdir(self._cwd)
        return False
