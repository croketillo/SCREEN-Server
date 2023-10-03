import http.server
import socketserver
import threading
import time
import os
import json

# Server Configuration
PORT = 8800
IMAGE_FOLDER = "images"  # Carpeta donde se almacenan las imágenes
CONFIG_FILE = "config.json"  # Archivo de configuración

# Secret key for generating and validating tokens
SECRET_KEY = "123456"

# Variables para almacenar la configuración y las imágenes
config = {}
image_list = []
current_image_data = None
current_image_index = 0

# Función para cargar la configuración desde el archivo JSON
def load_config():
    global config, image_list
    try:
        with open(CONFIG_FILE, "r") as config_file:
            config_data = json.load(config_file)
            config = config_data.get("config", {})
            image_list = config_data.get("images", [])
    except FileNotFoundError:
        print(f"El archivo de configuración {CONFIG_FILE} no se encuentra.")

# Función para cargar la siguiente imagen y su tiempo de visualización
def load_next_image():
    global current_image_data, current_image_index
    if not image_list:
        return None  # Devolver None si no hay imágenes en la configuración

    current_image_info = image_list[current_image_index]
    image_name = current_image_info.get("name", "")
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    duration = current_image_info.get("duration", 10)

    if os.path.isfile(image_path):
        with open(image_path, "rb") as f:
            current_image_data = f.read()
    else:
        print(f"La imagen {image_name} no se encuentra en la carpeta {IMAGE_FOLDER}")

    current_image_index = (current_image_index + 1) % len(image_list)
    return duration

# Función para servir la imagen actual
def serve_current_image():
    if current_image_data:
        return current_image_data

# Función para cambiar la imagen actual periódicamente
def change_image_periodically():
    while True:
        duration = load_next_image()
        if duration is not None:
            time.sleep(duration)

# Función para el servidor HTTP
class ImageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Obtener el token del encabezado de autorización
        token = self.headers.get("Authorization")

        # Verificar si el token es válido
        if token != f"Bearer {SECRET_KEY}":
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

    # Crear un subproceso para cambiar la imagen actual periódicamente
    image_change_timer_thread = threading.Thread(target=change_image_periodically)
    image_change_timer_thread.daemon = True
    image_change_timer_thread.start()

    # Iniciar el servidor
    with socketserver.TCPServer(("", PORT), ImageHandler) as httpd:
        print(f"Servidor activo en el puerto {PORT}")
        httpd.serve_forever()
