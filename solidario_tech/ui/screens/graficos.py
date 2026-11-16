"""Tela de Gráficos Analíticos (Ciência de Dados com Pandas, Matplotlib e Seaborn)."""

from __future__ import annotations

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from services.relatorio_service import RelatorioService
from ui.theme import (
    COR_BRANCO_NEVE,
    COR_CARD_BRANCO,
    COR_CINZA_CLARO,
    COR_DOURADO,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
    COR_VERDE_ESCURO_HOVER,
    COR_VERDE_PINHEIRO,
    COR_VERMELHO_NATAL,
)


class GraficosScreen(ctk.CTkFrame):
    """Exibe os 4 gráficos embutidos via FigureCanvasTkAgg e o indicador Arrecadado vs. Distribuído."""

    def __init__(self, master: ctk.CTkBaseClass, relatorio_service: RelatorioService) -> None:
        super().__init__(master, fg_color=COR_BRANCO_NEVE)
        self.relatorio_service = relatorio_service

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Barra superior de KPI (Arrecadado vs. Distribuído)
        kpi_bar = ctk.CTkFrame(
            self,
            fg_color=COR_CARD_BRANCO,
            corner_radius=12,
            border_width=1,
            border_color=COR_DOURADO,
        )
        kpi_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        kpi_bar.grid_columnconfigure(0, weight=1)

        self.lbl_kpi = ctk.CTkLabel(
            kpi_bar,
            text="📊 Carregando indicadores...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COR_VERDE_PINHEIRO,
            anchor="w",
        )
        self.lbl_kpi.grid(row=0, column=0, padx=16, pady=12, sticky="w")

        ctk.CTkButton(
            kpi_bar,
            text="Atualizar Gráficos",
            width=140,
            height=32,
            corner_radius=8,
            fg_color=COR_VERDE_PINHEIRO,
            hover_color=COR_VERDE_ESCURO_HOVER,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.atualizar_dados,
        ).grid(row=0, column=1, padx=16, pady=10, sticky="e")

        # 4 painéis de gráficos (2x2)
        self.fig_barras = Figure(figsize=(5.2, 3.2), dpi=100)
        self.fig_pizza = Figure(figsize=(5.2, 3.2), dpi=100)
        self.fig_linha = Figure(figsize=(5.2, 3.2), dpi=100)
        self.fig_kpi = Figure(figsize=(5.2, 3.2), dpi=100)

        self.canvas_barras = self._criar_painel_grafico(self.fig_barras, row=1, col=0, padx=(0, 6), pady=(0, 6))
        self.canvas_pizza = self._criar_painel_grafico(self.fig_pizza, row=1, col=1, padx=(6, 0), pady=(0, 6))
        self.canvas_linha = self._criar_painel_grafico(self.fig_linha, row=2, col=0, padx=(0, 6), pady=(6, 0))
        self.canvas_kpi = self._criar_painel_grafico(self.fig_kpi, row=2, col=1, padx=(6, 0), pady=(6, 0))

    def _criar_painel_grafico(
        self, fig: Figure, row: int, col: int, padx: tuple[int, int], pady: tuple[int, int]
    ) -> FigureCanvasTkAgg:
        frame = ctk.CTkFrame(
            self,
            fg_color=COR_CARD_BRANCO,
            corner_radius=12,
            border_width=1,
            border_color=COR_CINZA_CLARO,
        )
        frame.grid(row=row, column=col, sticky="nsew", padx=padx, pady=pady)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        return canvas

    def atualizar_dados(self) -> None:
        """Recalcula os DataFrames Pandas e redesenha todas as figuras Matplotlib."""
        kpis = self.relatorio_service.obter_kpis()
        self.lbl_kpi.configure(
            text=(
                f"📊 Indicador da Campanha:  Arrecadado: {kpis['total_arrecadado']} un.  |  "
                f"Distribuído: {kpis['total_distribuido']} un. ({kpis['taxa_distribuicao']}%)  |  "
                f"Em Estoque: {kpis['total_estoque']} un."
            ),
            text_color=COR_VERMELHO_NATAL if kpis["total_estoque"] < 15 else COR_VERDE_PINHEIRO,
        )

        self.relatorio_service.gerar_grafico_barras(self.fig_barras)
        self.canvas_barras.draw()

        self.relatorio_service.gerar_grafico_pizza(self.fig_pizza)
        self.canvas_pizza.draw()

        self.relatorio_service.gerar_grafico_linha_30_dias(self.fig_linha)
        self.canvas_linha.draw()

        self.relatorio_service.gerar_grafico_comparativo_kpi(self.fig_kpi)
        self.canvas_kpi.draw()
