CREATE  KEYSPACE amazon_dulher WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE amazon_dulher;

CREATE TABLE product_reviews_text (product_id text, review_id text, review_headline text, review_body text, star_rating int, PRIMARY KEY (product_id, star_rating, review_id));

CREATE TABLE product_reviews_date (product_id text, review_id text, review_date date, PRIMARY KEY (review_date, review_id));

CREATE TABLE customer_reviews_text (customer_id text, review_id text, review_headline text, review_body text, PRIMARY KEY (customer_id, review_id));

CREATE TABLE customer_reviews_rating (customer_id text, review_id text, review_date date, star_rating int, verified_purchase boolean, PRIMARY KEY (review_date, star_rating, review_id));
