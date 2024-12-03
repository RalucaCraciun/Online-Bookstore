from elasticsearch import Elasticsearch
import os
from app.elasticsearch.create_index import create_books_index, create_orders_index, create_cart_index

# Global Elasticsearch client
es_client: Elasticsearch = None


def connect_to_elastic():
    """
    Connect to Elasticsearch and ensure the 'books' index is created.
    """
    try:
        es_host = os.getenv("ES_HOST", "http://localhost:9200")
        print(f"Connecting to Elasticsearch at {es_host}")
        es = Elasticsearch(hosts=[es_host])

        if es.ping():
            print("Elasticsearch connection successful.")
            create_books_index(es)
            create_cart_index(es)
            create_orders_index(es)

            return es, True
        else:
            raise RuntimeError("Elasticsearch is not responding.")
    except Exception as e:
        print(f"Failed to connect to Elasticsearch: {e}")
        return None, False


# Initialize the Elasticsearch connection
es_connect = connect_to_elastic()
