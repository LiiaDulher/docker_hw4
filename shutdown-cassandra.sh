#!/bin/bash

docker stop cassandra-node
docker stop cassandra_api
docker rm cassandra-node
docker rm cassandra_api
docker network rm dulher-cassandra-network
