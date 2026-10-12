from app.database.db import get_connection


def search_product(query: str) -> dict:
    """
    Busca productos utilizando palabras presentes en el SKU,
    nombre, categoría o descripción.

    Args:
        query: Texto de búsqueda introducido por el usuario.

    Returns:
        Diccionario con los productos encontrados.
    """

    query = query.strip()

    if not query:
        return {
            "count": 0,
            "items": [],
            "message": "La búsqueda no puede estar vacía.",
        }

    # Dividir la búsqueda en palabras individuales.
    terms = query.lower().split()

    connection = get_connection()
    cursor = connection.cursor()

    conditions = []
    parameters = []

    for term in terms:
        condition = """
        (
            LOWER(sku) LIKE ?
            OR LOWER(name) LIKE ?
            OR LOWER(category) LIKE ?
            OR LOWER(description) LIKE ?
        )
        """

        conditions.append(condition)

        search_term = f"%{term}%"

        parameters.extend(
            [
                search_term,
                search_term,
                search_term,
                search_term,
            ]
        )

    where_clause = " AND ".join(conditions)

    sql = f"""
        SELECT
            sku,
            name,
            category,
            description,
            unit,
            unit_price,
            stock_qty
        FROM products
        WHERE {where_clause}
        ORDER BY name
        LIMIT 10
    """

    cursor.execute(sql, parameters)

    products = cursor.fetchall()

    connection.close()

    items = []

    for product in products:
        items.append(
            {
                "sku": product["sku"],
                "name": product["name"],
                "category": product["category"],
                "description": product["description"],
                "unit": product["unit"],
                "unit_price": product["unit_price"],
                "stock_qty": product["stock_qty"],
            }
        )

    return {
        "count": len(items),
        "items": items,
    }