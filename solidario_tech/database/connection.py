"""Gerenciamento de conexão SQLite e logging centralizado em app.log."""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "solidario_tech.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
LOG_PATH = BASE_DIR / "app.log"


def get_logger(name: str = "solidario_tech") -> logging.Logger:
    """Configura e retorna o logger da aplicação gravando em app.log."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


class DatabaseConnection:
    """Classe responsável pela conexão com o SQLite e inicialização do esquema."""

    def __init__(self, db_path: Path | str | None = None) -> None:
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.logger = get_logger("database")

    def connect(self) -> sqlite3.Connection:
        """Abre uma conexão SQLite com RowFactory e integridade referencial ativa."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Gerenciador de contexto transacional com commit automático ou rollback em falha."""
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception as exc:
            conn.rollback()
            self.logger.exception("Erro na transação SQLite: %s", exc)
            raise
        finally:
            conn.close()

    def inicializar_banco(self) -> None:
        """Executa o schema.sql para criar tabelas e garantir as 5 categorias no estoque."""
        try:
            schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
            with self.transaction() as conn:
                conn.executescript(schema_sql)
            self.logger.info("Banco SQLite inicializado em %s", self.db_path)
        except Exception as exc:
            self.logger.exception("Falha ao inicializar banco SQLite: %s", exc)
            raise
