"""Serviço de regras de negócio para Distribuições e controle de Estoque."""

from __future__ import annotations

from database.connection import DatabaseConnection, get_logger
from models.distribuicao import Distribuicao
from models.estoque import Estoque
from repositories.distribuicao_repository import DistribuicaoRepository
from repositories.estoque_repository import EstoqueRepository


class EstoqueInsuficienteError(ValueError):
    """Exceção lançada ao tentar distribuir mais itens do que há em estoque."""


class DistribuicaoService:
    """Garante integridade nas entregas e ajuste manual de estoque."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db
        self.distribuicao_repo = DistribuicaoRepository(db)
        self.estoque_repo = EstoqueRepository(db)
        self.logger = get_logger("distribuicao_service")

    def registrar_distribuicao(
        self,
        item_tipo: str,
        quantidade: int,
        beneficiario: str,
        data_entrega: str,
        responsavel: str,
        doacao_id: int | None = None,
    ) -> Distribuicao:
        """Registra uma entrega após verificar saldo suficiente em estoque."""
        distribuicao = Distribuicao(
            doacao_id=doacao_id,
            item_tipo=item_tipo,
            quantidade=quantidade,
            beneficiario=beneficiario,
            data_entrega=data_entrega,
            responsavel=responsavel,
        )
        distribuicao.validar()

        with self.db.transaction() as conn:
            estoque_atual = self.estoque_repo.buscar_por_tipo(distribuicao.item_tipo, conn=conn)
            disponivel = estoque_atual.quantidade_disponivel if estoque_atual else 0

            if distribuicao.quantidade > disponivel:
                raise EstoqueInsuficienteError(
                    f"Estoque insuficiente para {distribuicao.item_rotulo}! "
                    f"Disponível: {disponivel} | Solicitado: {distribuicao.quantidade}."
                )

            self.estoque_repo.ajustar_quantidade(
                distribuicao.item_tipo, -distribuicao.quantidade, conn=conn
            )
            dist_id = self.distribuicao_repo.inserir(distribuicao, conn=conn)
            distribuicao.id = dist_id

        self.logger.info(
            "Distribuição #%s registrada: %sx %s para %s (Resp.: %s)",
            distribuicao.id,
            distribuicao.quantidade,
            distribuicao.item_tipo,
            distribuicao.beneficiario,
            distribuicao.responsavel,
        )
        return distribuicao

    def listar_distribuicoes(self, filtro_beneficiario: str = "") -> list[Distribuicao]:
        """Lista histórico de entregas com busca por beneficiário."""
        return self.distribuicao_repo.listar(filtro_beneficiario=filtro_beneficiario)

    def obter_total_distribuido(self) -> int:
        """Retorna o total de itens já entregues."""
        return self.distribuicao_repo.somar_total()

    def listar_estoque(self) -> list[Estoque]:
        """Retorna o estoque atualizado das 5 categorias."""
        return self.estoque_repo.listar_todos()

    def obter_total_em_estoque(self) -> int:
        """Retorna a soma total de itens atualmente em estoque."""
        return self.estoque_repo.somar_total_disponivel()

    def ajustar_estoque_manual(self, tipo: str, delta: int) -> Estoque:
        """Permite ajuste manual (entrada positiva ou saída negativa) no estoque."""
        if not isinstance(delta, int) or delta == 0:
            raise ValueError("Informe um valor inteiro diferente de zero para o ajuste.")
        estoque = self.estoque_repo.ajustar_quantidade(tipo, delta)
        self.logger.info("Ajuste manual de estoque: %s (%+d) -> %d", tipo, delta, estoque.quantidade_disponivel)
        return estoque
