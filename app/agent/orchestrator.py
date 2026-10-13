import json
import re

from app.agent.llm import generate_response
from app.rag.retrieval import search_knowledge
from app.tools.inventory import (
    check_inventory,
    get_low_stock_items,
)
from app.tools.pricing import get_product_price
from app.tools.product_search import search_product
from app.tools.quotes import calculate_quote


# ---------------------------------------------------------
# Extracción básica de información
# ---------------------------------------------------------

def extract_sku(query: str) -> str | None:
    """
    Intenta identificar un SKU dentro de la consulta.
    """

    match = re.search(
        r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9.]+)+\b",
        query.upper(),
    )

    if match:
        return match.group(0)

    return None


def extract_quantity(query: str) -> int | None:
    """
    Intenta identificar una cantidad solicitada
    utilizando expresiones comunes.
    """

    patterns = [
        r"\bnecesito\s+(\d+)\b",
        r"\bquiero\s+(\d+)\b",
        r"\bcotiza(?:r)?\s+(\d+)\b",
        r"\b(\d+)\s+(?:unidades|piezas)\b",
    ]

    query_lower = query.lower()

    for pattern in patterns:
        match = re.search(pattern, query_lower)

        if match:
            return int(match.group(1))

    return None


# ---------------------------------------------------------
# Selección de Tools
# ---------------------------------------------------------

def execute_tools(query: str) -> dict:
    """
    Decide qué herramientas operativas ejecutar
    de acuerdo con la consulta.
    """

    query_lower = query.lower()

    sku = extract_sku(query)
    quantity = extract_quantity(query)

    tool_results = {}

    # -----------------------------------------------------
    # Bajo inventario
    # -----------------------------------------------------

    if (
        "bajo inventario" in query_lower
        or "inventario bajo" in query_lower
        or "low stock" in query_lower
    ):
        tool_results["low_stock"] = get_low_stock_items()

    # -----------------------------------------------------
    # Cotización / solicitud con cantidad
    # -----------------------------------------------------

    if sku and quantity:
        tool_results["quote"] = calculate_quote(
            sku=sku,
            quantity=quantity,
        )

    # -----------------------------------------------------
    # Consulta de inventario
    # -----------------------------------------------------

    elif sku and (
        "inventario" in query_lower
        or "stock" in query_lower
        or "disponible" in query_lower
        or "tenemos" in query_lower
    ):
        tool_results["inventory"] = check_inventory(sku)

    # -----------------------------------------------------
    # Consulta de precio
    # -----------------------------------------------------

    if sku and (
        "precio" in query_lower
        or "cuesta" in query_lower
        or "costo" in query_lower
    ):
        tool_results["price"] = get_product_price(sku)

    # -----------------------------------------------------
    # Búsqueda de producto cuando no tenemos SKU
    # -----------------------------------------------------

    if not sku and (
        "producto" in query_lower
        or "buscar" in query_lower
        or "encuentra" in query_lower
    ):
        tool_results["product_search"] = search_product(query)

    return {
        "sku_detected": sku,
        "quantity_detected": quantity,
        "tool_results": tool_results,
    }


# ---------------------------------------------------------
# Construcción de contexto
# ---------------------------------------------------------

def build_agent_context(query: str) -> dict:
    """
    Ejecuta Tools y RAG para construir el contexto
    que recibirá posteriormente el LLM.
    """

    operational_context = execute_tools(query)

    knowledge_context = search_knowledge(
        query=query,
        top_k=3,
        min_score=0.35,
    )

    return {
        "operational": operational_context,
        "knowledge": knowledge_context,
    }


# ---------------------------------------------------------
# Orquestador principal
# ---------------------------------------------------------

def run_agent(query: str) -> dict:
    """
    Procesa una consulta completa utilizando:

    1. Tools
    2. RAG
    3. Gemini
    """

    query = query.strip()

    if not query:
        return {
            "success": False,
            "answer": "",
            "message": "La consulta no puede estar vacía.",
        }

    context = build_agent_context(query)

    context_json = json.dumps(
        context,
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
CONSULTA DEL USUARIO:

{query}


CONTEXTO DISPONIBLE:

{context_json}


INSTRUCCIONES:

Utiliza únicamente la información disponible en el contexto.

Los datos provenientes de Tools representan información
operativa estructurada.

Los datos provenientes de Knowledge representan procedimientos
o políticas recuperadas mediante RAG.

No inventes inventario, precios, políticas ni procedimientos.

Si el contexto no contiene información suficiente para responder
alguna parte de la consulta, indícalo claramente.

Responde de forma profesional, clara y breve.
"""

    llm_result = generate_response(
        prompt=prompt,
        system_instruction=(
            "Eres el Sales & Inventory AI Agent de un prototipo "
            "académico. Debes responder en español utilizando "
            "exclusivamente la información proporcionada por "
            "las herramientas y la base de conocimiento."
        ),
    )

    # -----------------------------------------------------
    # Respuesta normal con LLM
    # -----------------------------------------------------

    if llm_result["success"]:
        return {
            "success": True,
            "answer": llm_result["text"],
            "model": llm_result["model"],
            "context": context,
        }

    # -----------------------------------------------------
    # Degradación controlada si el LLM no está disponible
    # -----------------------------------------------------

    return {
        "success": False,
        "answer": (
            "El modelo de lenguaje no está disponible "
            "temporalmente. Los datos recuperados por Tools "
            "y RAG siguen disponibles."
        ),
        "model": None,
        "context": context,
        "llm_error": llm_result.get("error"),
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

    result = run_agent(question)

    print("\n" + "=" * 70)
    print("CONSULTA")
    print("=" * 70)

    print(question)

    print("\n" + "=" * 70)
    print("RESPUESTA DEL AGENTE")
    print("=" * 70)

    print(result["answer"])

    print("\n" + "=" * 70)
    print("RECURSOS UTILIZADOS")
    print("=" * 70)

    print(
        json.dumps(
            result["context"],
            ensure_ascii=False,
            indent=2,
        )
    )

    if result.get("model"):
        print(f"\nModelo utilizado: {result['model']}")