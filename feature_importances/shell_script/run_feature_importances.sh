#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        [ -d data/feature_importances/$MAIN_CATEGORY/ ] || mkdir -p data/feature_importances/$MAIN_CATEGORY/
        
        feature_importances -mc $MAIN_CATEGORY -c $CATEGORY
    done
done