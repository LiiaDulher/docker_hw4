import csv
import gzip

from cassandra.cluster import Cluster


class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)

    def execute(self, query):
        self.session.execute(query)

    def close(self):
        self.session.shutdown()

    def write_data(self, product_id, review_id, review_headline, review_body, star_rating, review_date, customer_id,
                   verified_purchase):
        query1 = "INSERT INTO product_reviews_text (product_id, review_id, review_headline, review_body, star_rating)" \
                 " VALUES ('%s', '%s', '%s', '%s', %d)" % (product_id, review_id, review_headline, review_body,
                                                           star_rating)
        query2 = "INSERT INTO product_reviews_date (product_id, review_id, review_date)" \
                 " VALUES ('%s', '%s', '%s')" % (product_id, review_id, review_date)
        query3 = "INSERT INTO customer_reviews_text (customer_id, review_id, review_headline, review_body)" \
                 " VALUES ('%s', '%s', '%s', '%s')" % (customer_id, review_id, review_headline, review_body)
        query4 = "INSERT INTO customer_reviews_rating (customer_id, review_id, review_date, star_rating, " \
                 "verified_purchase) VALUES ('%s', '%s', '%s', %d, %r)" % (customer_id, review_id, review_date,
                                                                           star_rating, verified_purchase)
        self.execute(query1)
        self.execute(query2)
        self.execute(query3)
        self.execute(query4)


def write_dataset(client):
    lines_in_file = 3105372
    lines_number = lines_in_file // 5
    # TODO: check work
    dataset_file = 'amazon_reviews_us_Books_v1_02.tsv.gz'
    count = 0
    with gzip.open(dataset_file, 'rt') as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            if count == lines_number:
                break
            marketplace, customer_id, review_id, product_id, product_parent, product_title, product_category, \
            star_rating, helpful_votes, total_votes, vine, verified_purchase, review_headline, review_body, \
            review_date = line
            if marketplace == 'marketplace':
                continue
            verified_purchase = verified_purchase == 'Y'
            star_rating = int(star_rating)
            review_headline = review_headline.replace("'", "''")
            review_body = review_body.replace("'", "''")
            client.write_data(product_id, review_id, review_headline, review_body, star_rating, review_date,
                              customer_id, verified_purchase)
            count += 1


def main():
    host = 'localhost'
    port = 9042
    keyspace = 'amazon_dulher'
    client = CassandraClient(host, port, keyspace)
    client.connect()
    write_dataset(client)
    client.close()


if __name__ == "__main__":
    main()
