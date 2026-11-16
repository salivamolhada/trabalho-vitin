"""Camada de serviços e regras de negócio do Solidário Tech."""

from services.distribuicao_service import DistribuicaoService, EstoqueInsuficienteError
from services.doacao_service import DoacaoService

__all__ = [
    "DoacaoService",
    "DistribuicaoService",
    "EstoqueInsuficienteError",
    "RelatorioService",
]


def __getattr__(name: str):
    """Importação sob demanda do RelatorioService para não exigir Matplotlib em scripts de DB."""
    if name == "RelatorioService":
        from services.relatorio_service import RelatorioService

        return RelatorioService
    raise AttributeError(f"module 'services' has no attribute {name!r}")
