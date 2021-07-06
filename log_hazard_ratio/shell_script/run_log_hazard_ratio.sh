#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        for ALGORITHM in "elastic_net" "light_gbm"
        do
            rm out/log_hazard_ratio/$MAIN_CATEGORY/$CATEGORY/$ALGORITHM.out
            sbatch -J log_hazard_ratio/$MAIN_CATEGORY/$CATEGORY/$ALGORITHM -o out/log_hazard_ratio/$MAIN_CATEGORY/$CATEGORY/$ALGORITHM.out log_hazard_ratio/shell_script/unit_log_hazard_ratio.sh -mc $MAIN_CATEGORY -c $CATEGORY -sa $ALGORITHM
        done
    done
done