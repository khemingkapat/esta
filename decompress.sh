#!/bin/bash

declare -a directories=("./data/lan" "./data/online")
declare -A decompressed_counts
target_files=50

# Initialize decompressed counts for each directory
for dir in "${directories[@]}"; do
  decompressed_counts["$dir"]=0
done

for dir in "${directories[@]}"; do
  if [[ ! -d "$dir" ]]; then
    echo "Error: Directory '$dir' not found."
    continue # Move to the next directory
  fi

  # Find all .xz files in the directory and sort them (optional, but can help with consistency)
  find "$dir" -maxdepth 1 -type f -name "*.xz" -print0 | sort -z | while IFS= read -r -d $'\0' file; do
    if [[ ${decompressed_counts["$dir"]} -lt $((target_files / ${#directories[@]})) ]]; then
      echo "Processing file: $file"
      filename=$(basename "$file" .xz)
      output_file="./decompressed/$filename"
      mkdir -p "./decompressed" # Ensure the output directory exists
      xz -dkc "$file" > "$output_file"
      if [[ $? -eq 0 ]]; then
        echo "Decompressed: $file to $output_file"
        ((decompressed_counts["$dir"]++))
      else
        echo "Error decompressing: $file"
      fi
    fi
  done
done

# Handle any remaining files if target_files is not perfectly divisible by the number of directories
remaining_files=$((target_files - ${decompressed_counts["./data/lan"]} - ${decompressed_counts["./data/online"]}))

if [[ $remaining_files -gt 0 ]]; then
  echo "Decompressing remaining $remaining_files files from the first directory..."
  dir="${directories[0]}"
  find "$dir" -maxdepth 1 -type f -name "*.xz" -print0 | sort -z | while IFS= read -r -d $'\0' file; do
    if [[ ${decompressed_counts["$dir"]} -lt "$target_files" ]]; then
      echo "Processing file: $file"
      filename=$(basename "$file" .xz)
      output_file="./decompressed/$filename"
      mkdir -p "./decompressed" # Ensure the output directory exists
      xz -dkc "$file" > "$output_file"
      if [[ $? -eq 0 ]]; then
        echo "Decompressed: $file to $output_file"
        ((decompressed_counts["$dir"]++))
      else
        echo "Error decompressing: $file"
      fi
    fi
  done
fi

echo "Finished processing up to $target_files files."

exit 0
