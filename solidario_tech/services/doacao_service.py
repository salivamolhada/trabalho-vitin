"""Serviço de regras de negócio para Doações e sincronização com Estoque."""

from __future__ import annotations

from database.connection import DatabaseConnection, get_logger
from models.doacao import Doacao
from repositories.doacao_repository import DoacaoRepository
from repositories.estoque_repository import EstoqueRepository


class DoacaoService:
    """Coordena validações, persistência e atualização automática de estoque das doações."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db
        self.doacao_repo = DoacaoRepository(db)
        self.estoque_repo = EstoqueRepository(db)
        self.logger = get_logger("doacao_service")

    def registrar_doacao(
        self,
        doador: str,
        tipo: str,
        quantidade: int,
        data_doacao: str,
        descricao: str = "",
    ) -> Doacao:
        """Valida, grava a doação e incrementa o estoque em transação única."""
        doacao = Doacao(
            doador=doador,
            tipo=tipo,
            quantidade=quantidade,
            data_doacao=data_doacao,
            descricao=descricao,
        )
        doacao.validar()

        with self.db.transaction() as conn:
            doacao_id = self.doacao_repo.inserir(doacao, conn=conn)
            self.estoque_repo.ajustar_quantidade(doacao.tipo, doacao.quantidade, conn=conn)
            doacao.id = doacao_id

        self.logger.info(
            "Doação #%s registrada: %s (%sx %s)",
            doacao.id,
            doacao.doador,
            doacao.quantidade,
            doacao.tipo,
        )
        return doacao

    def atualizar_doacao(
        self,
        doacao_id: int,
        doador: str,
        tipo: str,
        quantidade: int,
        data_doacao: str,
        descricao: str = "",
    ) -> Doacao:
        """Atualiza uma doação existente recalculando o impacto líquido no estoque."""
        atualizada = Doacao(
            id=doacao_id,
            doador=doador,
            tipo=tipo,
            quantidade=quantidade,
            data_doacao=data_doacao,
            descricao=descricao,
        )
        atualizada.validar()

        with self.db.transaction() as conn:
            anterior = self.doacao_repo.buscar_por_id(doacao_id, conn=conn)
            if anterior is None:
                raise ValueError(f"Doação #{doacao_id} não encontrada.")

            if anterior.tipo == atualizada.tipo:
                delta = atualizada.quantidade - anterior.quantidade
                if delta != 0:
                    self.estoque_repo.ajustar_quantidade(atualizada.tipo, delta, conn=conn)
            else:
                # Se a categoria mudou, estorna da categoria anterior e soma na nova
                self.estoque_repo.ajustar_quantidade(anterior.tipo, -anterior.quantidade, conn=conn)
                self.estoque_repo.ajustar_quantidade(atualizada.tipo, atualizada.quantidade, conn=conn)

            self.doacao_repo.atualizar(atualizada, conn=conn)

        self.logger.info("Doação #%s atualizada (%s -> %sx %s)", doacao_id, atualizada.doador, atualizada.quantidade, atualizada.tipo)
        return atualizada

    def excluir_doacao(self, doacao_id: int) -> None:
        """Exclui uma doação e estorna a quantidade do estoque caso haja saldo suficiente."""
        with self.db.transaction() as conn:
            doacao = self.doacao_repo.buscar_por_id(doacao_id, conn=conn)
            if doacao is None:
                raise ValueError(f"Doação #{doacao_id} não encontrada.")

            self.estoque_repo.ajustar_quantidade(doacao.tipo, -doacao.quantidade, conn=conn)
            self.doacao_repo.excluir(doacao_id, conn=conn)

        self.logger.info("Doação #%s excluída (%sx %s estornados)", doacao_id, doacao.quantidade, doacao.tipo)

    def listar_doacoes(self, filtro_doador: str = "", filtro_tipo: str = "todos") -> list[Doacao]:
        """Lista doações filtradas para a tela de Cadastro de Doações."""
        return self.doacao_repo.listar(filtro_doador=filtro_doador, filtro_tipo=filtro_tipo)

    def obter_ultimas_doacoes(self, limite: int = 5) -> list[Doacao]:
        """Retorna as últimas doações para exibição no Dashboard."""
        return self.doacao_repo.listar_ultimas(limite=limite)

    def obter_total_doado(self) -> int:
        """Retorna o somatório de unidades recebidas."""
        return self.doacao_repo.somar_total()
