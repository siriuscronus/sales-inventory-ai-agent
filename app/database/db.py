import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "piedmont_metals.db"


def get_connection():
    """
    Crea y devuelve una conexión a la base SQLite.
    """

    connection = sqlite3.connect(DB_PATH)

    # Permite acceder a las columnas por nombre.
    connection.row_factory = sqlite3.Row

    return connection