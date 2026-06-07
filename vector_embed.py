import os
from qdrant_client import QdrantClient, models
import pymupdf

client = QdrantClient(path="qdrant_db")
library = "vector_db"

if not client.collection_exists(library):
    client.create_collection(
        collection_name=library,
        dense_vectors_config={
            "dense": models.VectorParams(
                size=384,
                distance=models.Distance.COSINE
            )
        },

        sparse_vectors_config={
            'sparse': models.SparseVectorParams(
                modifier=models.Modifier.IDF
            )
        }
    )

    print(f"Collection{library} created successfully")

    dense_model = "sentence-transformers/all-MiniLM-L6-v2"
    sparse_model = "qdrant/bm25"


    folder_name = "memroy"
    extracted_chunks =[]

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print("Folder not found. Created a folder", folder_name)
        exit()

    for filename in os.listdir(folder_name):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_name, filename)
            print("Extracting", filename)

            doc = pymupdf.open(pdf_path)
            for page


    doc_to_vector = []
    playloads_metadata = []

    for index, chunk in enumerate(extracted_chunks):

        doc_to_vector.append({
            "dense": models.Document(text=chunk['child_text'], model=dense_model),
            "sparse": models.Document(text=chunk['child_text'], model=sparse_model)
        })
        
        playloads_metadata.append({
            "book_title": chunk['book_title'],
            'text_content': chunk['parent_text']
        })

    client.upload_collection(
        collection_name=library,
        vectors=doc_to_vector,
        payload=playloads_metadata,
        ids=list(range(len(extracted_chunks\)))
    )