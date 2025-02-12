#!/bin/bash

FILE="../ex01/hh.csv"

(head -n 1 "$FILE" && tail +2 "$FILE" | sort -t ',' -k2 -k1) > hh_sorted.csv
