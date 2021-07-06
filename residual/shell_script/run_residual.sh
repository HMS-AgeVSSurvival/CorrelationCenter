#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in ../TrainingCenter/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        rm out/residual/$MAIN_CATEGORY/$CATEGORY.out
        sbatch -J residual/$MAIN_CATEGORY/$CATEGORY -o out/residual/$MAIN_CATEGORY/$CATEGORY.out residual/shell_script/unit_residual.sh -mc $MAIN_CATEGORY -c $CATEGORY
    done
done