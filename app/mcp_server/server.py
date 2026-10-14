from typing import Any

from mcp.server.mcpserver import MCPServer

from app.rag.retrieval import (
    search_knowledge as rag_search_knowledge,
)
from app.tools.inventory import (
    check_inventory as inventory_check,
    get_low_stock_items as inventory_low_stock,
)
from app.tools.pricing import (
    get_product_price as pricing_get_product_price,
)
from app.tools.product_search import (
    search_product as product_search,
)
from app.tools.quotes import (
    calculate_quote as quote_calculate,
)


# =========================================================
# MCP SERVER
# =========================================================

mcp = MCPServer(
    "Piedmont Metals Sales & Inventory MCP"
)


# =========================================================
# MCP TOOL: INVENTARIO
# =========================================================

@mcp.tool(structured_output=True)
def check_inventory(
    sku: str,
) -> dict[str, Any]:
    """
    Consulta el inventario disponible de un producto
    utilizando su SKU.
    """

    return inventory_check(
        sku
    )


# =========================================================
# MCP TOOL: BAJO INVENTARIO
# =========================================================

@mcp.tool(structured_output=True)
def get_low_stock_items() -> dict[str, Any]:
    """
    Devuelve los productos cuyo inventario está
    por debajo del nivel mínimo configurado.
    """

    return inventory_low_stock()


# =========================================================
# MCP TOOL: PRECIO
# =========================================================

@mcp.tool(structured_output=True)
def get_product_price(
    sku: str,
) -> dict[str, Any]:
    """
    Consulta el precio unitario actual de un producto
    mediante su SKU.
    """

    return pricing_get_product_price(
        sku
    )


# =========================================================
# MCP TOOL: BÚSQUEDA DE PRODUCTOS
# =========================================================

@mcp.tool(structured_output=True)
def search_product(
    query: str,
) -> dict[str, Any]:
    """
    Busca productos por nombre, SKU, categoría,
    dimensiones o descripción.
    """

    return product_search(
        query
    )


# =========================================================
# MCP TOOL: COTIZACIÓN
# =========================================================

@mcp.tool(structured_output=True)
def calculate_quote(
    sku: str,
    quantity: int,
) -> dict[str, Any]:
    """
    Calcula una cotización utilizando precio,
    cantidad solicitada e inventario disponible.
    """

    return quote_calculate(
        sku=sku,
        quantity=quantity,
    )


# =========================================================
# MCP TOOL: RAG / KNOWLEDGE BASE
# =========================================================

@mcp.tool(structured_output=True)
def search_knowledge(
    query: str,
    top_k: int = 3,
    min_score: float = 0.35,
) -> dict[str, Any]:
    """
    Consulta políticas y procedimientos de la
    base de conocimiento mediante RAG y Qdrant.
    """

    return rag_search_knowledge(
        query=query,
        top_k=top_k,
        min_score=min_score,
    )


# =========================================================
# EJECUCIÓN DEL MCP SERVER
# =========================================================

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8001,
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
    )