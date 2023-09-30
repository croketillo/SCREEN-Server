"""
		SCREEN-SERVER
		Version 1.0

	Create a server http to serve images por advertising screens

 	Author: Croketillo (croketillo@gmail.com)
	GITHUB: https://github.com/croketillo
"""

import http.server
import socketserver
import threading
import time
import os
import json

# Server Configuration
PORT = 8800
IMAGE_FOLDER = "images"  # Folder where images are stored
CONFIG_FILE = "config.json"  # Configuration file

# Variables to store configuration and images
config = {}
image_list = []
current_image_data = None
current_image_index = 0


def load_config():
    # Function to load configuration from JSON file
    global config, image_list
    try:
        with open(CONFIG_FILE, "r") as config_file:
            config_data = json.load(config_file)
            config = config_data.get("config", {})
            image_list = config_data.get("images", [])
    except FileNotFoundError:
        print(f"The configuration file {CONFIG_FILE} is not found.")


def load_next_image():
    # Function to load the next image and its display duration
    global current_image_data, current_image_index
    if not image_list:
        return None  # Return None if there are no images in the configuration

    current_image_info = image_list[current_image_index]
    image_name = current_image_info.get("name", "")
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    duration = current_image_info.get("duration", 10)

    if os.path.isfile(image_path):
        with open(image_path, "rb") as f:
            current_image_data = f.read()
    else:
        print(f"The image {image_name} is not found in the folder {IMAGE_FOLDER}")

    current_image_index = (current_image_index + 1) % len(image_list)
    return duration


def serve_current_image():
    # Function to serve the current image
    if current_image_data:
        return current_image_data


def change_image_periodically():
    # Function to change the current image periodically
    while True:
        duration = load_next_image()
        if duration is not None:
            time.sleep(duration)

class ImageHandler(http.server.BaseHTTPRequestHandler):
    # HTTP Server Function
    def do_GET(self):
        if self.path == "/get_image":
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            image_data = serve_current_image()
            if image_data:
                self.wfile.write(image_data)
            else:
                self.wfile.write(b"No images available.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    load_config()

    # Create a thread to change the current image periodically
    image_change_timer_thread = threading.Thread(target=change_image_periodically)
    image_change_timer_thread.daemon = True
    image_change_timer_thread.start()

    # Start the server
    with socketserver.TCPServer(("", PORT), ImageHandler) as httpd:
        print("""
┏━┓┏━╸┏━┓┏━╸┏━╸┏┓╻ ┏━┓┏━╸┏━┓╻ ╻┏━╸┏━┓
┗━┓┃  ┣┳┛┣╸ ┣╸ ┃┗┫ ┗━┓┣╸ ┣┳┛┃┏┛┣╸ ┣┳┛
┗━┛┗━╸╹┗╸┗━╸┗━╸╹ ╹╹┗━┛┗━╸╹┗╸┗┛ ┗━╸╹┗╸

Version 1.0

        """)
        print(f"Server RUNNING at (http://0.0.0.0/get_image) in {PORT}:")
        httpd.serve_forever()
