#!/bin/bash

IN="../ex03/hh_positions.csv"
OUT="hh_uniq_positions.csv"

echo "\"name\",\"count\"" > $OUT
echo "\"Junior\"","$(grep -c Junior $IN)" >> $OUT
echo "\"Middle\"","$(grep -c Middle $IN)" >> $OUT
echo "\"Senior\"","$(grep -c Senior $IN)" >> $OUT 