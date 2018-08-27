use std::error;
use std::fmt;

#[derive(Debug, Clone)]
pub struct PathError;

impl fmt::Display for PathError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "exptected path: No valid path to a directory found!"
        )
    }
}

impl error::Error for PathError {
    fn description(&self) -> &str {
        "exptected path: No valid path to a directory found!"
    }

    fn cause(&self) -> Option<&error::Error> {
        None
    }
}
