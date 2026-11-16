"""Componentes de cards natalinos com cordão de pisca-pisca animado nos itens."""

from __future__ import annotations

import tkinter as tk
import customtkinter as ctk

from ui.theme import (
    COR_ALERTA_FUNDO,
    COR_CARD_BRANCO,
    COR_CINZA_CLARO,
    COR_DOURADO,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
    COR_VERDE_PINHEIRO,
    COR_VERMELHO_NATAL,
    CORES_PISCA_ACESO,
    CORES_PISCA_APAGADO,
)


class PiscaPiscaStrip(ctk.CTkFrame):
    """Cordão animado de pisca-pisca natalino embutido no topo de cards e cabeçalhos."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        qtd_lampadas: int = 9,
        bg_color: str = COR_CARD_BRANCO,
        altura: int = 18,
    ) -> None:
        super().__init__(master, fg_color=bg_color, height=altura, corner_radius=0)
        self.qtd_lampadas = qtd_lampadas
        self.bg_color = bg_color
        self.fase = 0
        self.lampadas_ids: list[int] = []

        self.canvas = tk.Canvas(
            self,
            height=altura,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="x", expand=True, padx=6)
        self.canvas.bind("<Configure>", self._desenhar)
        self._agendar_pisca()

    def _desenhar(self, _event: object | None = None) -> None:
        largura = max(self.canvas.winfo_width(), 120)
        self.canvas.delete("all")
        self.lampadas_ids.clear()

        # Fio prateado conectando as lâmpadas
        self.canvas.create_line(8, 4, largura - 8, 4, fill="#CBD5E1", width=1.5)

        passo = (largura - 24) / max(self.qtd_lampadas - 1, 1)
        for i in range(self.qtd_lampadas):
            cx = 12 + i * passo
            self.canvas.create_rectangle(cx - 2, 3, cx + 2, 6, fill="#94A3B8", outline="")
            acesa = (i + self.fase) % 2 == 0
            cor = (
                CORES_PISCA_ACESO[i % len(CORES_PISCA_ACESO)]
                if acesa
                else CORES_PISCA_APAGADO[i % len(CORES_PISCA_APAGADO)]
            )
            bulb = self.canvas.create_oval(
                cx - 4, 6, cx + 4, 15, fill=cor, outline="#E2E8F0", width=0.5
            )
            self.lampadas_ids.append(bulb)

    def _agendar_pisca(self) -> None:
        self.fase = (self.fase + 1) % 2
        for i, bulb in enumerate(self.lampadas_ids):
            acesa = (i + self.fase) % 2 == 0
            cor = (
                CORES_PISCA_ACESO[i % len(CORES_PISCA_ACESO)]
                if acesa
                else CORES_PISCA_APAGADO[i % len(CORES_PISCA_APAGADO)]
            )
            self.canvas.itemconfigure(bulb, fill=cor)
        self.after(550, self._agendar_pisca)


class KPICard(ctk.CTkFrame):
    """Card de resumo métrico Natal Branco com pisca-pisca animado no topo."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        titulo: str,
        valor: str,
        subtitulo: str = "",
        cor_destaque: str = COR_VERDE_PINHEIRO,
    ) -> None:
        super().__init__(
            master,
            fg_color=COR_CARD_BRANCO,
            corner_radius=12,
            border_width=1,
            border_color=COR_CINZA_CLARO,
        )
        self.grid_columnconfigure(0, weight=1)

        self.pisca = PiscaPiscaStrip(self, qtd_lampadas=7, bg_color=COR_CARD_BRANCO)
        self.pisca.grid(row=0, column=0, padx=6, pady=(6, 0), sticky="ew")

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
            anchor="w",
        )
        self.lbl_titulo.grid(row=1, column=0, padx=16, pady=(6, 2), sticky="ew")

        self.lbl_valor = ctk.CTkLabel(
            self,
            text=valor,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=cor_destaque,
            anchor="w",
        )
        self.lbl_valor.grid(row=2, column=0, padx=16, pady=2, sticky="ew")

        self.lbl_subtitulo = ctk.CTkLabel(
            self,
            text=subtitulo,
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_SUAVE,
            anchor="w",
        )
        self.lbl_subtitulo.grid(row=3, column=0, padx=16, pady=(0, 14), sticky="ew")

    def atualizar_valor(self, novo_valor: str, novo_subtitulo: str | None = None) -> None:
        """Atualiza dinamicamente os valores exibidos no card."""
        self.lbl_valor.configure(text=novo_valor)
        if novo_subtitulo is not None:
            self.lbl_subtitulo.configure(text=novo_subtitulo)


class EstoqueCategoryCard(ctk.CTkFrame):
    """Card visual de item com pisca-pisca natalino e alerta vermelho quando < 5 unidades."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        emoji: str,
        nome: str,
        quantidade: int,
    ) -> None:
        baixo = quantidade < 5
        fundo = COR_ALERTA_FUNDO if baixo else COR_CARD_BRANCO
        super().__init__(
            master,
            fg_color=fundo,
            corner_radius=12,
            border_width=2 if baixo else 1,
            border_color=COR_VERMELHO_NATAL if baixo else COR_DOURADO,
        )
        self.grid_columnconfigure(0, weight=1)

        self.pisca = PiscaPiscaStrip(self, qtd_lampadas=6, bg_color=fundo)
        self.pisca.grid(row=0, column=0, padx=6, pady=(6, 0), sticky="ew")

        self.lbl_icone = ctk.CTkLabel(
            self,
            text=f"{emoji}  {nome}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_VERMELHO_NATAL if baixo else COR_VERDE_PINHEIRO,
            anchor="w",
        )
        self.lbl_icone.grid(row=1, column=0, padx=14, pady=(6, 4), sticky="ew")

        self.lbl_qtd = ctk.CTkLabel(
            self,
            text=f"{quantidade} un.",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COR_VERMELHO_NATAL if baixo else COR_TEXTO_ESCURO,
            anchor="w",
        )
        self.lbl_qtd.grid(row=2, column=0, padx=14, pady=2, sticky="ew")

        status_texto = "⚠️ Estoque baixo (< 5)" if baixo else "✅ Nível adequado"
        self.lbl_status = ctk.CTkLabel(
            self,
            text=status_texto,
            font=ctk.CTkFont(size=12, weight="bold" if baixo else "normal"),
            text_color=COR_VERMELHO_NATAL if baixo else COR_TEXTO_SUAVE,
            anchor="w",
        )
        self.lbl_status.grid(row=3, column=0, padx=14, pady=(2, 14), sticky="ew")
