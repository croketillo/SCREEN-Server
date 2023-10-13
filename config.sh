#!/bin/bash

# Set color format
RED='\033[1;31m'
GREEN='\033[1;32m'
PINK='\033[1;35m'
NC='\033[0m'

ERROR=0

echo -e """${PINK}

┏━┓┏━╸┏━┓┏━╸┏━╸┏┓╻ ┏━┓┏━╸┏━┓╻ ╻┏━╸┏━┓
┗━┓┃  ┣┳┛┣╸ ┣╸ ┃┗┫ ┗━┓┣╸ ┣┳┛┃┏┛┣╸ ┣┳┛
┗━┛┗━╸╹┗╸┗━╸┗━╸╹ ╹╹┗━┛┗━╸╹┗╸┗┛ ┗━╸╹┗╸
        Wizard-Config v1.3${NC}

By: Croketillo (croketillo@gmail.com)
"""
# Function to prompt for a valid port number
read_port() {
    local port
    while true; do
        read -p "[ >> ] Enter the port number for the server (between 1 and 65535): " port
        if [[ $port =~ ^[1-9][0-9]{0,4}$ && $port -ge 1 && $port -le 65535 ]]; then
            echo "$port"
            break
        else
            echo -e "\n[ ${RED}ERROR${NC} ] Invalid port number. Please enter a valid port."
        fi
    done
}

# Function to prompt for a secret key
read_secret_key() {
    local secret_key
    read -p "[ >> ] Enter the secret key: " secret_key
    echo "$secret_key"
}

# Function to confirm the secret key
confirm_secret_key() {
    local secret_key
    read -p "[ >> ] Confirm the secret key: " secret_key
    echo "$secret_key"
}

# Prompt the user for a secret key
secret_key=$(read_secret_key)

# Prompt the user to confirm the secret key
confirm_key=$(confirm_secret_key)

# Check if the secret key and confirmation match
if [ "$secret_key" != "$confirm_key" ]; then
   echo -e "\n[ ${RED}ERROR${NC} ] Secret key and confirmation do not match. Please try again."
    exit 1
fi

# Update the secret key in the config.json file
echo "Updating SECRET_KEY in config.json"
echo "$secret_key" > temp_secret_key.txt
python3 <<EOF
import json

# Read the current config.json
with open('config.json', 'r') as f:
    config_data = json.load(f)

# Update the SECRET_KEY
with open('temp_secret_key.txt', 'r') as f:
    secret_key = f.read().strip()
config_data['config']['SECRET_KEY'] = secret_key

# Write back to config.json
with open('config.json', 'w') as f:
    json.dump(config_data, f, indent=4)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "\n[ ${GREEN}OK${NC} ] - The SECRET_KEY is written in config.json"
    echo ""
    # OK
else
    echo -e "[ ${RED}ERROR${NC} ] - Can't write the SECRET_KEY in config.json"
    ERROR=1
    # FAIL
fi

# Get the port number from the user
port=$(read_port)

# Update the port in the config.json file
echo "Updating PORT in config.json"
python3 <<EOF
import json

# Read the current config.json
with open('config.json', 'r') as f:
    config_data = json.load(f)

# Update the PORT
config_data['config']['PORT'] = $port

# Write back to config.json
with open('config.json', 'w') as f:
    json.dump(config_data, f, indent=4)
EOF

if [ "$ERROR" -eq 0 ]; then
    echo -e "\n[ ${GREEN}OK${NC} ] The configuration has been successful"
else
    echo "[ ${RED}ERROR${NC} ] - The configuration failed"
fi

# Remove temporary files
rm temp_secret_key.txt
