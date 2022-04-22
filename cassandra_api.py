import datetime

from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
from flask import jsonify, request, Flask


class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)
        self.session.row_factory = named_tuple_factory

    def execute(self, query):
        self.session.execute(query)

    def close(self):
        self.session.shutdown()

    def query1(self, product_id):
        """
        Return all reviews for specified product_id
        :param product_id: string
        :return: Rows
        """
        query = "SELECT review_headline, review_body FROM product_reviews_text WHERE product_id='%s'" % product_id
        rows = self.session.execute(query)
        return rows

    def query2(self, product_id, star_rating):
        """
        Return all reviews for specified product_id with given star_rating
        :param product_id: string
        :param star_rating: int
        :return: Rows
        """
        query = "SELECT review_headline, review_body FROM product_reviews_text WHERE product_id='%s' AND " \
                "star_rating=%d" % (product_id, star_rating)
        rows = self.session.execute(query)
        return rows

    def query3(self, customer_id):
        """
        Return all reviews for specified customer_id
        :param customer_id: string
        :return: Rows
        """
        query = "SELECT review_headline, review_body FROM customer_reviews_text WHERE customer_id='%s'" % customer_id
        rows = self.session.execute(query)
        return rows

    def query4(self, start_date, end_date):
        """
        Return N most reviewed items (by # of reviews) for a given period of time
        :param start_date: date in string
        :param end_date: date in string
        :return: Rows
        """
        query = "SELECT product_id, review_id FROM product_reviews_date WHERE review_date >= '%s' AND" \
                " review_date <= '%s' ALLOW FILTERING" % (start_date, end_date)
        rows = self.session.execute(query)
        return rows

    def query5(self, start_date, end_date):
        """
        Return N most productive customers (by # of reviews written for verified purchases) for a given period
        :param start_date: date in string
        :param end_date: date in string
        :return: Rows
        """
        query = "SELECT customer_id, review_id, verified_purchase FROM customer_reviews_rating" \
                " WHERE review_date >= '%s' AND review_date <= '%s' ALLOW FILTERING" % (start_date, end_date)
        rows = self.session.execute(query)
        return rows

    def query6(self, start_date, end_date):
        """
        Return N most productive “haters” (by # of 1- or 2-star reviews) for a given period
        :param start_date: date in string
        :param end_date: date in string
        :return: Rows
        """
        query = "SELECT customer_id, review_id FROM customer_reviews_rating WHERE " \
                "review_date >= '%s' AND review_date <= '%s' AND star_rating in (1, 2) ALLOW FILTERING"\
                % (start_date, end_date)
        rows = self.session.execute(query)
        return rows

    def query7(self, start_date, end_date):
        """
        Return N most productive “backers” (by # of 4- or 5-star reviews) for a given period
        :param start_date: date in string
        :param end_date: date in string
        :return: Rows
        """
        query = "SELECT customer_id, review_id FROM customer_reviews_rating WHERE " \
                "review_date >= '%s' AND review_date <= '%s' AND star_rating in (4, 5) ALLOW FILTERING"\
                % (start_date, end_date)
        rows = self.session.execute(query)
        return rows


