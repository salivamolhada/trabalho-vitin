"""Componentes de cards 3D coloridos com cordão de pisca-pisca 3D animado."""

from __future__ import annotations

import math
import tkinter as tk
import customtkinter as ctk

from ui.theme import (
    COR_CARD_BRANCO,
    COR_DOURADO,
    COR_OURO_CLARO,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
    COR_VERDE_PINHEIRO,
    COR_VERMELHO_NATAL,
    CORES_CATEGORIA_3D,
    CORES_PISCA_ACESO,
    CORES_PISCA_APAGADO,
)


class PiscaPiscaStrip(ctk.CTkFrame):
    """Cordão curvo animado de pisca-pisca 3D colorido embutido no topo de cards."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        qtd_lampadas: int = 9,
        bg_color: str = COR_CARD_BRANCO,
        altura: int = 22,
    ) -> None:
        super().__init__(master, fg_color=bg_color, height=altura, corner_radius=0)
        self.qtd_lampadas = qtd_lampadas
        self.bg_color = bg_color
        self.fase = 0
        self.lampadas_ids: list[tuple[int, int]] = []

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

        # Fio dourado ondulado conectando as lâmpadas 3D
        pontos_fio: list[float] = []
        for x in range(8, int(largura) - 7, 8):
            y = 4 + 3 * math.sin((x / max(largura, 1)) * math.pi * 4)
            pontos_fio.extend([x, y])
        if len(pontos_fio) >= 4:
            self.canvas.create_line(*pontos_fio, fill="#F5C451", width=1.6, smooth=True)

        passo = (largura - 26) / max(self.qtd_lampadas - 1, 1)
        for i in range(self.qtd_lampadas):
            cx = 13 + i * passo
            top_y = 5 if i % 2 == 0 else 7
            self.canvas.create_rectangle(cx - 2, top_y - 2, cx + 2, top_y + 1, fill="#0B3D2E", outline="#F5C451")
            acesa = (i + self.fase) % 2 == 0
            cor = (
                CORES_PISCA_ACESO[i % len(CORES_PISCA_ACESO)]
                if acesa
                else CORES_PISCA_APAGADO[i % len(CORES_PISCA_APAGADO)]
            )
            bulb = self.canvas.create_oval(
                cx - 5, top_y + 1, cx + 5, top_y + 12, fill=cor, outline="#FFF9F0" if acesa else "#6E0E15", width=0.8
            )
            brilho = self.canvas.create_oval(
                cx - 2.5, top_y + 2.5, cx - 0.3, top_y + 4.8, fill="#FFFFFF" if acesa else cor, outline=""
            )
            self.lampadas_ids.append((bulb, brilho))

    def _agendar_pisca(self) -> None:
        self.fase = (self.fase + 1) % 2
        for i, (bulb, brilho) in enumerate(self.lampadas_ids):
            acesa = (i + self.fase) % 2 == 0
            cor = (
                CORES_PISCA_ACESO[i % len(CORES_PISCA_ACESO)]
                if acesa
                else CORES_PISCA_APAGADO[i % len(CORES_PISCA_APAGADO)]
            )
            self.canvas.itemconfigure(
                bulb,
                fill=cor,
                outline="#FFF9F0" if acesa else "#6E0E15",
            )
            self.canvas.itemconfigure(brilho, fill="#FFFFFF" if acesa else cor)
        self.after(520, self._agendar_pisca)


class KPICard(ctk.CTkFrame):
    """Card 3D colorido de resumo métrico com efeito de profundidade e pisca-pisca."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        titulo: str,
        valor: str,
        subtitulo: str = "",
        cor_destaque: str = COR_OURO_CLARO,
        cor_fundo: str = COR_VERDE_PINHEIRO,
        cor_borda: str = "#34D399",
    ) -> None:
        # Base 3D inferior escura para efeito de elevação
        super().__init__(
            master,
            fg_color="#2A0306",
            corner_radius=16,
        )
        self.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(
            self,
            fg_color=cor_fundo,
            corner_radius=14,
            border_width=2,
            border_color=cor_borda,
        )
        inner.grid(row=0, column=0, padx=0, pady=(0, 5), sticky="nsew")
        inner.grid_columnconfigure(0, weight=1)

        self.pisca = PiscaPiscaStrip(inner, qtd_lampadas=7, bg_color=cor_fundo)
        self.pisca.grid(row=0, column=0, padx=6, pady=(6, 0), sticky="ew")

        self.lbl_titulo = ctk.CTkLabel(
            inner,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
            anchor="w",
        )
        self.lbl_titulo.grid(row=1, column=0, padx=16, pady=(6, 2), sticky="ew")

        self.lbl_valor = ctk.CTkLabel(
            inner,
            text=valor,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=cor_destaque,
            anchor="w",
        )
        self.lbl_valor.grid(row=2, column=0, padx=16, pady=2, sticky="ew")

        self.lbl_subtitulo = ctk.CTkLabel(
            inner,
            text=subtitulo,
            font=ctk.CTkFont(size=12),
            text_color="#FFF9F0",
            anchor="w",
        )
        self.lbl_subtitulo.grid(row=3, column=0, padx=16, pady=(0, 14), sticky="ew")

    def atualizar_valor(self, novo_valor: str, novo_subtitulo: str | None = None) -> None:
        """Atualiza dinamicamente os valores exibidos no card."""
        self.lbl_valor.configure(text=novo_valor)
        if novo_subtitulo is not None:
            self.lbl_subtitulo.configure(text=novo_subtitulo)


