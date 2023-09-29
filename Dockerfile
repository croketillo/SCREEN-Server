# Use a lightweight Alpine Linux base image
FROM alpine:3.13

# Copy the Python script to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Install Python and pip
RUN apk --update add python3

# Expose the port
EXPOSE 8800

# Run the Python script
CMD ["python3", "screen.py"]


