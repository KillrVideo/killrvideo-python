# killrvideo-python
Python implementation of KillrVideo service layer. Requires Python 3.

Install:
* Clone this repo
    * `git clone <>`
    * `cd killrvideo-python`
    
Dependencies:
* To run the Python services, we recommend using `venv` to create a Python virtual environment, which leverages the contents 
of `requirements.txt` to install the required Python libraries
    * `python3 -m venv venv`
    * `source venv/bin/activate`
* Alternatively, you can build the dependencies locally by emulating the `pip install` commands in `Dockerfile`. 

Running Python services in Docker:
* Run the script to build the Docker container:
    * `scripts/docker-build.sh`  
* Run the services and supporting infrastructure in Docker
    * `docker-compose up -d`
    
(Alternate) Running the Python Services on the host (not in docker):   
* Run supporting infrastructure using Docker
    * `scripts/run-docker-backend-exernal.sh`
    * Note this script makes use of the custom compose file `scripts/docker-compose-backend-external.yaml`, which references the environment variable `KILLRVIDEO_BACKEND`. The script sets this to the host IP.
* Run the Python services
    * In your IDE or shell, set the environment variables `KILLRVIDEO_DSE_CONTACT_POINTS` and `KILLRVIDEO_KAFKA_BOOTSTRAP_SERVERS` to point to localhost (`127.0.0.1`)
    * `python killrvideo/__init__.py`
    * To stop the docker services, run `scripts/stop-docker-backend-external.sh`

For more advanced Docker configuration options including metrics, volume storage and OpsCenter, see the [killrvideo-docker-common](https://github.com/KillrVideo/killrvideo-docker-common) repository.  

