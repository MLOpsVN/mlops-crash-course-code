#!/bin/bash

cmd=$1

usage() {
    echo "bentoml_helper.sh <command> [options]"
    echo "Available commands:"
    echo " serve          serve a bentoml service"
    echo "Available options:"
    echo " --port=x       bentoml service's port"
    echo " --reload       auto reload bentoml service"
}

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    usage
    exit 1
fi

serve() {
    cd src
    bentoml serve bentoml_service:svc "$@"
}

shift

case $cmd in
serve)
    serve "$@"
    ;;
*)
    echo -n "Unknown command: $cmd"
    usage
    exit 1
    ;;
esac
