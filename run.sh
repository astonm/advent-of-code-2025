#!/bin/bash
DAY="$1"
PART="$2"
INPUT=${3:-input}
CODE=${4:-code}
OTHER=${@:5}
export PYTHONPATH="."
uv run python "$DAY/$CODE.py" "$PART" "$DAY/$INPUT.txt" $OTHER
