  docker run -v `pwd`:/workspace --rm gsscogs/csvlint sh -c "for i in codelists/*.csv-metadata.json ; do csvlint -s \"\$i\" --no-verbose; done"
