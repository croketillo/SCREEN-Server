![logo](https://github.com/croketillo/SCREEN-Server/assets/131451882/b01b209d-e4a6-4304-bda3-985651cfa992)


# SCREEN-SERVER

SCREEN-SERVER is an open-source client-server program that serves images through an HTTP server for remote advertising screens.


## SERVER
### First things first.

Prepare the images to be displayed in a directory. Keep in mind that the images should have the resolution and aspect ratio suitable for the screen where they will be displayed since SCREEN-CLIENT detects the screen and resizes them accordingly.

#### STEP 1 - Clone the repository and navigate to the directory

```git clone https://github.com/croketillo/screen-server.git```

```cd screen-server ```

```pip install -r requirements.txt ```

#### STEP 2 - Run config.sh and follow the instructions:


To enter the configuration menu:

```python3 /src/config.py ```

To upload new images you must enter the full path of the directory where you store your images locally. (Ex.  /home/user/new_images )

**Remember to restart the server so that the changes are applied if you are using docker**


#### STEP 3 - Choose an execution mode:
##### Directly run the script

```python3 screen.py```

##### DOCKER
###### Create a Docker image with:

```docker build -t screen .```

###### Start the Docker container with Docker-compose:

```docker-compose up -d```

###### CHECK THE SERVER RUNNING 

http://{YOUR_HOST}/get_image



## CLIENT

The client is prepared to run on small Linux machines installed for promotional and marketing screens by running the Python script.

Simply load the script  onto the client machine and specify the URL of the server; it will immediately load the images with the configuration loaded on the server indefinitely until you press ESC


