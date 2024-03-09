#!/bin/bash
DATA_PATH=$(dirname $(realpath -s $0))/data

container_exists() {
    if [ "$(docker ps -a | grep $1)" ]; then
        return 0
    else
        return 1
    fi
}

process_data() {
    echo "Purging ${DATA_PATH}"
    rm -rf $"DATA_PATH"
    docker rm osrm-extract osrm-partition osrm-customize &> /dev/null || true

    # re-generate input data for the service
    wget -P $DATA_PATH http://download.geofabrik.de/north-america/us/ohio-latest.osm.pbf
    docker run --name osrm-extract -t -v "${DATA_PATH}:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/ohio-latest.osm.pbf
    docker run --name osrm-partition -t -v "${DATA_PATH}:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/ohio-latest.osrm
    docker run --name osrm-customize -t -v "${DATA_PATH}:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/ohio-latest.osrm 
}

run_service() {
    if ! [ -d  "${DATA_PATH}" ]; then
        echo "DATA directory doesn't exist. Exiting..."
        exit 1
    fi

    if ! container_exists osrm-server; then
        docker run --name osrm-server -t -i -p 5000:5000 -v "${DATA_PATH}:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/ohio-latest.osrm
    else
        docker start osrm-server &> /dev/null || echo "Unable to start the OSRM service"
    fi
}

stop_service() {
    docker stop osrm-server &> /dev/null || true
}

help()
{
   # Display Help
   echo "Runs OSRM service related functions."
   echo
   echo "Syntax: osrm [-h|g|r]"
   echo "options:"
   echo "g     Generate the OSRM map data."
   echo "s     Start the OSRM service."
   echo "e     Exit the OSRM service."
   echo "h     Print this help."
}

while getopts "hgse" option; do
   case $option in
        h) # display Help
            help
            ;;
        g) # generate data
            process_data
            ;;
        s) # Run service
            run_service
            ;;
        e) # Stop service
            stop_service
            ;;
   esac
done

if [ $OPTIND -eq 1 ]; then
    help
fi


