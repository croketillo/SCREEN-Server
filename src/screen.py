# SCREEN-SERVER
# Version 2.0

# Create an HTTP server to serve images for advertising screens

# Author: Croketillo (croketillo@gmail.com)
# GITHUB: https://github.com/croketillo

import http.server
import socketserver
import threading
import time
import os
import json

print("\nSCREEN-SERVER \nVersion 1.3 \n\nBy: Croketillo (croketillo@gmail.com)")
print("\n[-----------------------------------------------]\n\n")

# Server Configuration
CONFIG_FILE = "config.json"  # Configuration file
IMAGE_FOLDER = "images"
# Variables to store configuration and images
config = {}
image_list = []
current_image_data = None
current_image_index = 0

# Function to load configuration from the JSON file
def load_config():
    global config, image_list
    try:
        with open(CONFIG_FILE, "r") as config_file:
            config_data = json.load(config_file)
            config = config_data.get("config", {})
            image_list = config_data.get("images", [])
    except FileNotFoundError:
        print(f"The configuration file {CONFIG_FILE} is not found.")

# Function to load the next image and its display duration
def load_next_image():
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

# Function to serve the current image
def serve_current_image():
    if current_image_data:
        return current_image_data

# Function to change the current image periodically
def change_image_periodically():
    while True:
        duration = load_next_image()
        if duration is not None:
            time.sleep(duration)

# HTTP Server Function
class ImageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Get the token from the Authorization header
        token = self.headers.get("Authorization")

        # Verify if the token is valid
        secret_key = config.get('SECRET_KEY')
        if token != f"Bearer {secret_key}":
            self.send_response(401)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return

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
    port=config.get('PORT', 8080)
    with socketserver.TCPServer(("",int(port) ), ImageHandler) as httpd:
        print(f"[ OK ] Server RUN on port {config.get('PORT', 8080)}...")
        httpd.serve_forever()
