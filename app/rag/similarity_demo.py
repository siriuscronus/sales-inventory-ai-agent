from app.rag.embeddings import embed_text


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """
    Calcula la similitud coseno entre dos vectores normalizados.
    """

    return sum(a * b for a, b in zip(vector_a, vector_b))


text_1 = "Política de devolución de materiales"

text_2 = "¿Puedo devolver un producto que compré?"

text_3 = "¿Cuánto inventario tenemos disponible?"


vector_1 = embed_text(text_1)
vector_2 = embed_text(text_2)
vector_3 = embed_text(text_3)


similarity_related = cosine_similarity(vector_1, vector_2)
similarity_different = cosine_similarity(vector_1, vector_3)


print("Texto base:")
print(text_1)

print("\nTexto relacionado:")
print(text_2)

print(f"\nSimilitud: {similarity_related:.4f}")


print("\nTexto diferente:")
print(text_3)

print(f"\nSimilitud: {similarity_different:.4f}")