#!/bin/sh

# Install necessary packages
apt-get update
apt-get install -y ffmpeg libasound2 libasound2-dev libpulse0 libpulse-dev libpulsedsp libpulse-mainloop-glib0

# Clean up
apt-get clean
rm -rf /var/lib/apt/lists/*