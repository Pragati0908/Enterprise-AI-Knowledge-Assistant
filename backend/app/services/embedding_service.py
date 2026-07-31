from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(

        "all-MiniLM-L6-v2"

    )

    @classmethod
    def generate_embedding(

        cls,

        text: str

    ):

        embedding = cls.model.encode(

            text,

            convert_to_numpy=True

        )

        return embedding

    @classmethod
    def generate_embeddings(

        cls,

        texts: list

    ):

        embeddings = cls.model.encode(

            texts,

            convert_to_numpy=True

        )

        return embeddings