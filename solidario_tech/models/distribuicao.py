"""Modelo de domínio para Distribuição."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from models.doacao import CATEGORIAS_VALIDAS, normalizar_data_iso


@dataclass
class Distribuicao:
    """Representa uma entrega de itens doados a um beneficiário."""

    item_tipo: str
    quantidade: int
    beneficiario: str
    data_entrega: str
    responsavel: str
    doacao_id: int | None = None
    id: int | None = None
    criado_em: str | None = None

    def validar(self) -> None:
        """Valida campos obrigatórios e formato da data de entrega."""
        if self.item_tipo not in CATEGORIAS_VALIDAS:
            raise ValueError("Selecione um tipo de item válido para distribuição.")
        if not isinstance(self.quantidade, int) or self.quantidade <= 0:
            raise ValueError("A quantidade a distribuir deve ser um número inteiro maior que zero.")
        if not self.beneficiario or len(self.beneficiario.strip()) < 2:
            raise ValueError("Informe o nome do beneficiário (mínimo 2 caracteres).")
        if not self.responsavel or len(self.responsavel.strip()) < 2:
            raise ValueError("Informe o nome do responsável pela entrega.")
        self.data_entrega = normalizar_data_iso(self.data_entrega)
        self.beneficiario = self.beneficiario.strip()
        self.responsavel = self.responsavel.strip()

    @property
    def emoji(self) -> str:
        """Retorna o emoji natalino correspondente ao item distribuído."""
        return CATEGORIAS_VALIDAS.get(self.item_tipo, ("⭐", self.item_tipo))[0]

    @property
    def item_rotulo(self) -> str:
        """Retorna o rótulo legível do item distribuído."""
        return CATEGORIAS_VALIDAS.get(self.item_tipo, ("⭐", self.item_tipo))[1]

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Distribuicao":
        """Constrói uma instância de Distribuicao a partir de um registro SQLite."""
        return cls(
            id=row["id"],
            doacao_id=row["doacao_id"],
            item_tipo=row["item_tipo"],
            quantidade=int(row["quantidade"]),
            beneficiario=row["beneficiario"],
            data_entrega=row["data_entrega"],
            responsavel=row["responsavel"],
            criado_em=row["criado_em"],
        )
