#!/bin/bash

source "$(dirname ${0})/utils.sh"

rc=0
for staged_file in ${@}; do
    mypy --follow-imports=silent --ignore-missing-imports "${staged_file}" &>/dev/null

    if [[ ${?} -ne 0 ]]; then
        rc=1
        echo_error "File failed mypy check [${staged_file}]."
    fi
done

exit ${rc}
