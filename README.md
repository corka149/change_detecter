# Change detector

## Example
```python
import logging as log
import shutil
from change_detector.core import FileObserver
from subprocess import call, Popen


java_process = None


def build_and_run():
    global java_process
    if java_process is not None:
        java_process.kill()
    call([shutil.which("mvn"), "clean", "package", "-Dmaven.test.skip=true"])
    java_process = Popen([shutil.which("java"), "-jar", "target\\gs-rest-service-0.1.0.jar"])


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    one_day = 24 * 60 * 60
    fo = FileObserver("src", recursive=True, once_action=build_and_run)
    fo.change_runtime(one_day)
    fo.run()

```