"""Repositório SQLite para controle de Estoque."""

from __future__ import annotations

import sqlite3
from typing import Optional

from database.connection import DatabaseConnection
from models.doacao import CATEGORIAS_VALIDAS
from models.estoque import Estoque


class EstoqueRepository:
    """Encapsula operações de leitura e atualização atômica da tabela `estoque`."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def inicializar_categorias(self, conn: Optional[sqlite3.Connection] = None) -> None:
        """Garante que todas as 5 categorias padrão existam na tabela `estoque`."""
        sql = "INSERT OR IGNORE INTO estoque (tipo, quantidade_disponivel) VALUES (?, 0)"
        if conn is not None:
            for tipo in CATEGORIAS_VALIDAS:
                conn.execute(sql, (tipo,))
            return

        with self.db.transaction() as local_conn:
            for tipo in CATEGORIAS_VALIDAS:
                local_conn.execute(sql, (tipo,))

    def buscar_por_tipo(
        self, tipo: str, conn: Optional[sqlite3.Connection] = None
    ) -> Optional[Estoque]:
        """Busca o registro de estoque de uma categoria."""
        sql = "SELECT * FROM estoque WHERE tipo = ?"
        if conn is not None:
            row = conn.execute(sql, (tipo,)).fetchone()
            return Estoque.from_row(row) if row else None

        with self.db.connect() as local_conn:
            row = local_conn.execute(sql, (tipo,)).fetchone()
            return Estoque.from_row(row) if row else None

    def listar_todos(self) -> list[Estoque]:
        """Lista todas as categorias do estoque em ordem padronizada."""
        ordem = list(CATEGORIAS_VALIDAS.keys())
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM estoque").fetchall()
            itens = [Estoque.from_row(row) for row in rows]
            itens.sort(key=lambda item: ordem.index(item.tipo) if item.tipo in ordem else 99)
            return itens

    def ajustar_quantidade(
        self, tipo: str, delta: int, conn: Optional[sqlite3.Connection] = None
    ) -> Estoque:
        """Aplica um incremento ou decremento no estoque impedindo saldo negativo."""
        def _executar(c: sqlite3.Connection) -> Estoque:
            atual = self.buscar_por_tipo(tipo, conn=c)
            if atual is None:
                self.inicializar_categorias(conn=c)
                atual = self.buscar_por_tipo(tipo, conn=c)
                if atual is None:
                    raise ValueError(f"Categoria de estoque desconhecida: {tipo}")

            novo_saldo = atual.validar_ajuste(delta)
            c.execute(
                """
                UPDATE estoque
                SET quantidade_disponivel = ?, atualizado_em = CURRENT_TIMESTAMP
                WHERE tipo = ?
                """,
                (novo_saldo, tipo),
            )
            atualizado = self.buscar_por_tipo(tipo, conn=c)
            assert atualizado is not None
            return atualizado

        if conn is not None:
            return _executar(conn)

        with self.db.transaction() as local_conn:
            return _executar(local_conn)

    def somar_total_disponivel(self) -> int:
        """Soma todas as unidades disponíveis em estoque."""
        sql = "SELECT COALESCE(SUM(quantidade_disponivel), 0) AS total FROM estoque"
        with self.db.connect() as conn:
            row = conn.execute(sql).fetchone()
            return int(row["total"]) if row else 0
