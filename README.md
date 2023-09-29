# SCREEN-SERVER

Screen-server is an open-source client-server program that serves images through an HTTP server.

## SERVER
### First things first.

Prepare the images to be displayed in a directory. Keep in mind that the images should have the resolution and aspect ratio suitable for the screen where they will be displayed since SCREEN-CLIENT detects the screen and resizes them accordingly.

#### STEP 1 - Clone the repository and navigate to the directory

git clone *******************
cd screen-server

#### STEP 2 - Run config.sh and follow the instructions:

./config.sh

Specify the path where you store the images you want to display, and it will automatically ask you how long you want to display each image. The data is loaded into the "config.json" file.

You can also do it manually by placing the images in the ./images folder and modifying the "config.json" file.

#### STEP 3 - Choose an execution mode:
##### Directly run the script or the binary (Not recommended)

python3 screen.py

#### DOCKER
##### Create a Docker image with:

docker build -t screen .

##### Start the Docker container with:

docker-compose up -d

## CLIENT

The client is prepared to run on small Linux machines installed for promotional and marketing screens by running the Python script or the binary.

Simply load the binary onto the client machine and specify the URL of the server; it will immediately load the images with the configuration loaded on the server indefinitely until you press ESC


