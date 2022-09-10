#!/bin/bash

cmd=$1

usage() {
    echo "feast_helper.sh <command>"
    echo "Available commands:"
    echo " apply                run feast apply"
    echo " materialize          materialize offline to online"
}

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    usage
    exit 1
fi

apply() {
    cd feature_repo
    feast apply
}

materialize() {
    cd feature_repo
    feast materialize-incremental $(date +%Y-%m-%d)
}

shift

case $cmd in
apply)
    apply "$@"
    ;;
materialize)
    materialize "$@"
    ;;
*)
    echo -n "Unknown command: $cmd"
    usage
    exit 1
    ;;
esac
