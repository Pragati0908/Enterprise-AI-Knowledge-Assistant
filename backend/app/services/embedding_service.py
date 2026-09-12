from sentence_transformers import SentenceTransformer


class EmbeddingService:

    _model = None

    @classmethod
    def _get_model(cls):

        if cls._model is None:

            print("Loading SentenceTransformer model...")

            cls._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            print("SentenceTransformer model loaded successfully.")

        return cls._model

    @classmethod
    def generate_embedding(
        cls,
        text: str
    ):

        model = cls._get_model()

        embedding = model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding

    @classmethod
    def generate_embeddings(
        cls,
        texts: list
    ):

        model = cls._get_model()

        embeddings = model.encode(
            texts,
            convert_to_numpy=True
        )

        return embeddings