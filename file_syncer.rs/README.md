# file_syncer

Future: Heart of the change_detector written in Rust. It should observer folders and emit changed files as list back to python. 

## Setup

On Windows: Rename 
1. Rename dll to pyd
2. Use with 'from file_syncer import PyDirectoryWatcher'

- Create object with: secs_interval: u64, path: String, recurisve: bool
- Watch for changed files via: emit_changed_files

## TODO

Parts that need to be impelmented
- -File register: Check which files avaible and determine if they are new or changed-
    - -Hash and store them-
    - -Check if file is open then do not register it-
- Python module-interface
    - -Implement event or hook point for python- 
    - Easy installation
- -Made time interval configurable-
- -Implement recursive file checking-
