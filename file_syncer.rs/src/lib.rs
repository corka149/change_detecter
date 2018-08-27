#![feature(specialization)]

#[macro_use]
extern crate pyo3;
extern crate crc;

mod directory_watcher;
mod error;

use pyo3::prelude::*;
use directory_watcher::DirectoryWatcher;

#[pyclass]
struct PyDirectoryWatcher {
    directory_watcher: DirectoryWatcher
}

#[pymethods]
impl PyDirectoryWatcher {

    #[new]
    fn __new__(obj: &PyRawObject, secs_interval: u64, path: &str, recurisve: bool) -> PyResult<()> {
        match DirectoryWatcher::new(secs_interval, path, recurisve) {
            Ok(directory_watcher) => obj.init(|_| PyDirectoryWatcher{ directory_watcher }),
            Err(e) => panic!("{:?}", e)
        }
    }

    fn emit_changed_files(&mut self) -> PyResult<Vec<String>> {
        match self.directory_watcher.emitted_changed_files() {
            Ok(result) => Ok(result),
            Err(e) => panic!("{:?}", e)
        }
    }

}


#[pymodinit]
fn file_syncer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyDirectoryWatcher>()?;
    Ok(())
}
