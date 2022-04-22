# Docker hw4
Cassandra 3

## Team: [Liia_Dulher](https://github.com/LiiaDulher)

### API 
<b>API_description.txt</b> contains description of API.

### Important
It takes about 65 seconds for Cassandra node to start, so <i>run-cassandra.sh</i> will start node about <b>1 minute</b> and then write data into
tables about <b>2 hours</b>(each of 4 tables contains more than 600,000 rows). Then script will start server and tell you, that it is ready to listen.<br>
Put dataset file <b>amazon_reviews_us_Books_v1_02.tsv.gz</b> into one directory with code.

## Prerequiments
````
pip install cassndra-driver
pip install flask
````
If you are using <i>client.py</i>
````
pip install requests
````

### Usage
````
$ sudo chmod +x run-cassandra.sh
$ sudo chmod +x shutdown-cassandra.sh
$ sudo chmod +x build.sh
$ sudo chmod +x write_dataset.sh
````
````
$ ./build.sh
$ ./run-cassandra.sh
$ python3 ./client.py # or any other way to send GET requests to port 8080
$ ./shutdown-cassandra.sh
````
## Results
Example of each query with answer to it are in the file <b>results.txt</b>
