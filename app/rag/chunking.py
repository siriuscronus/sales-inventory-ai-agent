from pathlib import Path


# ---------------------------------------------------------
# Rutas del proyecto
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "knowledge_base"


# ---------------------------------------------------------
# Cargar documentos
# ---------------------------------------------------------

def load_documents() -> list[dict]:
    """
    Carga todos los archivos Markdown de la base de conocimiento.

    Returns:
        Lista de documentos con nombre de archivo y contenido.
    """

    documents = []

    for file_path in sorted(KNOWLEDGE_BASE_PATH.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "text": text,
            }
        )

    return documents


# ---------------------------------------------------------
# Dividir texto en chunks
# ---------------------------------------------------------

def chunk_text(
    text: str,
    max_chars: int = 800,
    overlap_paragraphs: int = 1,
) -> list[str]:
    """
    Divide un documento en fragmentos utilizando párrafos.

    Args:
        text: Contenido completo del documento.
        max_chars: Tamaño aproximado máximo de cada chunk.
        overlap_paragraphs: Número de párrafos que se repetirán
                            entre chunks consecutivos.

    Returns:
        Lista de chunks.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_paragraphs = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)

        if (
            current_paragraphs
            and current_length + paragraph_length > max_chars
        ):
            chunk = "\n\n".join(current_paragraphs)
            chunks.append(chunk)

            if overlap_paragraphs > 0:
                current_paragraphs = current_paragraphs[-overlap_paragraphs:]
                current_length = sum(
                    len(item) for item in current_paragraphs
                )
            else:
                current_paragraphs = []
                current_length = 0

        current_paragraphs.append(paragraph)
        current_length += paragraph_length

    if current_paragraphs:
        chunks.append("\n\n".join(current_paragraphs))

    return chunks


# ---------------------------------------------------------
# Procesar todos los documentos
# ---------------------------------------------------------

def build_chunks() -> list[dict]:
    """
    Carga todos los documentos y crea chunks con metadata.
    """

    documents = load_documents()

    all_chunks = []

    for document in documents:
        chunks = chunk_text(document["text"])

        for index, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "source": document["source"],
                    "chunk_id": index,
                    "text": chunk,
                }
            )

    return all_chunks


# ---------------------------------------------------------
# Prueba local
# ---------------------------------------------------------

if __name__ == "__main__":
    documents = load_documents()
    chunks = build_chunks()

    print(f"Documentos cargados: {len(documents)}")
    print(f"Chunks generados: {len(chunks)}")

    print("\n--- Ejemplo de chunk ---\n")

    if chunks:
        print(f"Fuente: {chunks[0]['source']}")
        print(f"Chunk ID: {chunks[0]['chunk_id']}")
        print()
        print(chunks[0]["text"])