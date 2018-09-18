cargo +nightly build --release
rm ../change_detector/file_syncer/file_syncer.pyd
cp ./target/release/file_syncer.dll ../change_detector/file_syncer/file_syncer.pyd