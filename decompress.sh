#!/bin/bash

declare -a directories=("./data/lan" "./data/online")
target_files_per_dir=25 # Changed to files per directory
output_dir="./decompressed"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

for dir in "${directories[@]}"; do
  if [[ ! -d "$dir" ]]; then
    echo "Error: Directory '$dir' not found."
    continue # Move to the next directory
  fi

  decompressed_count=0 # Reset count for each directory
  
  # Find all .xz files in the directory and sort them
  find "$dir" -maxdepth 1 -type f -name "*.xz" -print0 | sort -z | while IFS= read -r -d $'\0' file; do
    if [[ $decompressed_count -lt "$target_files_per_dir" ]]; then
      echo "Processing file: $file"
      filename=$(basename "$file" .xz)
      output_file="$output_dir/$filename"
      xz -dkc "$file" > "$output_file"
      if [[ $? -eq 0 ]]; then
        echo "Decompressed: $file to $output_file"
        ((decompressed_count++))
      else
        echo "Error decompressing: $file"
      fi
    else
      echo "Reached the limit of $target_files_per_dir files for directory $dir. Skipping the rest."
      break # Exit the inner loop
    fi
  done
done

echo "Finished processing files."
exit 0

