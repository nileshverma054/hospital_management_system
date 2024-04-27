# <----------------------------------------- Build Stage ------------------------------------------------>

FROM python:3.12 AS build
# ?? what can't we use python:3.12-slim here itself?
# -> The python:3.12 image of python consist of apt packages required by python external libraries
# eg. if we use python:3.12-slim, then pip install mysqlclient fails due to missing libmariadb3 which comses 
# inbuilt in python:3.12
# 
# So we install the dependencies using python3.12 and copy installed packages from /usr/local in final stage. 
# Using this technique the image size is reduced from 1.1GB to 0.25GB

# Setting the working directory
WORKDIR /app

# Copying the requirements.txt file into the working directory
COPY requirements.txt /app

# Installing dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# <----------------------------------------- Final Stage ------------------------------------------------>

FROM python:3.12-slim AS final

ENV APPLICATION_LOG_PATH="/application/logs"

# Installing packages and changing ownership of directories to 'myuser'
# libmariadb3 is required by mysqlclient package
RUN useradd -ms /bin/bash myuser && \
    mkdir -p ${APPLICATION_LOG_PATH}

# Installing packages and changing ownership of directories to 'myuser'
RUN apt-get update && apt-get install libmariadb3 -y && \
    apt-get install -y nmap && \
    rm -rf /var/lib/apt/lists/* && \
    chown -R myuser:myuser ${APPLICATION_LOG_PATH}

# Switching to the user 'myuser'
USER myuser

WORKDIR /app

# Copying files from the build stage and changing their ownership to 'myuser'
COPY --chown=myuser:myuser --from=build  /usr/local /usr/local
COPY --chown=myuser:myuser --from=build /app/requirements.txt /app/requirements.txt
COPY --chown=myuser:myuser . /app
