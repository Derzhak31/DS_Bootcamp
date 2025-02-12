#!/bin/bash

FILE=../ex03/hh_positions.csv

header=$(head -n 1 "$FILE")

tail -n +2 "$FILE" | while read -r line; do
    data=$(echo "$line" | awk -F ',' '{print $2}' | cut -d'T' -f1 | tr -d '"')
    out="${data}.csv"
    if [ ! -f "$out" ]; then
    echo "$header" > "$out"
    fi
    echo "$line" >> "$out"
done