
from change_detector.file_syncer.file_syncer import PyDirectoryWatcher


class RsFileSyncer:

    def __init__(self, interval_secs, dir_path , recursive):
        self.py_dir_watch = PyDirectoryWatcher(interval_secs, dir_path, recursive)

    def emit_changed_files(self) -> list:
        return self.py_dir_watch.emit_changed_files()
