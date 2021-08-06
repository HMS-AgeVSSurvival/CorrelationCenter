#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    echo -n > out/residual/$MAIN_CATEGORY.out
    sbatch -J residual/$MAIN_CATEGORY -o out/residual/$MAIN_CATEGORY.out residual/shell_script/unit_residual.sh -mc $MAIN_CATEGORY
done