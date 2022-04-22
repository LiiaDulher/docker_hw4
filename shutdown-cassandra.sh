#!/bin/bash

docker stop cassandra-node
docker stop cassandra-flask
docker rm cassandra-node
docker rm cassandra-flask
docker network rm dulher-cassandra-network
