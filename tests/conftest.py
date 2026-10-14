import pytest

from app.database.seed import seed_database


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """
    Reconstruye la base SQLite ficticia antes de ejecutar
    la suite de pruebas.
    """

    seed_database()
