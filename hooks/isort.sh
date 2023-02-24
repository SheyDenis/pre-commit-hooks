#!/bin/bash

source "$(dirname ${0})/utils.sh"

function usage() {
    usage_str="
        Usage ./$(basename ${0}) [--settings-file <file>] files...
"
    echo ${usage_str} 1>&2
}

SETTINGS_FILE="$(dirname ${0})../configs/isort.cfg"
options=$(getopt --longoptions 'settings-file:' -o '' -- "${@}")
if [[ ${?} -ne 0 ]]; then
    usage
    exit 1
fi

eval set -- "$options"
while true; do
    case "${1}" in
    --settings-file)
        shift
        SETTINGS_FILE=${1}
        ;;
    --)
        echo '--'
        shift
        break
        ;;
    esac
    shift
done

rc=0
for staged_file in ${@}; do
    isort --quiet --check-only "${staged_file}" --settings-file "${SETTINGS_FILE}" 2>&1

    if [[ ${?} -ne 0 ]]; then
        rc=1
        echo_error "File failed isort check [${staged_file}]."
    fi
done

exit ${rc}
