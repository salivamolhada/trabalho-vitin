"""Tela Sobre com créditos do Desafio Tech Solutions 2026 e arquitetura 3D colorida."""

from __future__ import annotations

import customtkinter as ctk

from ui.components.card import PiscaPiscaStrip
from ui.theme import (
    COR_BRANCO_NEVE,
    COR_CARD_BRANCO,
    COR_DOURADO,
    COR_OURO_CLARO,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
)


class SobreScreen(ctk.CTkFrame):
    """Apresenta o propósito social, equipe e pilares técnicos do projeto."""

    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master, fg_color=COR_BRANCO_NEVE)
        self.grid_columnconfigure(0, weight=1)

        hero = ctk.CTkFrame(
            self,
            fg_color="#8C141D",
            corner_radius=16,
            border_width=2,
            border_color=COR_DOURADO,
        )
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        PiscaPiscaStrip(hero, qtd_lampadas=14, bg_color="#8C141D").pack(
            fill="x", padx=10, pady=(6, 0)
        )

        ctk.CTkLabel(
            hero,
            text="🎄 Solidário Tech — Campanha de Natal",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFFFFF",
            anchor="w",
        ).pack(padx=22, pady=(10, 4), anchor="w")

        ctk.CTkLabel(
            hero,
            text="Projeto desenvolvido para o Desafio Tech Solutions 2026 • 3º A – Técnico em Desenvolvimento de Sistemas",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COR_OURO_CLARO,
            anchor="w",
        ).pack(padx=22, pady=(0, 18), anchor="w")

        info = ctk.CTkFrame(
            self,
            fg_color=COR_CARD_BRANCO,
            corner_radius=14,
            border_width=2,
            border_color=COR_DOURADO,
        )
        info.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ctk.CTkLabel(
            info,
            text="🎯 Problema Resolvido & Impacto Social",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_OURO_CLARO,
            anchor="w",
        ).pack(padx=20, pady=(16, 6), anchor="w")

        ctk.CTkLabel(
            info,
            text=(
                "Durante as campanhas solidárias de fim de ano, muitas ONGs e instituições comunitárias "
                "ainda controlam doações em planilhas soltas ou cadernos manuais, gerando erros de estoque "
                "e dificuldade para prestar contas. O Solidário Tech centraliza o cadastro de doações, "
                "o saldo automático por categoria, o registro seguro de entregas e indicadores visuais em tempo real."
            ),
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_ESCURO,
            wraplength=820,
            justify="left",
        ).pack(padx=20, pady=(0, 16), anchor="w")

        pilares = ctk.CTkFrame(self, fg_color="transparent")
        pilares.grid(row=2, column=0, sticky="ew")
        for i in range(3):
            pilares.grid_columnconfigure(i, weight=1)

        dados_pilares = [
            (
                "💾 Banco de Dados",
                "#127053",
                "#34D399",
                "SQLite 3 relacional com restrições CHECK, chaves estrangeiras, seed automático e transações atômicas entre doações, estoque e distribuições.",
            ),
            (
                "📊 Ciência de Dados",
                "#C82333",
                "#FDA4AF",
                "Agregações temporais e por categoria com Pandas, visualização analítica com Matplotlib e Seaborn embutidos via FigureCanvasTkAgg.",
            ),
            (
                "🛠️ Desenvolvimento de Sistemas",
                "#1D4ED8",
                "#93C5FD",
                "Python 3.11+ com Programação Orientada a Objetos, arquitetura em camadas (UI → Service → Repository → SQLite), Pillow e logs em app.log.",
            ),
        ]

        for idx, (titulo, cor_fundo, cor_borda, texto) in enumerate(dados_pilares):
            card = ctk.CTkFrame(
                pilares,
                fg_color=cor_fundo,
                corner_radius=14,
                border_width=2,
                border_color=cor_borda,
            )
            padx = (0, 6) if idx == 0 else ((6, 0) if idx == 2 else 6)
            card.grid(row=0, column=idx, sticky="nsew", padx=padx)

            PiscaPiscaStrip(card, qtd_lampadas=6, bg_color=cor_fundo).pack(
                fill="x", padx=6, pady=(6, 0)
            )

            ctk.CTkLabel(
                card,
                text=titulo,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=COR_OURO_CLARO,
                anchor="w",
            ).pack(padx=16, pady=(8, 6), anchor="w")

            ctk.CTkLabel(
                card,
                text=texto,
                font=ctk.CTkFont(size=12),
                text_color=COR_TEXTO_SUAVE,
                wraplength=240,
                justify="left",
            ).pack(padx=16, pady=(0, 16), anchor="w")

    def atualizar_dados(self) -> None:
        """Mantém compatibilidade com a interface padrão das telas."""
        return None
