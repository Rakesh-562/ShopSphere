from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def create_index():
    if not es.indices.exists(index="products"):
        es.indices.create(index="products")