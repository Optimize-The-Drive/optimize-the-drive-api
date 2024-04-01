# Optimize The Drive
##### Nathan Dunn and Jacob Poling

### Development Setup
_Note: It's recommend to use an Enterprise Linux distrubtion for the development of this application. Currently we are using Rocky Linux 9._

- Ensure Docker, Python 3 and [Nix package manager](https://nixos.org/download/) are installed.
- Generate OSRM data (for OSRM service to consume):
    ```
        ./generate_osrm
    ```
- Spin up the backend service: 
    ```
    docker compose -f compose.dev.yaml build
    docker compose -f compose.dev.yaml up [api] [db] [osrm] (can run individual components if needed)
    ```
- Start the Frontend:
    ```
        nix-shell
        cd frontend/ && npm install
        npm start
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
./tests [--build] --run
```

### Creating and Running Migrations
* To create a migration script with latest changes: `docker exec -it flask-api flask db migrate`
* To upgrade to the next migration: `docker exec -it flask-api flask db upgrade`
* To revert back to the previous migration: `docker exec -it flask-api flask db downgrade`