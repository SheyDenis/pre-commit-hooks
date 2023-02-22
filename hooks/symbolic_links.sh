#!/bin/bash

source "$(dirname ${0})/utils.sh"

echo "@: $@"
rc=0
for staged_file in ${@}; do
    echo_debug "Handling file [${staged_file}]"
    if [[ -L "${staged_file}" ]]; then
        rc=1
        echo_error "File [${staged_file}] is a symbolic link to [$(file ${staged_file} | grep -Eo 'symbolic link to .*' | sed 's/symbolic link to //')]"
    fi
done

echo_info "rc [${rc}]"
exit ${rc}
