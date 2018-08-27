
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use crc::crc32;
use std;
use std::collections::HashMap;

const HAS_CHANGED: bool = true;

/// Checks if the checksum of a file is the same
pub fn has_file_changed(file_path: &Path, crc32_ieee_checksum: &u32) -> (bool, u32) {
    match read_file(file_path) {
        Ok(bytes) => {
                let calc_checksum = calculate_crc32(&bytes);
                (calc_checksum != *crc32_ieee_checksum, calc_checksum)
            },
        Err(e) => {
            eprintln!("Error while checking file {:?}", e);
            (HAS_CHANGED, 0)
        }
    }
}

/// Checks if a list of files is unchanged
pub fn have_files_changed<'a>(files_and_checksums: &mut HashMap<&'a Path, u32>) -> Vec<(&'a Path, u32)> {
    let mut changed_files: Vec<(&Path, u32)> = Vec::new();
    for (file_path, crc32_ieee_checksum) in files_and_checksums.iter() {
        let (changed, checksum) = has_file_changed(file_path, crc32_ieee_checksum);
        if changed {
            changed_files.push((file_path, checksum));
        }
    }
    changed_files
}

/// Helper function for reading the whole file content
fn read_file(path: &Path) -> Result<Vec<u8>, std::io::Error> {
    let mut byte_buffer: Vec<u8> = Vec::new();
    match File::open(path) {
        Ok(mut file) => {
            let read_result = file.read_to_end(&mut byte_buffer);
            match read_result {
                Ok(_) => Ok(byte_buffer),
                Err(e) => Err(e),
            }
        },
        Err(e) => Err(e)
    }
}

/// Calculates checksum
fn calculate_crc32(byte_buffer: &[u8]) -> u32 {
    crc32::checksum_ieee(byte_buffer)
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_calculateok() {
        let byte_buffer = b"123456789";
        let sum = calculate_crc32(byte_buffer);
        assert_eq!(sum, 0xcbf43926);
    }

    #[test]
    fn test_read_file() {
        let path = Path::new("./test.d/3/web.log");
        let result = read_file(path);
        assert!(result.is_ok());
        assert_eq!(108, result.unwrap().pop().unwrap());
    }

    #[test]
    fn test_has_file_changed_true() {
        let path = Path::new("./test.d/3/web_true.log");
        let false_checksum: u32 = 1;
        let (changed, checksum) = has_file_changed(path, &false_checksum);
        assert!(changed);
        assert_eq!(2342642008, checksum);
    }

    #[test]
    fn test_has_file_changed_false() {
        let path = Path::new("./test.d/3/web_false.log");
        let false_checksum: u32 = 1249955312;
        let (changed, checksum) = has_file_changed(path, &false_checksum);
        assert_eq!(1249955312, checksum);
        assert!(!changed);
    }
}