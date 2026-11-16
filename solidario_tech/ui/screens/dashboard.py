"""Tela Inicial (Dashboard) Natal Branco com pisca-pisca, contador e últimas 5 doações."""

from __future__ import annotations

import customtkinter as ctk

from models.doacao import formatar_data_br
from services.distribuicao_service import DistribuicaoService
from services.doacao_service import DoacaoService
from ui.components.card import KPICard, PiscaPiscaStrip
from ui.components.table import StyledTreeviewTable
from ui.theme import (
    COR_BRANCO_NEVE,
    COR_CARD_BRANCO,
    COR_DOURADO,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
    COR_VERDE_PINHEIRO,
    COR_VERMELHO_NATAL,
    FRASES_SOLIDARIEDADE,
    calcular_dias_para_natal,
)


class DashboardScreen(ctk.CTkFrame):
    """Exibe indicadores principais, banner Natal Branco com pisca-pisca e últimas doações."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        doacao_service: DoacaoService,
        distribuicao_service: DistribuicaoService,
    ) -> None:
        super().__init__(master, fg_color=COR_BRANCO_NEVE)
        self.doacao_service = doacao_service
        self.distribuicao_service = distribuicao_service
        self.frase_index = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Banner Natal Branco com pisca-pisca + Contador Regressivo
        banner = ctk.CTkFrame(
            self,
            fg_color=COR_CARD_BRANCO,
            corner_radius=14,
            border_width=2,
            border_color=COR_DOURADO,
        )
        banner.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        banner.grid_columnconfigure(0, weight=1)

        PiscaPiscaStrip(banner, qtd_lampadas=14, bg_color=COR_CARD_BRANCO).grid(
            row=0, column=0, columnspan=2, padx=10, pady=(6, 0), sticky="ew"
        )

        ctk.CTkLabel(
            banner,
            text="🎄 Feliz Natal! Que a solidariedade transforme vidas.",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COR_VERDE_PINHEIRO,
            anchor="w",
        ).grid(row=1, column=0, padx=20, pady=(6, 4), sticky="w")

        self.lbl_frase = ctk.CTkLabel(
            banner,
            text=f"⭐ \"{FRASES_SOLIDARIEDADE[0]}\"",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color=COR_TEXTO_SUAVE,
            anchor="w",
        )
        self.lbl_frase.grid(row=2, column=0, padx=20, pady=(0, 14), sticky="w")

        dias_natal = calcular_dias_para_natal()
        texto_contagem = (
            "🎅 Hoje é Natal!"
            if dias_natal == 0
            else f"🦌 Faltam {dias_natal} dias para o Natal (25/12)"
        )
        countdown_box = ctk.CTkFrame(
            banner,
            fg_color=COR_BRANCO_NEVE,
            corner_radius=10,
            border_width=1,
            border_color=COR_DOURADO,
        )
        countdown_box.grid(row=1, column=1, rowspan=2, padx=20, pady=10, sticky="e")

        ctk.CTkLabel(
            countdown_box,
            text=texto_contagem,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COR_VERMELHO_NATAL,
        ).pack(padx=14, pady=10)

        # Cards de Resumo (KPIs) com pisca-pisca nos itens
        cards_row = ctk.CTkFrame(self, fg_color="transparent")
        cards_row.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        for col in range(3):
            cards_row.grid_columnconfigure(col, weight=1)

        self.card_doado = KPICard(
            cards_row,
            titulo="🎁 Total de Doações Recebidas",
            valor="0",
            subtitulo="Soma acumulada na campanha",
            cor_destaque=COR_VERDE_PINHEIRO,
        )
        self.card_doado.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.card_distribuido = KPICard(
            cards_row,
            titulo="⭐ Total Distribuído",
            valor="0",
            subtitulo="Itens entregues às famílias",
            cor_destaque=COR_VERMELHO_NATAL,
        )
        self.card_distribuido.grid(row=0, column=1, sticky="ew", padx=4)

        self.card_estoque = KPICard(
            cards_row,
            titulo="🎄 Itens em Estoque",
            valor="0",
            subtitulo="Prontos para distribuição",
            cor_destaque="#B08A17",
        )
        self.card_estoque.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        # Cabeçalho da mini-tabela
        sec_header = ctk.CTkFrame(self, fg_color="transparent")
        sec_header.grid(row=2, column=0, sticky="ew", pady=(4, 6))
        sec_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            sec_header,
            text="🎁 Últimos 5 Registros de Doação",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COR_TEXTO_ESCURO,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            sec_header,
            text="Atualizar",
            width=100,
            height=30,
            corner_radius=8,
            fg_color=COR_VERDE_PINHEIRO,
            command=self.atualizar_dados,
        ).grid(row=0, column=1, sticky="e")

        self.tabela = StyledTreeviewTable(
            self,
            colunas=[
                ("id", "ID", 60),
                ("doador", "Doador", 240),
                ("tipo", "Categoria", 150),
                ("quantidade", "Qtd.", 90),
                ("data", "Data", 110),
                ("descricao", "Descrição", 260),
            ],
            altura=8,
        )
        self.tabela.grid(row=3, column=0, sticky="nsew")

        self._agendar_rotacao_frase()

    def _agendar_rotacao_frase(self) -> None:
        """Alterna automaticamente a frase motivacional natalina a cada 8 segundos."""
        self.frase_index = (self.frase_index + 1) % len(FRASES_SOLIDARIEDADE)
        self.lbl_frase.configure(text=f"⭐ \"{FRASES_SOLIDARIEDADE[self.frase_index]}\"")
        self.after(8000, self._agendar_rotacao_frase)

    def atualizar_dados(self) -> None:
        """Recarrega os indicadores e as últimas 5 doações do SQLite."""
        total_doado = self.doacao_service.obter_total_doado()
        total_dist = self.distribuicao_service.obter_total_distribuido()
        total_est = self.distribuicao_service.obter_total_em_estoque()

        self.card_doado.atualizar_valor(f"{total_doado}")
        self.card_distribuido.atualizar_valor(f"{total_dist}")

        estoque_itens = self.distribuicao_service.listar_estoque()
        baixos = sum(1 for item in estoque_itens if item.esta_baixo())
        sub_est = (
            f"⚠️ {baixos} categoria(s) abaixo de 5 un."
            if baixos > 0
            else "Todas as categorias em nível seguro"
        )
        self.card_estoque.atualizar_valor(f"{total_est}", sub_est)

        ultimas = self.doacao_service.obter_ultimas_doacoes(limite=5)
        linhas = [
            (
                d.id,
                d.doador,
                f"{d.emoji} {d.tipo_rotulo}",
                d.quantidade,
                formatar_data_br(d.data_doacao),
                d.descricao or "—",
            )
            for d in ultimas
        ]
        self.tabela.atualizar_linhas(linhas)
