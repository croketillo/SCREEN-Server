"""
		SCREEN-SERVER // CLIENT
		Version 1.2

	       Client for SCREEN-Server

 	Author: Croketillo (croketillo@gmail.com)
	GITHUB: https://github.com/croketillo
"""




from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import requests
import pygame
from io import BytesIO
import time

# Server Configuration


print("""

┏━┓┏━╸┏━┓┏━╸┏━╸┏┓╻   ┏━╸╻  ╻┏━╸┏┓╻╺┳╸
┗━┓┃  ┣┳┛┣╸ ┣╸ ┃┗┫╺━╸┃  ┃  ┃┣╸ ┃┗┫ ┃ 
┗━┛┗━╸╹┗╸┗━╸┗━╸╹ ╹   ┗━╸┗━╸╹┗━╸╹ ╹ ╹ 
Version 1.1

By: Croketillo (croketillo@gmail.com)      
      

Press [ESC] to quit.
""")

print("Enter the server URL (example: http://localhost:8080/get_image)")
SERVER_URL = input(">>> URL: ")
SECRET_KEY = input(">>> Enter the KEY: ")
# Initialize pygame
pygame.init()

# Get screen information
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set up the screen to full screen with detected size
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Server Image")

running = True

while running:
    try:
        # Request the image from the server with the token in the headers
        headers = {"Authorization": f"Bearer {SECRET_KEY}"}
        response = requests.get(SERVER_URL, headers=headers)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image = pygame.image.load(image_data)

            # Scale the image to the screen size
            image = pygame.transform.scale(image, (screen_width, screen_height))

            # Display the image in full screen
            screen.blit(image, (0, 0))
            pygame.display.flip()

        # Capture window close events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    except Exception as e:
        print(f"Error: {e}")

    # Wait for some time before requesting the next image
    time.sleep(1)  # Change the image every 5 seconds

    # Return to the beginning of the folder if images run out
    if response.status_code != 200:
        response = requests.get(SERVER_URL)
        time.sleep(1.5)  # Give the server time to change the image

pygame.quit()
