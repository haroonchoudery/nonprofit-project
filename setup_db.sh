#!/bin/sh
# This script will create the database on the localhost and populate it.

mysql -u root < src/db/setup_db.sql
python src/db/populatedb.py
