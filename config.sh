#!/bin/bash

# Set color format
RED='\033[1;31m'
GREEN='\033[1;32m'
PINK='\033[1;35m'
NC='\033[0m'

echo -e """${PINK}

┏━┓┏━╸┏━┓┏━╸┏━╸┏┓╻ ┏━┓┏━╸┏━┓╻ ╻┏━╸┏━┓
┗━┓┃  ┣┳┛┣╸ ┣╸ ┃┗┫ ┗━┓┣╸ ┣┳┛┃┏┛┣╸ ┣┳┛
┗━┛┗━╸╹┗╸┗━╸┗━╸╹ ╹╹┗━┛┗━╸╹┗╸┗┛ ┗━╸╹┗╸
        Wizard-Config v1.0${NC}
"""

# User-provided image folder path
read -p "[ >> ] Enter the path of the folder with images: " image_folder

# Check if the image folder exists
if [ ! -d "$image_folder" ]; then
    echo -e "\n[ ${RED}ERROR${NC} ] The specified image folder does not exist."
    exit 1
fi

# Get the list of jpg and png files in the provided folder
image_files=$(find "$image_folder" -type f \( -iname \*.jpg -o -iname \*.png \))

# Check if files were found
if [ -z "$image_files" ]; then
    echo "\n[ ${RED}ERROR${NC} ] No JPG or PNG files were found in the specified folder."
    exit 1
fi

# Remove all existing entries in the config.json file
echo "{\"config\": {}, \"images\": [" > config.json

# Iterate over the found files
first_iteration=true
for image_path in $image_files; do
    # Get the file name without the path
    image_name=$(basename "$image_path")

    # Request exposure time in seconds
    read -p "[ >> ] Exposure time for $image_name (in seconds): " exposure_time

    # Check if it's the first iteration
    if [ "$first_iteration" = true ]; then
        first_iteration=false
    else
        # Add a comma before the next entry
        echo "," >> config.json
    fi

    # Add the information to the config.json file
    json_line="{\"name\": \"$image_name\", \"duration\": $exposure_time}"
    echo -n "$json_line" >> config.json

    # Copy the image to the "images" directory
    cp "$image_path" "images/"
done

# Close the config.json file
echo "]}" >> config.json

echo -e "\n[ ${GREEN}OK${NC} ] The config.json file has been successfully generated."
