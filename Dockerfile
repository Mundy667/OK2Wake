# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:2.7.13-jessie

# What does the following run do? Installs, NGINX
# removes the config files
# changes the timezone to Berlin 
# and then installs the rpi.gpio python module

RUN apt-get update && apt-get install -y \
nginx php-fpm \ 
&& rm -rf /var/lib/apt/lists/* \
#&& rm /etc/nginx/conf.d/default.conf \
#&&  rm /etc/nginx/conf.d/examplessl.conf \
&& echo "Europe/Berlin" > /etc/timezone \
&& dpkg-reconfigure -f noninteractive tzdata  \
&& pip install --no-cache-dir rpi.gpio 

# Copy the Python Script for OK2Wake
COPY ok2wake.py ./

# Trigger Python script
CMD ["python", "./ok2wake.py"]
