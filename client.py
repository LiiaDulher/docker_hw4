import requests


class Client:
    def __init__(self, url):
        self.url = url
        self.queries = {
            1: [
                {
                    "name": "product_id",
                    "help_string": "string with id"
                }
            ],
            2: [
                {
                    "name": "product_id",
                    "help_string": "string with id"
                },
                {
                    "name": "star_rating",
                    "help_string": "int between 1 and 5"
                }
            ],
            3: [
                {
                    "name": "customer_id",
                    "help_string": "string with id"
                }
            ],
            4: [
                {
                    "name": "N",
                    "help_string": "int: number of products"
                },
                {
                    "name": "start_date",
                    "help_string": "date in format yyyy-mm-dd"
                },
                {
                    "name": "end_date",
                    "help_string": "date in format yyyy-mm-dd"
                }
            ],
            5: [
                {
                    "name": "N",
                    "help_string": "int: number of customers"
                },
                {
                    "name": "start_date",
                    "help_string": "date in format yyyy-mm-dd"
                },
                {
                    "name": "end_date",
                    "help_string": "date in format yyyy-mm-dd"
                }
            ],
            6: [
                {
                    "name": "N",
                    "help_string": "int: number of customers"
                },
                {
                    "name": "start_date",
                    "help_string": "date in format yyyy-mm-dd"
                },
                {
                    "name": "end_date",
                    "help_string": "date in format yyyy-mm-dd"
                }
            ],
            7: [
                {
                    "name": "N",
                    "help_string": "int: number of customers"
                },
                {
                    "name": "start_date",
                    "help_string": "date in format yyyy-mm-dd"
                },
                {
                    "name": "end_date",
                    "help_string": "date in format yyyy-mm-dd"
                }
            ]
        }

    def get_request(self):
        query_number = int(input("1: Return all reviews for specified *`product_id`* \n"
                                 "2: Return all reviews for specified *`product_id`* with given *`star_rating`* \n"
                                 "3: Return all reviews for specified *`customer_id`*\n"
                                 "4 :Return N most reviewed items (by # of reviews) for a given period of time\n"
                                 "5: Return N most productive customers (by # of reviews written for verified "
                                 "purchases) for a given period\n"
                                 "6: Return N most productive “haters” (by # of 1- or 2-star reviews)"
                                 " for a given period\n"
                                 "7: Return N most productive “backers” (by # of 4- or 5-star reviews) for a given"
                                 " period)\n"
                                 "0: exit\n"))
        query_body = {
            "query_number": 0,
            "params": {}
        }
        if query_number == 0:
            return None
        if 0 < query_number < 8:
            query_body["query_number"] = query_number
            for param in self.queries[query_number]:
                p = input("Enter %s (%s):" % (param["name"], param["help_string"]))
                query_body["params"][param["name"]] = p
            return query_body

        raise AttributeError("Wrong query number")

    def send_query(self, query_body):
        try:
            response = requests.get(self.url, json=query_body)
        except requests.exceptions.RequestException as err:
            return 0, err
        return response.status_code, response.json()


def main():
    host = 'http://localhost'
    port = 8080
    url = host + ":" + str(port)
    client = Client(url)
    while True:
        try:
            query_body = client.get_request()
        except AttributeError as err:
            print(err)
            continue
        if query_body is None:
            break
        else:
            code, json = client.send_query(query_body)
            print("Code: %d\n" % code, json)


if __name__ == "__main__":
    main()
