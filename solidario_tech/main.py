"""Ponto de entrada da aplicação desktop Solidário Tech."""

from __future__ import annotations

import sys
from pathlib import Path

# Garante que os imports relativos ao diretório solidario_tech funcionem de qualquer cwd
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.connection import DatabaseConnection, get_logger
from database.seed import popular_dados_exemplo
from ui.app import SolidarioTechApp


def main() -> None:
    """Inicializa o banco SQLite, carrega dados de exemplo se vazio e abre a interface."""
    logger = get_logger("main")
    try:
        db = DatabaseConnection()
        db.inicializar_banco()
        popular_dados_exemplo(db)

        app = SolidarioTechApp(db)
        app.mainloop()
    except Exception as exc:
        logger.exception("Erro fatal ao iniciar o Solidário Tech: %s", exc)
        raise


if __name__ == "__main__":
    main()
