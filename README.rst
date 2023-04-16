===================
Technical assignment
===================

This is the technical assignment repository. This file contains instructions on how to run the code and the tests, as well as an explanation on the folder structure.

---------------

Project folder structure
----------------

The notebooks folder contains the first solution approach. May be useful to get a grasp on the fundamental ideas.

The core folder contains the OOP structure that will be used in the script. Provides input/output path consistensy, custom exceptions, and methods to scale an image and a label file following technical requirements.

The script folder contains the script that scales the given data.

The restapi folder contains a simple tornado based Rest API.

The tests folder contains all the unittest. Continue reading to know how to easily run the unittest.

The utils folder contains customized loggers.

----------------

Running with Docker
-----------------

If Docker is installed on your machine:

``docker-compose up -d``

There must be an environment variable called ``REST_DATA_PATH`` set to the path where the data is stored following Kitti Format.

When deploying the container, the Rest API will be running on port 8080.

``http://localhost:8080``

There is a simple user authentication needed to run the get request that will scale the provided data. 

The only allowed users are: "jponte98@gmail.com" and "trifork@emails.homerun.co" (see ``./restapi/config.py``)

The following URL is an example on how to get an authentication token that will be needed for the requests

``http://localhost:8080/auth?user_id=jponte98@gmail.com``

Keep the token and use it in the headers so that the Rest API can authenticate you. (i.e. There must be the following header in the get request: ``Authorization: bearer <token>``)

The following URL will scale the provided data

``http://localhost:8080/images``


----------------

Running script
-----------------

Another possibility is to simply run the script. Although we must first install the package.

``python3 setup.py install``

``python3 ./script/run.py [OPTIONS]``

Option description:

Name, shorthand | Default | Description 
--- | --- | --- | 
--target_width | 284 | target image width
--target_height | 284 | target image height
--input_path | '' | path to data
--output_path | '' | path to store scaled images and annotations

----------------

Running the tests
-----------------

  ``python3 ./tests/runner.py ``
