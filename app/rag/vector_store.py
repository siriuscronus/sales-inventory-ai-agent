from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.rag.chunking import build_chunks
from app.rag.embeddings import embed_texts


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

QDRANT_PATH = PROJECT_ROOT / "data" / "qdrant"

COLLECTION_NAME = "piedmont_knowledge"


# ---------------------------------------------------------
# Cliente Qdrant local
# ---------------------------------------------------------

def get_qdrant_client() -> QdrantClient:
    """
    Crea un cliente Qdrant utilizando almacenamiento local.
    """

    QDRANT_PATH.mkdir(parents=True, exist_ok=True)

    return QdrantClient(path=str(QDRANT_PATH))


# ---------------------------------------------------------
# Indexar base de conocimiento
# ---------------------------------------------------------

def index_knowledge_base():
    """
    Convierte los chunks en embeddings y los almacena
    dentro de Qdrant.
    """

    client = get_qdrant_client()

    chunks = build_chunks()

    texts = [chunk["text"] for chunk in chunks]

    print(f"Chunks a indexar: {len(chunks)}")
    print("Generando embeddings...")

    vectors = embed_texts(texts)

    if not vectors:
        raise ValueError("No se generaron embeddings.")

    vector_size = len(vectors[0])

    print(f"Dimensión de embeddings: {vector_size}")

    # Reconstruimos la colección para mantener el índice limpio.
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )

    points = []

    for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
        points.append(
            PointStruct(
                id=index,
                vector=vector,
                payload={
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True,
    )

    print(f"Puntos almacenados en Qdrant: {len(points)}")
    print(f"Colección creada: {COLLECTION_NAME}")


if __name__ == "__main__":
    index_knowledge_base()