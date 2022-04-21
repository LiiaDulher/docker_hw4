#!/bin/bash

docker build -t ddl_image -f Dockerfile1 .

docker build -t cassandra_api -f Dockerfile2 .
