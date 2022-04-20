#!/bin/bash

docker network create dulher-cassandra-network
docker run --name cassandra-node --network dulher-cassandra-network -d cassandra:latest
sleep 70s
