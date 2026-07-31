from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


texts = [

    "Artificial Intelligence",

    "Machine Learning",

    "Natural Language Processing",

    "Deep Learning"

]


embeddings = EmbeddingService.generate_embeddings(

    texts

)


dimension = len(

    embeddings[0]

)


store = VectorStore(

    dimension

)


store.add_embeddings(

    embeddings

)


print()

print("=" * 60)
print("VECTOR STORE TEST")
print("=" * 60)

print()

print(

    f"Embedding Dimension : {dimension}"

)

print(

    f"Total Texts : {len(texts)}"

)

print(

    f"Total Stored Vectors : {store.total_vectors()}"

)


store.save(

    "vector_db/faiss.index"

)

print()

print(

    "Index Saved Successfully"

)


new_store = VectorStore(

    dimension

)

new_store.load(

    "vector_db/faiss.index"

)

print(

    "Index Loaded Successfully"

)

print()

print(

    f"Loaded Vectors : {new_store.total_vectors()}"

)