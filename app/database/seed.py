import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# Rutas del proyecto
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "piedmont_metals.db"


# ---------------------------------------------------------
# Datos ficticios de demostración
# ---------------------------------------------------------

PRODUCTS = [
    (
        "IJOIST-16-20",
        "I-Joist 16 x 20 ft",
        "I-Joist",
        "I-Joist de 16 pulgadas de profundidad y 20 pies de longitud",
        "EA",
        42.50,
        14,
        10,
    ),
    (
        "IJOIST-16-28",
        "I-Joist 16 x 28 ft",
        "I-Joist",
        "I-Joist de 16 pulgadas de profundidad y 28 pies de longitud",
        "EA",
        58.75,
        8,
        10,
    ),
    (
        "LUMBER-2X6-16",
        "Lumber 2x6x16",
        "Lumber",
        "Madera dimensional 2 x 6 x 16 pies",
        "EA",
        15.25,
        42,
        20,
    ),
    (
        "LUMBER-2X12-12",
        "Lumber 2x12x12",
        "Lumber",
        "Madera dimensional 2 x 12 x 12 pies",
        "EA",
        24.90,
        25,
        15,
    ),
    (
        "OSB-2332-4X8",
        "OSB 23/32 4x8",
        "Sheathing",
        "Panel OSB de 23/32 pulgadas de 4 x 8 pies",
        "EA",
        33.95,
        75,
        25,
    ),
    (
        "LVL-175-16-14",
        "LVL 1.75x16x14",
        "LVL",
        "Viga LVL de 1.75 x 16 pulgadas x 14 pies",
        "EA",
        89.50,
        12,
        8,
    ),
    (
        "LVL-175-16-12",
        "LVL 1.75x16x12",
        "LVL",
        "Viga LVL de 1.75 x 16 pulgadas x 12 pies",
        "EA",
        78.25,
        6,
        8,
    ),
    (
        "PANEL-29GA-WHITE",
        "Classic Panel 29GA Bright White",
        "Metal Roofing",
        "Panel metálico calibre 29 color blanco brillante",
        "EA",
        31.75,
        30,
        15,
    ),
    (
        "FLATSHEET-29GA",
        "Flat Sheet 29GA",
        "Metal Roofing",
        "Lámina plana calibre 29",
        "EA",
        27.40,
        18,
        10,
    ),
    (
        "STRAP-25-TWIST",
        "Twist Strap 2.5x2.5",
        "Hardware",
        "Conector estructural tipo twist strap",
        "EA",
        4.85,
        120,
        40,
    ),
]


def seed_database():
    """
    Crea la base SQLite del prototipo e inserta
    productos ficticios de demostración.
    """

    # Garantiza que la carpeta data exista.
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            unit TEXT,
            unit_price REAL NOT NULL,
            stock_qty INTEGER NOT NULL,
            min_stock INTEGER NOT NULL
        )
        """
    )

    # Borra los registros anteriores para que el seed
    # pueda ejecutarse varias veces sin duplicar datos.
    cursor.execute("DELETE FROM products")

    cursor.executemany(
        """
        INSERT INTO products (
            sku,
            name,
            category,
            description,
            unit,
            unit_price,
            stock_qty,
            min_stock
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        PRODUCTS,
    )

    connection.commit()
    connection.close()

    print(f"Base de datos creada correctamente: {DB_PATH}")
    print(f"Productos cargados: {len(PRODUCTS)}")


if __name__ == "__main__":
    seed_database()