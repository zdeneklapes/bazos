#!/bin/bash

python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install $(pip3 list --outdated | awk '{print $1}'|tail -n 7) --upgrade
PYTHONPATH=$PWD python3 bazos/__init__.py \
    --items-path $PWD/examples-data/ \
    --credentials-path $PWD/tokens/ \
    --verbose=1 \
    --remote=0 \
    --create-all=1 \
    --delete-all=1 \
    --country cz sk \
    --mode=fast
