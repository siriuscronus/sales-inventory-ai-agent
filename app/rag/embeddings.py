from functools import lru_cache

from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Modelo de embeddings
# ---------------------------------------------------------

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Carga el modelo de embeddings.

    El modelo se mantiene en memoria para evitar cargarlo
    nuevamente cada vez que generamos un vector.
    """

    return SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    """
    Convierte un texto en un vector numérico.

    Args:
        text: Texto que se desea representar.

    Returns:
        Vector de embeddings como lista de números.
    """

    model = get_embedding_model()

    vector = model.encode(
        text,
        normalize_embeddings=True,
    )

    return vector.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convierte varios textos en embeddings.

    Args:
        texts: Lista de textos.

    Returns:
        Lista de vectores.
    """

    model = get_embedding_model()

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return vectors.tolist()


if __name__ == "__main__":
    sample_text = "Política de devolución de materiales"

    vector = embed_text(sample_text)

    print(f"Modelo: {MODEL_NAME}")
    print(f"Texto: {sample_text}")
    print(f"Dimensiones del vector: {len(vector)}")
    print(f"Primeros 10 valores: {vector[:10]}")