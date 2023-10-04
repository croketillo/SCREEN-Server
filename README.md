![log](https://github.com/croketillo/screen-server/assets/131451882/1f365bd5-bb93-4e3c-9e12-e9db1ee49127)

# SCREEN-SERVER

SCREEN-SERVER is an open-source client-server program that serves images through an HTTP server.


## SERVER
### First things first.

Prepare the images to be displayed in a directory. Keep in mind that the images should have the resolution and aspect ratio suitable for the screen where they will be displayed since SCREEN-CLIENT detects the screen and resizes them accordingly.

#### STEP 1 - Clone the repository and navigate to the directory

```git clone https://github.com/croketillo/screen-server.git```

cd screen-server

#### STEP 2 - Run config.sh and follow the instructions:

./config.sh

You has to specify the server port


#### STEP 3 - Choose an execution mode:
##### Directly run the script

python3 screen.py

##### DOCKER
###### Create a Docker image with:

docker build -t screen .

###### Start the Docker container with:

docker-compose up -d

###### CHECK THE SERVER RUNNING 

http://{YOUR_HOST}/get_images



##### For update images:

./update_imges.sh

Then, specify the path where you store the images you want to display, and it will automatically ask you how long you want to display each image. The data is loaded into the "config.json" file.

You can also do it manually by placing the images in the ./images folder and modifying the "config.json" file.



docker restart {YOUR_CONTAINER}



## CLIENT

The client is prepared to run on small Linux machines installed for promotional and marketing screens by running the Python script.

Simply load the script  onto the client machine and specify the URL of the server; it will immediately load the images with the configuration loaded on the server indefinitely until you press ESC


