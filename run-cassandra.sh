#!/bin/bash

docker network create dulher-cassandra-network
docker run --name cassandra-node --network dulher-cassandra-network -p 9042:9042 -d cassandra:latest
sleep 70s
docker run -it --network dulher-cassandra-network --rm ddl_image
. ./write_dataset.sh
docker run --name cassandra-flask --network dulher-cassandra-network -p 8080:8080 -d cassandra_api
