#!/bin/bash

MAIN_CATEGORIES=("examination" "laboratory" "questionnaire")

for MAIN_CATEGORY in ${MAIN_CATEGORIES[@]}
do
    echo -n > out/feature_importances_correlation/$MAIN_CATEGORY.out
    [ ! -e error/feature_importances_correlation/$MAIN_CATEGORY ] || rm error/feature_importances_correlation/$MAIN_CATEGORY.out

    sbatch -J feature_importances_correlation/$CATEGORY -o out/feature_importances_correlation/$CATEGORY.out -e error/feature_importances_correlation/$CATEGORY.out correlation/shell_script/unit_feature_importances_correlation.sh -mc $MAIN_CATEGORY
done