#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mapproxy-seed -s ${SCRIPT_DIR}/../seed.yaml -f ${SCRIPT_DIR}/../mapproxy.yaml