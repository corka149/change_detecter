import logging as log
from multiprocessing import Process
from change_detector.file_syncer import RsFileSyncer


class FileObserver:
    """ The FileObserver detect changes based on the modified time of a file
    and performs a given action. Example usage:

    if __name__ == '__main__':
        log.basicConfig(level=log.INFO)\n
        one_day = 24 * 60 * 60\n
        observer = FileObserver(".")\n
        observer.change_runtime(one_day)\n
        observer.run()\n
    """

    def __init__(self, target_dir, recursive=False, parallel_action=None, once_action=None, foreach_action=None):
        """Creates an file observer.

        :param target_dir: Defines the observed folder
        :param recursive: Should the folder be observed recursively
        :param parallel_action: Run in a different process
        :param once_action: Once performed (e.g.: 'lambda: print("Files were changed")')
        :param foreach_action: Performed for each changed item (e.g.: 'lambda it: print(it)')
        """
        self.__target_dir__ = target_dir

        self.__runtime__ = 60
        self.__interval_in_secs__ = 5
        self.__recursive__ = recursive
        self.__parallel_action__ = parallel_action
        self.__once_action__ = once_action
        self.__foreach_action__ = foreach_action
        # non parameter attributes
        self.__file_register__ = dict()
        self.__child_process__: Process = None
        self.__file_syncer__: RsFileSyncer = None

    def __read_dir__(self):
        if self.__file_syncer__ is None:
            self.__file_syncer__ = RsFileSyncer(self.__interval_in_secs__, self.__target_dir__, self.__recursive__)
        file_list = self.__file_syncer__.emit_changed_files()
        self.__runtime__ -= self.__interval_in_secs__
        return file_list

    def __do_once__(self):
        self.__once_action__()
        log.info("Executed '{}'".format(self.__once_action__.__name__))

    def __do_in_parallel__(self):
        if self.__child_process__ is not None and self.__child_process__.is_alive():
            self.__child_process__.terminate()
        self.__child_process__ = Process(target=self.__parallel_action__)
        self.__child_process__.start()
        log.info("Executed '{}'".format(self.__parallel_action__.__name__))

    def __do_foreach_action__(self, changed_files):
        for file in changed_files:
            self.__foreach_action__(file)
            log.info("Executed '{}'".format(self.__foreach_action__.__name__))

    def change_interval(self, interval_in_secs):
        """Change the interval when the observer should check for changes (Default 5 seconds)"""
        self.__file_syncer__ = None
        self.__interval_in_secs__ = interval_in_secs

    def change_runtime(self, runtime_in_secs):
        """Change how long the observer should run (Default 60 seconds)"""
        self.__file_syncer__ = None
        self.__runtime__ = runtime_in_secs

    def run(self):
        """Starts the file observation"""
        while self.__runtime__ > 0:
            changed_files = self.__read_dir__()
            log.info("Changed files: {}".format(str(changed_files)))

            if changed_files is not None and len(changed_files) > 0 and self.__once_action__ is not None:
                # For one action
                self.__do_once__()
            elif changed_files is not None and len(changed_files) > 0 and self.__parallel_action__ is not None:
                # For parallel actions
                self.__do_in_parallel__()
            elif changed_files is not None and len(changed_files) > 0 and self.__foreach_action__ is not None:
                # For multiple actions on file change
                self.__do_foreach_action__(changed_files)
            else:
                log.info("Nothing happened.")
        log.info("Observation ends")
