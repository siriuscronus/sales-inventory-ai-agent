from app.rag.embeddings import embed_text
from app.rag.vector_store import (
    COLLECTION_NAME,
    get_qdrant_client,
)


def search_knowledge(
    query: str,
    top_k: int = 3,
    min_score: float = 0.35,
) -> dict:
    """
    Busca los chunks más relacionados semánticamente
    con la consulta del usuario.
    query_vector = embed_text(query)
    Args:
        query: Pregunta o texto de búsqueda.
        top_k: Número máximo de resultados a recuperar.

    Returns:
        Diccionario con la consulta y los resultados encontrados.
    """

    query = query.strip()

    if not query:
        return {
            "query": query,
            "count": 0,
            "results": [],
            "message": "La consulta no puede estar vacía.",
        }

    client = get_qdrant_client()

    try:
        if not client.collection_exists(COLLECTION_NAME):
            return {
                "query": query,
                "count": 0,
                "results": [],
                "message": (
                    "La colección de conocimiento todavía no existe. "
                    "Ejecute primero la indexación."
                ),
            }

        # Convertimos la pregunta a un embedding.
        query_vector = embed_text(query)

        # Buscamos en Qdrant los vectores más similares.
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        )

        results = []

        for point in response.points:
            score = float(point.score)

            if score < min_score:
                continue

            payload = point.payload or {}

            results.append(
                {
                    "score": round(score, 4),
                    "source": payload.get("source"),
                    "chunk_id": payload.get("chunk_id"),
                    "text": payload.get("text"),
                }
            )

        return {
            "query": query,
            "count": len(results),
            "results": results,
        }

    finally:
        client.close()


if __name__ == "__main__":
    question = "¿Puedo devolver un producto que compré?"

    response = search_knowledge(question)

    print(f"\nPregunta: {response['query']}")
    print(f"Resultados encontrados: {response['count']}")

    for index, result in enumerate(response["results"], start=1):
        print("\n" + "=" * 70)
        print(f"Resultado {index}")
        print(f"Score: {result['score']}")
        print(f"Fuente: {result['source']}")
        print(f"Chunk ID: {result['chunk_id']}")
        print()
        print(result["text"])