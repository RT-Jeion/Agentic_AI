import os
from qdrant_client import QdrantClient, models

client = QdrantClient(path="qdrant_db")
library = "memory"

if not client.collection_exists(library):
    client.create_collection(
        collection_name=library,
        vectors_config={
            "dense": models.VectorParams
        }
    )