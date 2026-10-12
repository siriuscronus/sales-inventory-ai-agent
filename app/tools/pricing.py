from app.database.db import get_connection


def get_product_price(sku: str) -> dict:
    """
    Consulta el precio unitario de un producto mediante su SKU.

    Args:
        sku: Código SKU del producto.

    Returns:
        Diccionario con el precio y datos básicos del producto.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            sku,
            name,
            unit,
            unit_price
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
        "unit": product["unit"],
        "unit_price": product["unit_price"],
    }