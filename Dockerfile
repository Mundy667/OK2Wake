# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:2.7.13-jessie

# Copy the Python Script for OK2Wake
COPY ok2wake.py ./

# RUN apt-get update && apt-get install -y \
# && rm -rf /var/lib/apt/lists/*

RUN echo "Europe/Berlin" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata  

# Intall the rpi.gpio python module
RUN pip install --no-cache-dir rpi.gpio

# Trigger Python script
CMD ["python", "./ok2wake.py"]
