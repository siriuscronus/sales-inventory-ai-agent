from app.tools.inventory import check_inventory
from app.tools.pricing import get_product_price


def calculate_quote(sku: str, quantity: int) -> dict:
    """
    Calcula una cotización básica para un producto.

    Args:
        sku: Código SKU del producto.
        quantity: Cantidad solicitada.

    Returns:
        Diccionario con disponibilidad, precio y subtotal.
    """

    if quantity <= 0:
        return {
            "success": False,
            "message": "La cantidad debe ser mayor que cero.",
        }

    inventory = check_inventory(sku)

    if not inventory["found"]:
        return {
            "success": False,
            "message": inventory["message"],
        }

    pricing = get_product_price(sku)

    if not pricing["found"]:
        return {
            "success": False,
            "message": pricing["message"],
        }

    available_quantity = inventory["stock_qty"]
    unit_price = pricing["unit_price"]

    sufficient_stock = available_quantity >= quantity
    shortage = max(quantity - available_quantity, 0)

    subtotal_requested = round(quantity * unit_price, 2)

    fulfillable_quantity = min(quantity, available_quantity)
    subtotal_available = round(fulfillable_quantity * unit_price, 2)

    return {
        "success": True,
        "sku": sku,
        "name": inventory["name"],
        "quantity_requested": quantity,
        "quantity_available": available_quantity,
        "sufficient_stock": sufficient_stock,
        "shortage": shortage,
        "unit_price": unit_price,
        "subtotal_requested": subtotal_requested,
        "fulfillable_quantity": fulfillable_quantity,
        "subtotal_available": subtotal_available,
    }