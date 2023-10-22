# SCREEN-SERVER CONFIG
# Version 2.0

# Configure menu for SCREEN-SERVER

# Author: Croketillo (croketillo@gmail.com)
# GITHUB: https://github.com/croketillo

from rich.console import Console
import json
import os
import shutil

console = Console()
JSON_FILE = "config.json"

def show_menu():
    console.print("\nSCREEN SERVER CONFIG\n", style="bold yellow underline")
    console.print("1) VIEW CONFIGURATION")
    console.print("2) CONFIGURE SERVER")
    console.print("3) UPDATE IMAGES")
    console.print("\nQ) QUIT")
    option = input("\nSelect an option (Q to quit): ")
    return option

def load_json_as_dictionary(file_name):
    try:
        with open(file_name, 'r') as file:
            dictionary = json.load(file)
        return dictionary
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def show_config():
    dict = load_json_as_dictionary(JSON_FILE)
        
    console.print("\nCURRENT CONFIGURATION\n", style="bold red underline")
    console.print("[bold]SECRET KEY:[/bold]\t" + str(dict["config"]['SECRET_KEY']))
    console.print("[bold]PORT:[/bold]\t" + str(dict["config"]['PORT']))
    print("\n")
    console.print("LOADED IMAGES\n", style="bold red underline")
    for image in dict['images']:
        console.print(image['name'], "\t - ", image['duration'], "sec.")
    print("\n")    
    option = input("Q to go Back:")
    return option

def insert_config():
    console.print("\nCONFIGURE SERVER", style="bold red underline")
    secret_key = input("Enter the new secret key: ")
    port = input("Enter the port: ")
    return secret_key, port

def modify_config_in_json(json_file, new_secret_key, new_port):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Modify values in the "config" dictionary
        data["config"]["SECRET_KEY"] = new_secret_key
        data["config"]["PORT"] = new_port

        # Save the changes to the JSON file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Values modified successfully in '{json_file}'")
    except FileNotFoundError:
        print(f"File '{json_file}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding the JSON file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def process_files_in_directory(user_path):
    try:
        # "images" folder in the same directory as the script
        images_folder = "images"

        # Check if the "images" folder exists, and if not, create it
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        # List and delete all files in the "images" folder
        for file in os.listdir(images_folder):
            file_path = os.path.join(images_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Iterate over the path provided by the user
        for file in os.listdir(user_path):
            file_path = os.path.join(user_path, file)
            if os.path.isfile(file_path):
                # Check if it's a JPG or PNG file
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    # Copy the found file to the "images" folder
                    shutil.copy(file_path, os.path.join(images_folder, file))
                    print(f"File {file} copied to the 'images' folder in the current directory")

        print("Process completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_config_json():
    # "images" folder in the same directory as the script
    images_folder = "images"

    try:
        # Load the "config.json" file
        config_json_path = "config.json"  # Make sure the location is correct
        with open(config_json_path, 'r') as config_file:
            config_data = json.load(config_file)

        # Get the list of files in the "images" folder
        image_files = [file for file in os.listdir(images_folder) if file.lower().endswith((".jpg", ".jpeg", ".png"))]

        # Clear existing keys in "images"
        config_data["images"] = []

        # Update the list of images in "config.json" with user-provided duration
        for file in image_files:
            duration = input(f"Enter the exposure time for '{file}' (seconds): ")
            config_data["images"].append({"name": file, "duration": int(duration)})

        # Save the changes to "config.json"
        with open(config_json_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

        print("File 'config.json' updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    os.system("clear")
    option = show_menu()
    if option == "1":
        os.system("clear")
        while True:
            option = show_config()
            if option == "Q" or option == "q":
                break
    elif option == "2":
        os.system("clear")
        conf = insert_config()
        secret_key = conf[0]
        port = conf[1]
        modify_config_in_json(JSON_FILE, secret_key, port)
    elif option == "3":
        os.system("clear")
        console.print("\nUPDATE IMAGES\n", style="bold red underline")
        path = input("Enter the path of the folder where the images are located: ")
        process_files_in_directory(path)
        update_config_json()
    elif option == "Q" or option == "q":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid option. Please choose a valid option.")
