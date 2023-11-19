#!/bin/bash

container_exists() {
    if [ "$(docker ps -a | grep $1)" ]; then
        return 0
    else
        return 1
    fi

}

# Download Open Street Maps Extracts
if ! [ -f ./data/ohio-latest.osm.pbf ]; then
    echo "BOOTY CHEEKS"
    wget -P data http://download.geofabrik.de/north-america/us/ohio-latest.osm.pbf
fi
if ! container_exists osrm-extract ; then
    docker run --name osrm-extract -t -v "${PWD}/data:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/ohio-latest.osm.pbf || echo "osrm-extract failed"
fi
if ! container_exists osrm-partition ; then
    docker run --name osrm-partition -t -v "${PWD}/data:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/ohio-latest.osrm || echo "osrm-partition failed"
fi
if ! container_exists osrm-customize ; then
    docker run --name osrm-customize -t -v "${PWD}/data:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/ohio-latest.osrm || echo "osrm-customize failed"
fi
if ! container_exists server ; then
    docker run --name server -t -i -p 5000:5000 -v "${PWD}/data:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/ohio-latest.osrm
else
    docker start server
fi

