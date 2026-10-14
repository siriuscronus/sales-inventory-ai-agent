from app.tools.inventory import (
    check_inventory,
    get_low_stock_items,
)
from app.tools.pricing import get_product_price
from app.tools.product_search import search_product
from app.tools.quotes import calculate_quote


def test_inventory_known_product():
    result = check_inventory("IJOIST-16-20")

    assert result["found"] is True
    assert result["stock_qty"] == 14
    assert result["min_stock"] == 10
    assert result["low_stock"] is False


def test_inventory_unknown_product():
    result = check_inventory("SKU-NO-EXISTE")

    assert result["found"] is False


def test_low_stock_items():
    result = get_low_stock_items()

    skus = {
        item["sku"]
        for item in result["items"]
    }

    assert result["count"] == 2
    assert "IJOIST-16-28" in skus
    assert "LVL-175-16-12" in skus


def test_product_price():
    result = get_product_price("OSB-2332-4X8")

    assert result["found"] is True
    assert result["unit_price"] == 33.95


def test_quote_with_insufficient_inventory():
    result = calculate_quote(
        "IJOIST-16-20",
        20,
    )

    assert result["success"] is True
    assert result["quantity_requested"] == 20
    assert result["quantity_available"] == 14
    assert result["sufficient_stock"] is False
    assert result["shortage"] == 6
    assert result["subtotal_available"] == 595.0


def test_product_search():
    result = search_product(
        "I-Joist 20"
    )

    assert result["count"] == 1
    assert result["items"][0]["sku"] == "IJOIST-16-20"
