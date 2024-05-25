#!/bin/sh

# Update package list
apt-get update

# Add deb-multimedia repository for ffmpeg
echo "deb http://www.deb-multimedia.org stretch main non-free" >> /etc/apt/sources.list
apt-get update

# Install deb-multimedia-keyring to avoid key verification errors
apt-get install -y --allow-unauthenticated deb-multimedia-keyring
apt-get update

# Install necessary packages
apt-get install -y --allow-unauthenticated ffmpeg libasound2 libasound2-dev libpulse0 libpulse-dev libpulsedsp libpulse-mainloop-glib0

# Clean up
apt-get clean
rm -rf /var/lib/apt/lists/*