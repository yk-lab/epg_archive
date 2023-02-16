#!/usr/bin/env bash

echo "STANDBY: ${STANDBY}"
if [ -z "${STANDBY}" ]; then
    echo "dockerize"
    dockerize -timeout 60s -wait ${STANDBY}
fi
