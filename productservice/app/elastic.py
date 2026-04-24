import os
from pathlib import Path

from elasticsearch import Elasticsearch
import elasticsearch
import elastic_transport

print("ELASTICSEARCH VERSION:", elasticsearch.__version__)
print("TRANSPORT VERSION:", elastic_transport.__version__)


def load_local_env():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def build_client():
    load_local_env()
    hosts = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    username = os.getenv("ELASTICSEARCH_USERNAME")
    password = os.getenv("ELASTICSEARCH_PASSWORD")
    ca_certs = os.getenv("ELASTICSEARCH_CA_CERT")
    verify_certs = os.getenv("ELASTICSEARCH_VERIFY_CERTS", "true").lower() == "true"

    client_kwargs = {"hosts": hosts, "verify_certs": verify_certs}

    if username and password:
        client_kwargs["basic_auth"] = (username, password)

    if ca_certs:
        client_kwargs["ca_certs"] = ca_certs

    return Elasticsearch(**client_kwargs)


es = build_client()


def create_index():
    if not es.indices.exists(index="products"):
        es.indices.create(index="products")
