#!/bin/bash

source "$(dirname ${0})/utils.sh"

function usage() {
    usage_str="
        Usage ./$(basename ${0}) [--error-limit=int] files...
"
    echo ${usage_str} 1>&2
}

ERROR_LIMIT=0
options=$(getopt --longoptions 'error-limit:' -o '' -- "${@}")
if [[ ${?} -ne 0 ]]; then
    usage
    exit 1
fi

eval set -- "$options"
while true; do
    case "${1}" in
    --error-limit)
        shift
        ERROR_LIMIT=${1}
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
    echo_debug "Handling file [${staged_file}]"
    res=$(clang-format --style=file --dry-run -Werror --ferror-limit=0 "${staged_file}" 2>&1)

    if [[ ${?} -ne 0 ]]; then
        rc=1
        echo_error "File failed clang-format check [${staged_file}] [${res}]."
    fi
done

echo_info "rc [${rc}]"
exit ${rc}
