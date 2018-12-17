## Usage

    zipindex [--index INDEX] (create|find|archives|files|purge)

The following commands assume:

    export ZIPINDEX=myindex.idx

Create an archive:

    zipindex create /path/to/zip/files

Search an index:

    zipindex find 'some*pattern'

List archives contained in an index:

    zipindex archives

List files contained in an index

    zipindex files

Purge archives from an index:

    zipindex purge --archives 'pattern*.zip'

Purge files from an index:

    zipindex purge --files 'some*pattern'