class CassandraAPI:

    def __init__(self, name="CassandraAPI"):
        self.app = Flask(name)
        self.name = name
        self.client = self.create_client()
        self.client.connect()

        @self.app.route('/', methods=['GET'])
        def get_request():
            if request.method == 'GET':
                query_body = request.get_json()
                try:
                    result = self.execute_query(query_body)
                    return jsonify(result)
                except AttributeError as err:
                    return jsonify(err=str(err)), 400

    def run(self, host, port):
        self.app.run(host=host, port=port)

    def __del__(self):
        self.client.close()

    def execute_query(self, query_body):
        if len(query_body.keys()) != 2 or "query_number" not in query_body.keys() or "params" not in query_body.keys():
            raise AttributeError("Wrong body: it should only have fields 'query_number' and 'params'")

        try:
            query_number = int(query_body["query_number"])
        except ValueError:
            raise AttributeError("Wrong query_number: it should be int between 1 and 7")
        if query_number < 0 or query_number > 7:
            raise AttributeError("Wrong query_number: it should be int between 1 and 7")

        params = query_body["params"]
        if 1 <= query_number <= 3:

            if query_number == 1:
                if len(params.keys()) != 1 or "product_id" not in params.keys():
                    raise AttributeError("Wrong params for query %d: it should only have field 'product_id'"
                                         % query_number)
                product_id = params["product_id"]
                rows = self.client.query1(product_id)

            elif query_number == 2:
                if len(params.keys()) != 2 or "product_id" not in params.keys() or "star_rating" not in params.keys():
                    raise AttributeError("Wrong params for query %d: it should only have fields 'product_id' and "
                                         "'star_rating'" % query_number)
                product_id = params["product_id"]
                star_rating = params["star_rating"]
                try:
                    star_rating = int(star_rating)
                except ValueError:
                    raise AttributeError("Wrong params for query %d: field 'star_rating' should be int" % query_number)
                rows = self.client.query2(product_id, star_rating)

            else:
                if len(params.keys()) != 1 or "customer_id" not in params.keys():
                    raise AttributeError(
                        "Wrong params for query %d: it should only have field 'customer_id'" % query_number)
                customer_id = params["customer_id"]
                rows = self.client.query3(customer_id)

            result_json = {"columns_names": ("review_headline", "review_body"),
                           "rows": []}
            for row in rows:
                result_json["rows"].append((row.review_headline, row.review_body))
            return result_json

        else:
            if len(params.keys()) != 3 or "N" not in params.keys() or "start_date" not in params.keys() \
                    or "end_date" not in params.keys():
                raise AttributeError("Wrong params for query %d: it should only have fields 'N', 'start_date' and "
                                     "'end_date'" % query_number)

            start_date = params["start_date"]
            end_date = params["end_date"]
            n = params["N"]

            try:
                datetime.datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise AttributeError("Wrong params for query %d: field 'start_date' should be in format 'yyyy-mm-dd'"
                                     % query_number)
            try:
                datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise AttributeError("Wrong params for query %d: field 'end_date' should be in format 'yyyy-mm-dd'"
                                     % query_number)
            try:
                n = int(n)
            except ValueError:
                raise AttributeError("Wrong params for query %d: field 'N' should be int " % query_number)

            if query_number == 4:
                rows = self.client.query4(start_date, end_date)
                result_json = {"columns_names": "product_id",
                               "rows": []}
                count_products = {}
                for row in rows:
                    p_id = row.product_id
                    count_products[p_id] = count_products.setdefault(p_id, 1) + 1
                count_products = dict(sorted(count_products.items(), key=lambda item: item[1], reverse=True))
                i = 0
                for key in count_products.keys():
                    if i < n:
                        result_json["rows"].append(key)
                        i += 1
                    else:
                        break
                return result_json
            elif query_number == 5:
                rows = self.client.query5(start_date, end_date)
                result_json = {"columns_names": "customer_id",
                               "rows": []}
                count_customers = {}
                for row in rows:
                    if not row.verified_purchase:
                        continue
                    c_id = row.customer_id
                    count_customers[c_id] = count_customers.setdefault(c_id, 1) + 1
                count_customers = dict(sorted(count_customers.items(), key=lambda item: item[1], reverse=True))
                i = 0
                for key in count_customers.keys():
                    if i < n:
                        result_json["rows"].append(key)
                        i += 1
                    else:
                        break
                return result_json
            else:
                if query_number == 6:
                    rows = self.client.query6(start_date, end_date)
                else:
                    rows = self.client.query7(start_date, end_date)
                result_json = {"columns_names": "customer_id",
                               "rows": []}
                count_customers = {}
                for row in rows:
                    c_id = row.customer_id
                    count_customers[c_id] = count_customers.setdefault(c_id, 1) + 1
                count_customers = dict(sorted(count_customers.items(), key=lambda item: item[1], reverse=True))
                i = 0
                for key in count_customers.keys():
                    if i < n:
                        result_json["rows"].append(key)
                        i += 1
                    else:
                        break
                return result_json

    @staticmethod
    def create_client():
        host = 'cassandra-node'
        port = 9042
        keyspace = 'amazon_dulher'

        client = CassandraClient(host, port, keyspace)
        return client


def main():
    app = CassandraAPI()
    app.run("0.0.0.0", 8080)


if __name__ == '__main__':
    main()
