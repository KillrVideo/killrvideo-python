# killrvideo-python
Python implementation of KillrVideo service layer. Requires Python 3.

Dependencies: 
* To run locally, recommend using `venv` to create a Python virtual environment, which leverages the contents 
of `requirements.txt` (see below)
* Otherwise, you can build the dependencies locally by emulating the `pip install` commands in `Dockerfile`. 


Install and run:
* Clone this repo
    * `git clone <>`
    * `cd killrvideo-python`
* Create Python virtual environment
    * `python3 -m venv venv`
    * `source venv/bin/activate`
* Run supporting infrastructure using Docker
    * See the instructions in the [killrvideo-docker-common][https://github.com/KillrVideo/killrvideo-docker-common] repository for running the supporting infrastructure 
    * The documentation describes an option to run the KillrVideo python services in a Docker container
* Run the Python KillrVideo services
    * `python killrvideo/__init__.py`
