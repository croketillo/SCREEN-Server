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
        Wizard-Config v1.2${NC}

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
            echo "[ERROR] Invalid port number. Please enter a valid port."
        fi
    done
}


# Prompt the user for a secret key
read -s -p"[ >> ] Enter the secret key: " secret_key
echo ""

# Update SECRET_KEY in screen_secure.py
sed -i "s/SECRET_KEY = .*/SECRET_KEY = \"$secret_key\"/" screen.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[ OK ] - The KEY is wirten in screen.py"
    echo ""
    # OK
else
    echo "\n[ ERROR$ ] - Can't wirte the KEY in screen.py"
    ERROR=1
    # FAIL
fi

# Update SECRET_KEY in client/client_secure.py
sed -i "s/SECRET_KEY = .*/SECRET_KEY = \"$secret_key\"/" client/client.py

if [ $? -eq 0 ]; then
    echo "[ OK$ ] - The KEY is wirten in client/client.py"
    echo ""
    # OK
else
    echo "[ ERROR$ ] - Can't wirte the KEY in client/client.py"
    ERROR=1
    # FAIL
fi

# Get the port number from the user
port=$(read_port)

# Update the port in the screen.py file
sed -i "s/PORT = [0-9]\+/PORT = $port/" screen.py

if [ "$ERROR" -eq 0 ]; then
    echo -e "\n[ ${GREEN}OK${NC} ] The configuration has been successfull"
else
    echo "[ ${RED}ERROR${NC} ] - The configuration fail"
fi