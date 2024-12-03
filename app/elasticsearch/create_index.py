from elasticsearch import Elasticsearch

BOOKS_INDEX = "books"
BOOKS_INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "genre": {"type": "keyword"},
            "price": {"type": "float"},
            "description": {"type": "text"},
            "stock": {"type": "integer"},
            "rating": {"type": "float"}
        }
    }
}


def create_books_index(es: Elasticsearch):
    """
    Create the 'books' index in Elasticsearch if it doesn't exist.
    """
    try:
        if not es.indices.exists(index=BOOKS_INDEX):
            print(f"Creating index: {BOOKS_INDEX}")
            es.indices.create(index=BOOKS_INDEX, body=BOOKS_INDEX_SETTINGS)
            print(f"Index {BOOKS_INDEX} created.")
        else:
            print(f"Index {BOOKS_INDEX} already exists.")
    except Exception as e:
        print(f"Failed to create index {BOOKS_INDEX}: {e}")


CART_INDEX = "cart"
CART_INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "bookId": {"type": "keyword"},
            "quantity": {"type": "integer"},
            "userId": {"type": "keyword"},
            "totalPrice": {"type": "float"}
        }
    }
}


def create_cart_index(es: Elasticsearch):
    """
    Create the 'cart' index in Elasticsearch if it doesn't exist.
    """
    try:
        if not es.indices.exists(index=CART_INDEX):
            print(f"Creating index: {CART_INDEX}")
            es.indices.create(index=CART_INDEX, body=CART_INDEX_SETTINGS)
            print(f"Index {CART_INDEX} created.")
        else:
            print(f"Index {CART_INDEX} already exists.")
    except Exception as e:
        print(f"Failed to create index {CART_INDEX}: {e}")


ORDERS_INDEX = "orders"
ORDERS_INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "orderId": {"type": "keyword"},
            "userId": {"type": "keyword"},
            "items": {
                "type": "nested",
                "properties": {
                    "bookId": {"type": "keyword"},
                    "quantity": {"type": "integer"}
                }
            },
            "totalPrice": {"type": "float"},
            "status": {"type": "keyword"},
            "placedAt": {"type": "date"}
        }
    }
}


def create_orders_index(es: Elasticsearch):
    """
    Create the 'orders' index in Elasticsearch if it doesn't exist.
    """
    try:
        if not es.indices.exists(index=ORDERS_INDEX):
            print(f"Creating index: {ORDERS_INDEX}")
            es.indices.create(index=ORDERS_INDEX, body=ORDERS_INDEX_SETTINGS)
            print(f"Index {ORDERS_INDEX} created.")
        else:
            print(f"Index {ORDERS_INDEX} already exists.")
    except Exception as e:
        print(f"Failed to create index {ORDERS_INDEX}: {e}")
