# Jenkins plugins compatibility list

This Python script performs two different operations:

- it creates a list of plugins that are currently installed in your Jenkins server
- then it creates another list with the latest version of the plugins from the step above that are compatible with the Jenkins version passed as argument

## How to use it

The suggested way to use this script is by running it inside a container:

- Clone the repository locally
- Open a terminal and execute:
  - `docker run -ti -v $(pwd):/root python:latest /bin/bash`
- Once inside the container run:
  - `pip install -r requirements.txt`
- Then you can execute the script (see section below)

If you don't want to use a container you can run the script in your local environment as long as you have python3 installed. If you run it in your local environment it is suggested to use python virtual environments.

## Usage

- Simple run with a plugin_list.csv already downloaded
  - `python3 main.py -jv 1.580.1`
- Simple run with download
  - `python3 main.py -d -jh localhost -jusr admin -jpwd -jv 1.580.1`
- Get usage message
  - `python3 main.py`

## Test

- python -m unittest
