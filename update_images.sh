#!/bin/bash

# Set color format
RED='\033[1;31m'
GREEN='\033[1;32m'
PINK='\033[1;35m'
NC='\033[0m'

# Variable to track errors
error_occurred=false

echo -e """${GREEN}

 _______ _______  ______ _______ _______ __   _     _______ _______  ______ _    _ _______  ______
 |______ |       |_____/ |______ |______ | \  | ___ |______ |______ |_____/  \  /  |______ |_____/
 ______| |_____  |    \_ |______ |______ |  \_|     ______| |______ |    \_   \/   |______ |    \_
                                                                                                  
                                         UPDATE IMAGES${NC}

By: Croketillo (croketillo@gmail.com)
"""

# User-provided image folder path
read -p "[ >> ] Enter the path of the folder with images: " image_folder

# Check if the image folder exists
if [ ! -d "$image_folder" ]; then
    echo -e "\n[ ${RED}ERROR${NC} ] The specified image folder does not exist."
    error_occurred=true
else
    # Get the list of jpg and png files in the provided folder
    image_files=$(find "$image_folder" -type f \( -iname \*.jpg -o -iname \*.png \))

    # Check if files were found
    if [ -z "$image_files" ]; then
        echo -e "\n[ ${RED}ERROR${NC} ] No JPG or PNG files were found in the specified folder."
        error_occurred=true
    else
        # Iterate over the found files and prompt for exposure time
        image_list="\"images\": ["
        first_iteration=true
        for image_path in $image_files; do
            # Get the file name without the path
            image_name=$(basename "$image_path")

            # Request exposure time in seconds
            read -p "[ >> ] Exposure time for $image_name (in seconds): " exposure_time

            if [ "$first_iteration" = true ]; then
                first_iteration=false
            else
                image_list="$image_list, "
            fi

            image_list="$image_list{\"name\": \"$image_name\", \"duration\": $exposure_time}"
        done
        image_list="$image_list]"

        # Create a temporary JSON file
        tmp_file=$(mktemp)
        echo "{" > $tmp_file
        echo "    \"config\": {" >> $tmp_file
        echo "        \"SECRET_KEY\": \"YOUR_PASSWORD\"," >> $tmp_file
        echo "        \"PORT\": 12345" >> $tmp_file
        echo "    }," >> $tmp_file
        echo "    $image_list" >> $tmp_file
        echo "}" >> $tmp_file

        # Replace the original config.json with the temporary file
        mv $tmp_file config.json

        echo -e "\n[ ${GREEN}OK${NC} ] Updated images successfully"
    fi
fi

# Check if errors occurred
if [ "$error_occurred" = true ]; then
    echo -e "\n[ ${RED}ERROR${NC} ] There were errors during the execution."
fi
