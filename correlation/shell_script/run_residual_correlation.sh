#!/bin/bash

[ -d data/correlation/residual ] || mkdir -p data/correlation/residual

TARGETS=("age" "all" "cvd" "cancer")
TARGETS_INDEXES=(0 1 2 3)

for IDX_TARGET_IDX in ${TARGETS_INDEXES[@]}
do
    number_indexes=$(( ${#TARGETS_INDEXES[@]} - IDX_TARGET_IDX ))
    for IDX_TARGET_COLUMN in ${TARGETS_INDEXES[@]:IDX_TARGET_IDX:number_indexes}
    do
        echo -n > out/residual_correlation/${TARGETS[IDX_TARGET_IDX]}_${TARGETS[IDX_TARGET_COLUMN]}.out
        [ ! -e error/residual_correlation/${TARGETS[IDX_TARGET_IDX]}_${TARGETS[IDX_TARGET_COLUMN]}.out ] || rm error/residual_correlation/${TARGETS[IDX_TARGET_IDX]}_${TARGETS[IDX_TARGET_COLUMN]}.out

        sbatch -J residual_correlation/${TARGETS[IDX_TARGET_IDX]}_${TARGETS[IDX_TARGET_COLUMN]} -o out/residual_correlation/${TARGETS[IDX_TARGET_IDX]}_${TARGETS[IDX_TARGET_COLUMN]}.out -e error/residual_correlation/${TARGETS[IDX_TARGET_IDX]}_${TARGETS[IDX_TARGET_COLUMN]}.out correlation/shell_script/unit_residual_correlation.sh -ti ${TARGETS[IDX_TARGET_IDX]} -tc ${TARGETS[IDX_TARGET_COLUMN]}
    done
done