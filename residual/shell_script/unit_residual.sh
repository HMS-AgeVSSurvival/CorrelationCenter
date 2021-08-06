#!/bin/bash
#SBATCH --partition short
#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu 400M

unset MAIN_CATEGORY

module load gcc/6.2.0
module load python/3.7.4
source env_o2/bin/activate


while [[ $# -gt 0 ]]; do
    case $1 in
        -mc | --main_category)
            MAIN_CATEGORY=$2
            shift
            shift
            ;;
        -?*)
            printf "WARN: Unknown option (ignored): $1\n" >&2
            usage
            shift
            shift
            ;;
    esac
done


if [[ $MAIN_CATEGORY = "" ]]
then
    echo "Please precise the main category"
else
    for PATH_CATEGORY in ../TrainingCenter/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)
        
        residual -mc $MAIN_CATEGORY -c $CATEGORY
    done
fi 