class EstoqueCategoryCard(ctk.CTkFrame):
    """Card 3D colorido por categoria com pisca-pisca natalino e alerta quando < 5."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        emoji: str,
        nome: str,
        quantidade: int,
        tipo_chave: str = "brinquedo",
    ) -> None:
        baixo = quantidade < 5
        cor_fundo, cor_borda_padrao = CORES_CATEGORIA_3D.get(
            tipo_chave, (COR_VERDE_PINHEIRO, COR_DOURADO)
        )
        cor_borda = "#FF4D6D" if baixo else cor_borda_padrao

        super().__init__(
            master,
            fg_color="#2A0306",
            corner_radius=16,
        )
        self.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(
            self,
            fg_color=cor_fundo,
            corner_radius=14,
            border_width=2,
            border_color=cor_borda,
        )
        inner.grid(row=0, column=0, padx=0, pady=(0, 5), sticky="nsew")
        inner.grid_columnconfigure(0, weight=1)

        self.pisca = PiscaPiscaStrip(inner, qtd_lampadas=6, bg_color=cor_fundo)
        self.pisca.grid(row=0, column=0, padx=6, pady=(6, 0), sticky="ew")

        self.lbl_icone = ctk.CTkLabel(
            inner,
            text=f"{emoji}  {nome}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#FFFFFF",
            anchor="w",
        )
        self.lbl_icone.grid(row=1, column=0, padx=14, pady=(6, 4), sticky="ew")

        self.lbl_qtd = ctk.CTkLabel(
            inner,
            text=f"{quantidade} un.",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COR_TEXTO_ESCURO,
            anchor="w",
        )
        self.lbl_qtd.grid(row=2, column=0, padx=14, pady=2, sticky="ew")

        status_texto = "⚠️ Estoque baixo (< 5)" if baixo else "✅ Nível adequado"
        self.lbl_status = ctk.CTkLabel(
            inner,
            text=status_texto,
            font=ctk.CTkFont(size=12, weight="bold" if baixo else "normal"),
            text_color="#FFE4E6" if baixo else "#D1FAE5",
            anchor="w",
        )
        self.lbl_status.grid(row=3, column=0, padx=14, pady=(2, 14), sticky="ew")
