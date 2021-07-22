#!/bin/bash

unset MEMORY
unset TIME


function usage()
{
    cat << HEREDOC

    Usage: $interactive_node [-m MEMORY] [-t TIME]

    optional arguments:
        -h, --help           show this help message and exit
        -m, --memory MEMORY  memory allocated in Gigabytes
        -t, --time TIME      time allocated in hours

HEREDOC
}


HELP_CALLED=false


while [[ $# -gt 0 ]]; do
    case $1 in
        -h | --help ) 
            usage >&2
            HELP_CALLED=true
            shift
            ;;
        -m | --memory)
            MEMORY=$2
            shift
            shift
            ;;
        -t | --time)
            TIME=$2
            shift
            shift
            ;;
        -?*)
            printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
            usage
            shift
            shift
            ;;
    esac
done


if [[ $MEMORY = "" ]]
then
    MEMORY=2
fi 

if [[ $TIME = "" ]]
then
    TIME=2
fi

srun --partition interactive --job-name "InteractiveJob" --cpus-per-task 1 --mem-per-cpu $MEMORY\G --time $TIME:00:00 --pty bash
module load gcc/6.2.0 python/3.7.4
source env_o2/bin/activate