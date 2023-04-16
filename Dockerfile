FROM ubuntu:focal

# Change the current directory 
WORKDIR /usr/src/app

# Create folder for volumes
RUN mkdir ./data

# Installation of the modules required for the execution of the binaries
RUN apt-get update
RUN apt-get -y install python3-pip

# Copying the code inside the Docker container
COPY . .

# Installation of requirements
RUN python3 -m pip install -r ./requirements.txt
RUN python3 setup.py install

# Execution of the compilation of binaries
CMD [ "python3", "./restapi/rest_api.py"]