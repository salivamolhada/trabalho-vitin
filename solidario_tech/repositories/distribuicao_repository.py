"""Repositório SQLite para registros de Distribuições."""

from __future__ import annotations

import sqlite3
from typing import Optional

from database.connection import DatabaseConnection
from models.distribuicao import Distribuicao


class DistribuicaoRepository:
    """Encapsula operações de persistência e consulta da tabela `distribuicoes`."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def inserir(
        self, distribuicao: Distribuicao, conn: Optional[sqlite3.Connection] = None
    ) -> int:
        """Insere uma nova distribuição e retorna o ID criado."""
        sql = """
            INSERT INTO distribuicoes (doacao_id, item_tipo, quantidade, beneficiario, data_entrega, responsavel)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            distribuicao.doacao_id,
            distribuicao.item_tipo,
            distribuicao.quantidade,
            distribuicao.beneficiario,
            distribuicao.data_entrega,
            distribuicao.responsavel,
        )
        if conn is not None:
            cursor = conn.execute(sql, params)
            return int(cursor.lastrowid)

        with self.db.transaction() as local_conn:
            cursor = local_conn.execute(sql, params)
            return int(cursor.lastrowid)

    def listar(self, filtro_beneficiario: str = "") -> list[Distribuicao]:
        """Lista distribuições ordenadas por data decrescente com busca por beneficiário."""
        sql = "SELECT * FROM distribuicoes WHERE 1=1"
        params: list[object] = []

        if filtro_beneficiario.strip():
            sql += " AND LOWER(beneficiario) LIKE ?"
            params.append(f"%{filtro_beneficiario.strip().lower()}%")

        sql += " ORDER BY data_entrega DESC, id DESC"

        with self.db.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [Distribuicao.from_row(row) for row in rows]

    def somar_total(self) -> int:
        """Retorna a soma total de itens entregues aos beneficiários."""
        sql = "SELECT COALESCE(SUM(quantidade), 0) AS total FROM distribuicoes"
        with self.db.connect() as conn:
            row = conn.execute(sql).fetchone()
            return int(row["total"]) if row else 0
