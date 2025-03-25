#!/bin/bash

directory="./data/online"
# Check if the directory exists
if [[ ! -d "$directory" ]]; then
  echo "Error: Directory '$directory' not found."
  exit 1
fi

for file in "$directory"/*; do
  if [[ -f "$file" ]]; then
    echo "Processing file: $file"
    filename=$(basename "$file" .xz)
    output_files="./decompressed/$filename"
    xz -dkc "$file" > "$output_files"
    if [[ $? -eq 0 ]]; then
      echo "Decompressed: $file to $output_file"
    else
      echo "Error decompressing: $file"
    fi

  fi
done

echo "Finished processing all files."

exit 0
