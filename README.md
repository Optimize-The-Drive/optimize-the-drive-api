# Optimize The Drive
##### Nathan Dunn and Jacob Poling

### Development Setup
_Note: It's recommend to use an Enterprise Linux distrubtion for the development of this application. Currently we are using Rocky Linux 9._

- Ensure Docker and Python 3 are installed
- Spin up the API service: 
    ```
    docker compose -f compose.dev.yaml build
    docker compose -f compose.dev.yaml up [-d]
    ```
- Start up the OSRM server:
    ```
    osrm-service/start-service.sh
    ```

- Since we are using docker for development, there isn't an easy way to get local linting, so it's recommended to install   **venv** in the root directory of the project and install all dependencies there.

**Its really that easy! You can start developing right away.**

### Linting
To run the lint, ensure you have installed the virtual environment setup.
* Drop into the python virtual environment: `source venv/bin/activate`
* run the linter: `pylint  --rcfile=.pylintrc flask-api/`

### Running Tests
Running the tests is very simple. A separate docker configuration is included for running them:
```
docker compose -f compose.ci.yaml up --abort-on-container-exit
```