import re


# ---------------------------------------------------------
# Límites operativos del MVP
# ---------------------------------------------------------

MAX_QUOTE_QUANTITY = 10000
MAX_SEARCH_LENGTH = 200
MAX_TOP_K = 10

SKU_PATTERN = re.compile(
    r"^[A-Z0-9]+(?:-[A-Z0-9.]+)+$"
)


# ---------------------------------------------------------
# Validación de SKU
# ---------------------------------------------------------

def validate_sku(sku: str) -> dict:
    """
    Valida que el SKU tenga un formato permitido.
    """

    if not isinstance(sku, str):
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "El SKU debe ser una cadena de texto."
            ],
        }

    cleaned_sku = sku.strip().upper()

    if not cleaned_sku:
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "El SKU no puede estar vacío."
            ],
        }

    if len(cleaned_sku) > 50:
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "El SKU supera la longitud permitida."
            ],
        }

    if not SKU_PATTERN.fullmatch(cleaned_sku):
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "El formato del SKU no es válido."
            ],
        }

    return {
        "allowed": True,
        "value": cleaned_sku,
        "issues": [],
    }


# ---------------------------------------------------------
# Validación de cantidad
# ---------------------------------------------------------

def validate_quantity(quantity: int) -> dict:
    """
    Valida cantidades utilizadas en cotizaciones.
    """

    if isinstance(quantity, bool) or not isinstance(
        quantity,
        int,
    ):
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "La cantidad debe ser un número entero."
            ],
        }

    if quantity <= 0:
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "La cantidad debe ser mayor que cero."
            ],
        }

    if quantity > MAX_QUOTE_QUANTITY:
        return {
            "allowed": False,
            "value": None,
            "issues": [
                (
                    "La cantidad supera el límite "
                    f"operativo de {MAX_QUOTE_QUANTITY}."
                )
            ],
        }

    return {
        "allowed": True,
        "value": quantity,
        "issues": [],
    }


# ---------------------------------------------------------
# Validación de búsquedas
# ---------------------------------------------------------

def validate_search_query(query: str) -> dict:
    """
    Valida consultas enviadas a búsqueda de productos
    o recuperación documental.
    """

    if not isinstance(query, str):
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "La búsqueda debe ser texto."
            ],
        }

    cleaned_query = query.strip()

    if not cleaned_query:
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "La búsqueda no puede estar vacía."
            ],
        }

    if len(cleaned_query) > MAX_SEARCH_LENGTH:
        return {
            "allowed": False,
            "value": None,
            "issues": [
                (
                    "La búsqueda supera el límite de "
                    f"{MAX_SEARCH_LENGTH} caracteres."
                )
            ],
        }

    return {
        "allowed": True,
        "value": cleaned_query,
        "issues": [],
    }


# ---------------------------------------------------------
# Validación de parámetros RAG
# ---------------------------------------------------------

def validate_top_k(top_k: int) -> dict:
    """
    Limita el número de fragmentos recuperados.
    """

    if isinstance(top_k, bool) or not isinstance(
        top_k,
        int,
    ):
        return {
            "allowed": False,
            "value": None,
            "issues": [
                "top_k debe ser un número entero."
            ],
        }

    if top_k < 1 or top_k > MAX_TOP_K:
        return {
            "allowed": False,
            "value": None,
            "issues": [
                (
                    "top_k debe estar entre "
                    f"1 y {MAX_TOP_K}."
                )
            ],
        }

    return {
        "allowed": True,
        "value": top_k,
        "issues": [],
    }


# ---------------------------------------------------------
# Pruebas locales
# ---------------------------------------------------------

if __name__ == "__main__":
    tests = [
        ("SKU válido", validate_sku("IJOIST-16-20")),
        ("SKU inválido", validate_sku("../../etc/passwd")),
        ("Cantidad válida", validate_quantity(20)),
        ("Cantidad negativa", validate_quantity(-10)),
        (
            "Cantidad excesiva",
            validate_quantity(999999999),
        ),
        (
            "top_k válido",
            validate_top_k(3),
        ),
        (
            "top_k excesivo",
            validate_top_k(10000),
        ),
    ]

    for name, result in tests:
        print("\n" + "=" * 60)
        print(name)
        print(result)