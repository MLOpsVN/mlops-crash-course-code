#!/bin/bash#
cd feature_repo
feast materialize-incremental $(date +%Y-%m-%d)