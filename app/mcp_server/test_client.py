import anyio

from mcp import Client


async def main():
    async with Client(
        "http://127.0.0.1:8001/mcp"
    ) as client:

        # =================================================
        # 1. LISTAR TOOLS
        # =================================================

        tools = await client.list_tools()

        print("\nTOOLS MCP DISPONIBLES")
        print("=" * 60)

        for tool in tools.tools:
            print(f"- {tool.name}")

        # =================================================
        # 2. CONSULTAR INVENTARIO
        # =================================================

        print("\nPRUEBA MCP - INVENTARIO")
        print("=" * 60)

        inventory_result = await client.call_tool(
            "check_inventory",
            {
                "sku": "IJOIST-16-20"
            },
        )

        print(inventory_result.structured_content)

        # =================================================
        # 3. CONSULTAR PRECIO
        # =================================================

        print("\nPRUEBA MCP - PRECIO")
        print("=" * 60)

        price_result = await client.call_tool(
            "get_product_price",
            {
                "sku": "IJOIST-16-20"
            },
        )

        print(price_result.structured_content)

        # =================================================
        # 4. CONSULTAR RAG
        # =================================================

        print("\nPRUEBA MCP - RAG")
        print("=" * 60)

        rag_result = await client.call_tool(
            "search_knowledge",
            {
                "query": (
                    "¿Qué hacemos si no hay "
                    "suficiente inventario?"
                )
            },
        )

        print(rag_result.structured_content)


if __name__ == "__main__":
    anyio.run(main)
