from app.database.db import get_connection


def check_inventory(sku: str) -> dict:
    """
    Consulta el inventario disponible de un producto utilizando su SKU.

    Args:
        sku: Código SKU del producto.

    Returns:
        Diccionario con información del producto e inventario.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            sku,
            name,
            stock_qty,
            min_stock
        FROM products
        WHERE sku = ?
        """,
        (sku,),
    )

    product = cursor.fetchone()

    connection.close()

    if product is None:
        return {
            "found": False,
            "message": f"No se encontró el producto con SKU {sku}.",
        }

    return {
        "found": True,
        "sku": product["sku"],
        "name": product["name"],
        "stock_qty": product["stock_qty"],
        "min_stock": product["min_stock"],
        "low_stock": product["stock_qty"] < product["min_stock"],
    }