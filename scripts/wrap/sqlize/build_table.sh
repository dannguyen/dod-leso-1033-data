# #!/bin/sh

# DEPRECATED

# # Example
# # scripts/wrap/sqlize/load_table.sh /tmp/mydb/foo.sqlite data/compiled/state-agencies.csv

# DB_PATH=$1
# SRC_PATH=$2
# TABLE_NAME=$3
# SCHEMA_PATH=$4

# echo "database path: ${DB_PATH}"
# echo "source data: ${SRC_PATH}"
# echo "dest table: ${TABLE_NAME}"
# mkdir -p $(dirname $DB_PATH)




# sqlite3 ${DB_PATH} <<SQL_HERE
# .bail on
# .mode csv
# .import ${SRC_PATH} ${TABLE_NAME}
# .mode column
# SELECT 'table "${TABLE_NAME}" has ' || COUNT(1) || ' rows, imported from: ${SRC_PATH}'
# FROM ${TABLE_NAME};
# SQL_HERE


