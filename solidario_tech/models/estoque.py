"""Modelo de domínio para Estoque."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from models.doacao import CATEGORIAS_VALIDAS


@dataclass
class Estoque:
    """Representa o saldo disponível de uma categoria de doação no estoque."""

    tipo: str
    quantidade_disponivel: int = 0
    id: int | None = None
    atualizado_em: str | None = None

    def esta_baixo(self, limite: int = 5) -> bool:
        """Retorna True quando o estoque está abaixo do limite mínimo de segurança."""
        return self.quantidade_disponivel < limite

    @property
    def emoji(self) -> str:
        """Emoji natalino correspondente à categoria."""
        return CATEGORIAS_VALIDAS.get(self.tipo, ("🎄", self.tipo))[0]

    @property
    def nome_exibicao(self) -> str:
        """Nome amigável da categoria."""
        return CATEGORIAS_VALIDAS.get(self.tipo, ("🎄", self.tipo))[1]

    def validar_ajuste(self, delta: int) -> int:
        """Calcula e valida o novo saldo após um ajuste positivo ou negativo."""
        novo_saldo = self.quantidade_disponivel + delta
        if novo_saldo < 0:
            raise ValueError(
                f"Ajuste inválido: o estoque de {self.nome_exibicao} não pode ficar negativo "
                f"(disponível: {self.quantidade_disponivel})."
            )
        return novo_saldo

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Estoque":
        """Constrói uma instância de Estoque a partir de um registro SQLite."""
        return cls(
            id=row["id"],
            tipo=row["tipo"],
            quantidade_disponivel=int(row["quantidade_disponivel"]),
            atualizado_em=row["atualizado_em"],
        )
