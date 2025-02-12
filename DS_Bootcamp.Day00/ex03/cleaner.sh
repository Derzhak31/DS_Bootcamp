#!/bin/bash

FILE="../ex02/hh_sorted.csv"

(head -n 1 "$FILE" && tail +2 "$FILE" | awk -F ',' 'BEGIN{OFS=","}{
    if ($3 ~ /[Jj]unior/) { level = "Junior" }
    if ($3 ~ /[Mm]iddle/) { level = (level ? level "/Middle" : "Middle") }
    if ($3 ~ /[Ss]enior/) { level = (level ? level "/Senior" : "Senior") }
    if (!level) { level = "-" }
    $3 = level;
    print $0;
    level = ""
}') > hh_positions.csv