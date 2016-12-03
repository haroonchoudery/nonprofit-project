#!/bin/sh

mysql -u root < src/db/setup_db.sql
python src/db/populatedb.py
