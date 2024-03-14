#!/bin/sh

cleanup() {
    docker compose -f compose.ci.yaml down 1> /dev/null
    exit 1
}

trap cleanup SIGINT EXIT SIGKILL

docker compose -f compose.ci.yaml up --abort-on-container-exit && docker compose -f compose.ci.yaml down