# Use Debian as a parent image
FROM ubuntu:latest

# Update the package index and install necessary packages
RUN apt update && apt install -y \ 
    ruby ruby-bundler ruby-dev \
    nano \
    systemctl \
    nginx \ 
    build-essential \ 
 && rm -rf /var/lib/apt/lists/* 

# nginx # Need for redirect request from docker container to outside


# Set the working directory to /app
WORKDIR /app

# Display Ruby version and bundler version
RUN ruby --version && bundle --version && gem install bundler jekyll

# Command to run when the container starts
CMD ["irb"]

# docker build -t github.io-ruby-env .