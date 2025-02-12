#!/bin/bash

echo '"id","created_at","name","has_test","alternate_url"' > combined.csv
tail -q -n +2 $(ls *.csv | sort) >> combined.csv