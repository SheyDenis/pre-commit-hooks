#!/bin/bash

source "$(dirname ${0})/utils.sh"

function usage() {
    usage_str="
        Usage ./$(basename ${0}) [--rcfile <file>] [--fail-under <int>] files...
"
    echo ${usage_str} 1>&2
}

RCFILE="$(dirname ${0})/../configs/pylintrc"
FAIL_UNDER=10

options=$(getopt --longoptions 'rcfile:,fail-under:' -o '' -- "${@}")
if [[ ${?} -ne 0 ]]; then
    usage
    exit 1
fi

eval set -- "$options"
while true; do
    case "${1}" in
    --rcfile)
        shift
        RCFILE=${1}
        ;;
    --fail-under)
        shift
        FAIL_UNDER=${1}
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
    pylint "${staged_file}" --rcfile "${RCFILE}" --fail-under ${FAIL_UNDER}

    if [[ ${?} -ne 0 ]]; then
        rc=1
        echo_error "File failed pylint check [${staged_file}]."
    fi
done

exit ${rc}
