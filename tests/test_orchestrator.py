from app.agent.orchestrator import run_agent


def test_greeting_uses_local_router():
    result = run_agent("Hola")

    assert result["success"] is True
    assert result["intent"] == "greeting"
    assert result["model"] == "local-conversation-router"


def test_price_uses_operational_router():
    result = run_agent(
        "¿Cuánto cuesta el SKU IJOIST-16-20?"
    )

    assert result["success"] is True
    assert result["intent"] == "price"
    assert result["model"] == "local-operational-router"
    assert "$42.50" in result["answer"]


def test_inventory_uses_operational_router():
    result = run_agent(
        "¿Cuántas unidades tenemos del SKU IJOIST-16-20?"
    )

    assert result["success"] is True
    assert result["intent"] == "inventory"
    assert result["model"] == "local-operational-router"
    assert "14 unidades" in result["answer"]


def test_out_of_scope_query():
    result = run_agent(
        "Escribe un código Python para sumar dos números"
    )

    assert result["success"] is True
    assert result["intent"] == "out_of_scope"
    assert result["model"] == "local-scope-router"
