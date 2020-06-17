# documentation for cleaning up agency names


Order of operations:

```sh
$ make compile 
$ make sqlize_compile
$ printf ".mode csv\nSELECT * FROM agency_files_summary;" | sqlite3 data/wrapped/db.sqlite > data/wrapped/summaries/agency-files.csv

cat data/compiled/state-agencies/ALL.csv | xsv search '\bLEA\b' --select org_station_name
