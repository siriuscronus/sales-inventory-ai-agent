from google.genai import errors, types

from app.agent.llm import MODELS, get_gemini_client
from app.rag.retrieval import search_knowledge
from app.tools.inventory import (
    check_inventory,
    get_low_stock_items,
)
from app.tools.pricing import get_product_price
from app.tools.product_search import search_product
from app.tools.quotes import calculate_quote


# ---------------------------------------------------------
# Tools instrumentadas
# ---------------------------------------------------------

def tool_check_inventory(sku: str) -> dict:
    """Consulta el inventario disponible para un SKU."""
    print(f"\n[TOOL CALL] check_inventory(sku={sku})")
    return check_inventory(sku)


def tool_get_low_stock_items() -> dict:
    """Obtiene los productos cuyo inventario está por debajo del mínimo."""
    print("\n[TOOL CALL] get_low_stock_items()")
    return get_low_stock_items()


def tool_get_product_price(sku: str) -> dict:
    """Consulta el precio actual de un producto utilizando su SKU."""
    print(f"\n[TOOL CALL] get_product_price(sku={sku})")
    return get_product_price(sku)


def tool_search_product(query: str) -> dict:
    """Busca productos utilizando nombre, categoría, dimensiones o descripción."""
    print(f"\n[TOOL CALL] search_product(query={query})")
    return search_product(query)


def tool_calculate_quote(sku: str, quantity: int) -> dict:
    """Calcula una cotización considerando precio e inventario disponible."""
    print(
        f"\n[TOOL CALL] calculate_quote("
        f"sku={sku}, quantity={quantity})"
    )
    return calculate_quote(
        sku=sku,
        quantity=quantity,
    )


def tool_search_knowledge(
    query: str,
    top_k: int = 3,
    min_score: float = 0.35,
) -> dict:
    """
    Busca políticas, procedimientos y conocimiento documental
    mediante RAG.
    """
    print(
        f"\n[TOOL CALL] search_knowledge("
        f"query={query}, top_k={top_k}, min_score={min_score})"
    )

    return search_knowledge(
        query=query,
        top_k=top_k,
        min_score=min_score,
    )


TOOLS = [
    tool_check_inventory,
    tool_get_low_stock_items,
    tool_get_product_price,
    tool_search_product,
    tool_calculate_quote,
    tool_search_knowledge,
]

# ---------------------------------------------------------
# Agente con Automatic Function Calling
# ---------------------------------------------------------

def run_tool_calling_agent(query: str) -> dict:
    """
    Ejecuta un agente en el que Gemini decide
    qué herramientas necesita utilizar.

    El SDK de Google administra automáticamente:
    1. Selección de funciones.
    2. Ejecución de funciones Python.
    3. Envío del resultado al modelo.
    4. Generación de la respuesta final.
    """

    query = query.strip()

    if not query:
        return {
            "success": False,
            "answer": "",
            "model": None,
            "error": "La consulta no puede estar vacía.",
        }

    client = get_gemini_client()

    system_instruction = """
Eres un Sales & Inventory AI Agent para un prototipo académico.

Tienes acceso a herramientas para:

- consultar inventario;
- consultar precios;
- preparar cotizaciones;
- buscar productos;
- detectar productos con bajo inventario;
- consultar políticas y procedimientos mediante RAG.

Debes utilizar las herramientas cuando necesites información
operativa o conocimiento documental.

No inventes inventario, precios, cantidades, políticas
ni procedimientos.

Si una consulta necesita información de varias fuentes,
utiliza varias herramientas cuando sea necesario.

Responde siempre en español de forma profesional,
clara y concisa.
"""

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=TOOLS,
    )

    last_error = None

    for model_name in MODELS:
        try:
            print(f"\nIntentando modelo: {model_name}")

            # Creamos una sesión de chat específica para este modelo.
            chat = client.chats.create(
                model=model_name,
                config=config,
            )

            # El SDK puede ejecutar automáticamente las tools.
            response = chat.send_message(query)

            return {
                "success": True,
                "answer": response.text or "",
                "model": model_name,
                "error": None,
            }

        except errors.ServerError as exc:
            last_error = exc

            print(
                f"{model_name} no está disponible. "
                "Probando siguiente modelo..."
            )

    return {
        "success": False,
        "answer": "",
        "model": None,
        "error": (
            "Los modelos Gemini están temporalmente "
            "no disponibles."
        ),
        "details": str(last_error),
    }


# ---------------------------------------------------------
# Prueba local
# ---------------------------------------------------------

if __name__ == "__main__":
    question = (
        "Necesito 20 unidades del SKU IJOIST-16-20. "
        "¿Tenemos suficiente inventario y qué procedimiento "
        "seguimos si no alcanza?"
    )

    result = run_tool_calling_agent(question)

    print("\n" + "=" * 70)
    print("CONSULTA")
    print("=" * 70)
    print(question)

    print("\n" + "=" * 70)
    print("RESPUESTA DEL AGENTE")
    print("=" * 70)

    if result["success"]:
        print(result["answer"])
        print(f"\nModelo utilizado: {result['model']}")
    else:
        print(result["error"])