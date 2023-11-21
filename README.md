# Optimize The Drive
##### Nathan Dunn and Jacob Poling

### Development Setup
_Note: It's recommend to use an Enterprise Linux distrubtion for the development of this application. Currently we are using Rocky Linux 9._

- Install Docker
- Spin up the API service: 
    ```
    docker compose -f docker/compose.dev.yaml build
    docker compose -f docker/compose.dev.yaml up [-d]
    ```
- Start up the OSRM server:
    ```
    osrm-service/start-service.sh
    ```

- Since we are using docker for development, there isn't an easy way to get local linting, so it's recommended to install   **venv** in the root directory of the project and install all dependencies there.

**Its really that easy! You can start developing right away.**

