"""Modelo de domínio para Doação."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

CATEGORIAS_VALIDAS: dict[str, tuple[str, str]] = {
    "brinquedo": ("🎁", "Brinquedo"),
    "alimento": ("🍪", "Alimento"),
    "roupa": ("🧥", "Roupa"),
    "dinheiro": ("💰", "Dinheiro"),
    "cesta": ("🧺", "Cesta básica"),
}


@dataclass
class Doacao:
    """Representa uma doação registrada na campanha de Natal."""

    doador: str
    tipo: str
    quantidade: int
    data_doacao: str
    descricao: str = ""
    id: int | None = None
    criado_em: str | None = None

    def validar(self) -> None:
        """Valida regras de integridade da doação antes da persistência."""
        if not self.doador or not self.doador.strip():
            raise ValueError("Informe o nome do doador.")
        if len(self.doador.strip()) < 2:
            raise ValueError("O nome do doador deve ter pelo menos 2 caracteres.")
        if self.tipo not in CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Tipo de item inválido '{self.tipo}'. Escolha entre: {', '.join(CATEGORIAS_VALIDAS)}."
            )
        if not isinstance(self.quantidade, int) or self.quantidade <= 0:
            raise ValueError("A quantidade doada deve ser um número inteiro maior que zero.")
        self.data_doacao = normalizar_data_iso(self.data_doacao)
        self.doador = self.doador.strip()
        self.descricao = (self.descricao or "").strip()

    @property
    def emoji(self) -> str:
        """Retorna o emoji natalino correspondente ao tipo da doação."""
        return CATEGORIAS_VALIDAS.get(self.tipo, ("🎄", self.tipo))[0]

    @property
    def tipo_rotulo(self) -> str:
        """Retorna o nome legível do tipo da doação."""
        return CATEGORIAS_VALIDAS.get(self.tipo, ("🎄", self.tipo))[1]

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Doacao":
        """Constrói uma instância de Doacao a partir de um registro SQLite."""
        return cls(
            id=row["id"],
            doador=row["doador"],
            tipo=row["tipo"],
            quantidade=int(row["quantidade"]),
            data_doacao=row["data_doacao"],
            descricao=row["descricao"] or "",
            criado_em=row["criado_em"],
        )


def normalizar_data_iso(data_str: str) -> str:
    """Aceita formatos YYYY-MM-DD ou DD/MM/YYYY e devolve YYYY-MM-DD validado."""
    texto = (data_str or "").strip()
    if not texto:
        raise ValueError("Informe a data no formato DD/MM/AAAA ou AAAA-MM-DD.")
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(texto, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError("Data inválida. Use o formato DD/MM/AAAA (ex.: 15/12/2026) ou AAAA-MM-DD.")


def formatar_data_br(data_iso: str) -> str:
    """Converte YYYY-MM-DD para DD/MM/YYYY para exibição amigável na interface."""
    try:
        return datetime.strptime(data_iso[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return data_iso
