#!/bin/bash

docker network create dulher-cassandra-network
docker run --name cassandra-node --network dulher-cassandra-network -p 9042:9042 -d cassandra:latest
sleep 70s
