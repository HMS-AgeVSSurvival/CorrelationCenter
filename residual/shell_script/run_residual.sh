#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    [ ! -e out/residual/$MAIN_CATEGORY.out ] || rm out/residual/$MAIN_CATEGORY.out
    sbatch -J residual/$MAIN_CATEGORY -o out/residual/$MAIN_CATEGORY.out residual/shell_script/unit_residual.sh -mc $MAIN_CATEGORY
done