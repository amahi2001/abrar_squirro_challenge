#!/bin/bash

# Check if a directory is provided as an argument
if [ "$#" -eq 1 ]; then
  directory=$1
else
  # If not, use the current directory
  directory="."
fi

# List the contents of the directory
echo "Listing contents of: $directory"
ls -l $directory