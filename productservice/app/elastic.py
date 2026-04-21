from elasticsearch import Elasticsearch
import elasticsearch
import elastic_transport

print("ELASTICSEARCH VERSION:", elasticsearch.__version__)
print("TRANSPORT VERSION:", elastic_transport.__version__)
es = Elasticsearch("http://localhost:9200")

def create_index():
    if not es.indices.exists(index="products"):
        es.indices.create(index="products")