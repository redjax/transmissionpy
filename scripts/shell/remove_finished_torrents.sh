#!/bin/bash

echo "Running script to remove finished torrents."

CMD="uv run scripts/remove_finished_torrents.py"

echo "Running command: $CMD"
eval "$CMD"

if [[ $? -eq 0 ]]; then
    echo "Finished removing finished torrents."
else
    echo "Failed to remove finished torrents."
    exit 1
fi
