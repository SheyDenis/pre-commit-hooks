#!/bin/bash

source "$(dirname ${0})/utils.sh"

DEV_MARKER_REGEX='([^\s]+ DEV MARKER.*$)'

rc=0
for staged_file in ${@}; do
    echo_debug "Handling file [${staged_file}]"
    marker_lines=$(git diff --cached "${staged_file}" | grep -E "${DEV_MARKER_REGEX}" | sed "s/$/\\n/")
    if [[ ${?} == 0 ]]; then
        rc=1
        OLDIFS="${IFS}"
        IFS=$'\n'
        for l in ${marker_lines}; do
            echo_error "Found dev-marker line [${l}] in file [${staged_file}]" # TODO - Add line number to output
        done
        IFS="${OLDIFS}"
    fi

done

echo_info "rc [${rc}]"
exit ${rc}
