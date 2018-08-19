import os
import time
import logging as log
from os import path
from multiprocessing import Process


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
        self.target_dir = target_dir

        self.runtime = 60
        self.interval_in_secs = 5
        self.recursive = recursive
        self.parallel_action = parallel_action
        self.once_action = once_action
        self.foreach_action = foreach_action
        # non parameter attributes
        self.file_register = dict()
        self.child_process: Process = None

    def __add_file__(self, modified_file, changed_files):
        self.file_register[modified_file] = path.getmtime(modified_file)
        changed_files.append(modified_file)

    def __is_changed_file__(self, check_file):
        return path.isfile(check_file) and not path.getmtime(check_file) == self.file_register.get(check_file)

    def __wait_and_reduce__(self):
        time.sleep(self.interval_in_secs)
        self.runtime -= self.interval_in_secs

    def __read_dir__(self, dir_path):
        file_list = list()
        if path.isdir(dir_path):
            for it in os.listdir(dir_path):
                r_path = path.join(dir_path, it)
                if path.isfile(r_path):
                    file_list.append(r_path)
                elif path.isdir(r_path) and self.recursive:
                    file_list += self.__read_dir__(r_path)
        return file_list

    def __do_once__(self):
        self.once_action()
        log.info("Executed '{}'".format(self.once_action.__name__))

    def __do_in_parallel__(self):
        if self.child_process is not None and self.child_process.is_alive():
            self.child_process.terminate()
        self.child_process = Process(target=self.parallel_action)
        self.child_process.start()
        log.info("Executed '{}'".format(self.parallel_action.__name__))

    def __do_foreach_action__(self, changed_files):
        for file in changed_files:
            self.foreach_action(file)
            log.info("Executed '{}'".format(self.foreach_action.__name__))

    def change_interval(self, interval_in_secs):
        """Change the interval when the observer should check for changes (Default 5 seconds)"""
        self.interval_in_secs = interval_in_secs

    def change_runtime(self, runtime_in_secs):
        """Change how long the observer should run (Default 60 seconds)"""
        self.runtime = runtime_in_secs

    def run(self):
        """Starts the file observation"""
        while self.runtime > 0:
            self.__wait_and_reduce__()
            changed_files = list()
            for item in self.__read_dir__(self.target_dir):
                if self.__is_changed_file__(item) and item not in __file__:
                    self.__add_file__(item, changed_files)
            log.info("Changed files: {}".format(str(changed_files)))

            if len(changed_files) > 0 and self.once_action is not None:
                # For one action
                self.__do_once__()
            elif len(changed_files) > 0 and self.parallel_action is not None:
                # For parallel actions
                self.__do_in_parallel__()
            elif len(changed_files) > 0 and self.foreach_action is not None:
                # For multiple actions on file change
                self.__do_foreach_action__(changed_files)
            else:
                log.info("Nothing happened.")
        log.info("Observation ends")
