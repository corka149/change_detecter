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


/// Error, which occurs when an invalid mode was selected.
#[derive(Debug, Clone)]
pub struct UnknowMode<'a>{
    message: &'a str
}

impl<'a> fmt::Display for UnknowMode<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{}",
            self.message
        )
    }
}

impl<'a> error::Error for UnknowMode<'a> {
    fn description(&self) -> &str {
        self.message
    }

    fn cause(&self) -> Option<&error::Error> {
        None
    }
}
