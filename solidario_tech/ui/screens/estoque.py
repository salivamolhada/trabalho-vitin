"""Tela de Controle de Estoque com cards 3D coloridos, alerta < 5 unidades e ajuste manual."""

from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from models.doacao import CATEGORIAS_VALIDAS
from services.distribuicao_service import DistribuicaoService
from ui.components.card import EstoqueCategoryCard
from ui.components.dialog import show_christmas_dialog
from ui.components.table import StyledTreeviewTable
from ui.theme import (
    COR_BRANCO_NEVE,
    COR_CARD_BRANCO,
    COR_DOURADO,
    COR_INPUT_FUNDO,
    COR_OURO_CLARO,
    COR_VERDE_ESCURO_HOVER,
    COR_VERDE_PINHEIRO,
    COR_VERMELHO_HOVER,
    COR_VERMELHO_NATAL,
)


class EstoqueScreen(ctk.CTkFrame):
    """Exibe os 5 cards 3D coloridos de categoria, alerta de estoque baixo e ajuste manual."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        distribuicao_service: DistribuicaoService,
        on_data_changed: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color=COR_BRANCO_NEVE)
        self.distribuicao_service = distribuicao_service
        self.on_data_changed = on_data_changed

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._opcoes_rotulo_para_chave = {
            f"{emoji} {rotulo}": chave for chave, (emoji, rotulo) in CATEGORIAS_VALIDAS.items()
        }

        # Container dos 5 cards 3D coloridos de categoria
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        for col in range(5):
            self.cards_frame.grid_columnconfigure(col, weight=1)

        # Painel de ajuste manual (Entrada / Saída)
        ajuste_frame = ctk.CTkFrame(
            self,
            fg_color=COR_CARD_BRANCO,
            corner_radius=14,
            border_width=2,
            border_color=COR_DOURADO,
        )
        ajuste_frame.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        ajuste_frame.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(
            ajuste_frame,
            text="📦 Ajuste Manual de Estoque:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COR_OURO_CLARO,
        ).grid(row=0, column=0, padx=(16, 10), pady=14, sticky="w")

        self.combo_categoria = ctk.CTkOptionMenu(
            ajuste_frame,
            values=list(self._opcoes_rotulo_para_chave.keys()),
            height=34,
            fg_color=COR_VERDE_PINHEIRO,
            button_color=COR_VERDE_ESCURO_HOVER,
        )
        self.combo_categoria.grid(row=0, column=1, padx=6, pady=14)

        self.entry_delta = ctk.CTkEntry(
            ajuste_frame,
            width=120,
            height=34,
            placeholder_text="Quantidade",
            fg_color=COR_INPUT_FUNDO,
            border_color=COR_DOURADO,
            text_color="#FFF9F0",
        )
        self.entry_delta.grid(row=0, column=2, padx=6, pady=14)

        ctk.CTkButton(
            ajuste_frame,
            text="+ Entrada",
            width=110,
            height=34,
            corner_radius=8,
            fg_color=COR_VERDE_PINHEIRO,
            hover_color=COR_VERDE_ESCURO_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._aplicar_ajuste(1),
        ).grid(row=0, column=3, padx=6, pady=14)

        ctk.CTkButton(
            ajuste_frame,
            text="- Saída",
            width=110,
            height=34,
            corner_radius=8,
            fg_color=COR_VERMELHO_NATAL,
            hover_color=COR_VERMELHO_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._aplicar_ajuste(-1),
        ).grid(row=0, column=4, padx=(6, 16), pady=14, sticky="w")

        # Tabela detalhada do estoque
        self.tabela = StyledTreeviewTable(
            self,
            colunas=[
                ("categoria", "Categoria", 220),
                ("disponivel", "Quantidade Disponível", 180),
                ("status", "Situação", 240),
                ("atualizado", "Última Atualização", 200),
            ],
            altura=8,
        )
        self.tabela.grid(row=2, column=0, sticky="nsew")

    def _aplicar_ajuste(self, sinal: int) -> None:
        try:
            texto = self.entry_delta.get().strip()
            if not texto.isdigit() or int(texto) <= 0:
                raise ValueError("Informe uma quantidade inteira positiva para ajustar o estoque.")
            valor = int(texto) * sinal
            tipo = self._opcoes_rotulo_para_chave[self.combo_categoria.get()]
            atualizado = self.distribuicao_service.ajustar_estoque_manual(tipo, valor)
            self.entry_delta.delete(0, "end")
            self.on_data_changed()
            acao = "entrada" if sinal > 0 else "saída"
            show_christmas_dialog(
                self,
                "Estoque Ajustado",
                f"Ajuste de {acao} aplicado para {atualizado.nome_exibicao}. Saldo atual: {atualizado.quantidade_disponivel} un.",
                icone="🎄",
            )
        except Exception as exc:
            show_christmas_dialog(self, "Erro no Ajuste de Estoque", str(exc), icone="⚠️", tipo="erro")

    def atualizar_dados(self) -> None:
        """Atualiza os 5 cards visuais 3D e a tabela de estoque destacando alertas < 5."""
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        itens = self.distribuicao_service.listar_estoque()
        linhas = []
        alertas: set[int] = set()

        for idx, item in enumerate(itens):
            card = EstoqueCategoryCard(
                self.cards_frame,
                emoji=item.emoji,
                nome=item.nome_exibicao,
                quantidade=item.quantidade_disponivel,
                tipo_chave=item.tipo,
            )
            padx = (0, 6) if idx == 0 else ((6, 0) if idx == 4 else 6)
            card.grid(row=0, column=idx, sticky="ew", padx=padx)

            baixo = item.esta_baixo(5)
            if baixo:
                alertas.add(idx)

            linhas.append(
                (
                    f"{item.emoji} {item.nome_exibicao}",
                    item.quantidade_disponivel,
                    "⚠️ Estoque baixo (< 5 unidades)" if baixo else "✅ Disponível",
                    item.atualizado_em or "—",
                )
            )

        self.tabela.atualizar_linhas(linhas, alertas_indices=alertas)
