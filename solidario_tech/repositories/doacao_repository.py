"""Repositório SQLite para operações CRUD de Doações."""

from __future__ import annotations

import sqlite3
from typing import Optional

from database.connection import DatabaseConnection
from models.doacao import Doacao


class DoacaoRepository:
    """Encapsula todas as consultas SQL da tabela `doacoes`."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def inserir(self, doacao: Doacao, conn: Optional[sqlite3.Connection] = None) -> int:
        """Insere uma nova doação e retorna o ID gerado."""
        sql = """
            INSERT INTO doacoes (doador, tipo, quantidade, data_doacao, descricao)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            doacao.doador,
            doacao.tipo,
            doacao.quantidade,
            doacao.data_doacao,
            doacao.descricao,
        )
        if conn is not None:
            cursor = conn.execute(sql, params)
            return int(cursor.lastrowid)

        with self.db.transaction() as local_conn:
            cursor = local_conn.execute(sql, params)
            return int(cursor.lastrowid)

    def atualizar(self, doacao: Doacao, conn: Optional[sqlite3.Connection] = None) -> None:
        """Atualiza os campos de uma doação existente pelo ID."""
        if doacao.id is None:
            raise ValueError("ID da doação é obrigatório para atualização.")
        sql = """
            UPDATE doacoes
            SET doador = ?, tipo = ?, quantidade = ?, data_doacao = ?, descricao = ?
            WHERE id = ?
        """
        params = (
            doacao.doador,
            doacao.tipo,
            doacao.quantidade,
            doacao.data_doacao,
            doacao.descricao,
            doacao.id,
        )
        if conn is not None:
            conn.execute(sql, params)
            return

        with self.db.transaction() as local_conn:
            local_conn.execute(sql, params)

    def excluir(self, doacao_id: int, conn: Optional[sqlite3.Connection] = None) -> None:
        """Remove uma doação do banco pelo ID."""
        sql = "DELETE FROM doacoes WHERE id = ?"
        if conn is not None:
            conn.execute(sql, (doacao_id,))
            return

        with self.db.transaction() as local_conn:
            local_conn.execute(sql, (doacao_id,))

    def buscar_por_id(
        self, doacao_id: int, conn: Optional[sqlite3.Connection] = None
    ) -> Optional[Doacao]:
        """Retorna uma doação específica ou None caso não exista."""
        sql = "SELECT * FROM doacoes WHERE id = ?"
        if conn is not None:
            row = conn.execute(sql, (doacao_id,)).fetchone()
            return Doacao.from_row(row) if row else None

        with self.db.connect() as local_conn:
            row = local_conn.execute(sql, (doacao_id,)).fetchone()
            return Doacao.from_row(row) if row else None

    def listar(
        self, filtro_doador: str = "", filtro_tipo: str = "todos"
    ) -> list[Doacao]:
        """Lista doações ordenadas por data decrescente, com filtros opcionais."""
        query = "SELECT * FROM doacoes WHERE 1=1"
        params: list[object] = []

        if filtro_doador.strip():
            query += " AND LOWER(doador) LIKE ?"
            params.append(f"%{filtro_doador.strip().lower()}%")

        if filtro_tipo and filtro_tipo != "todos":
            query += " AND tipo = ?"
            params.append(filtro_tipo)

        query += " ORDER BY data_doacao DESC, id DESC"

        with self.db.connect() as conn:
            rows = conn.execute(query, params).fetchall()
            return [Doacao.from_row(row) for row in rows]

    def listar_ultimas(self, limite: int = 5) -> list[Doacao]:
        """Retorna os últimos registros de doação para o Dashboard."""
        sql = "SELECT * FROM doacoes ORDER BY data_doacao DESC, id DESC LIMIT ?"
        with self.db.connect() as conn:
            rows = conn.execute(sql, (limite,)).fetchall()
            return [Doacao.from_row(row) for row in rows]

    def somar_total(self) -> int:
        """Retorna a soma total de itens/valores recebidos em doações."""
        sql = "SELECT COALESCE(SUM(quantidade), 0) AS total FROM doacoes"
        with self.db.connect() as conn:
            row = conn.execute(sql).fetchone()
            return int(row["total"]) if row else 0
