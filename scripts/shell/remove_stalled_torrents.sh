#!/bin/bash

echo "Running script to remove stalled torrents."

CMD="uv run scripts/remove_stalled_torrents.py"

echo "Running command: $CMD"
eval "$CMD"

if [[ $? -eq 0 ]]; then
    echo "Finished removing stalled torrents."
else
    echo "Failed to remove stalled torrents."
    exit 1
fi
