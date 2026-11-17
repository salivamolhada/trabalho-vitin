"""Componente de tabela estilizada sobre tema rubi 3D usando ttk.Treeview."""

from __future__ import annotations

from tkinter import ttk
from typing import Any, Callable, Sequence

import customtkinter as ctk

from ui.theme import COR_CARD_BRANCO, COR_DOURADO, COR_OURO_CLARO, COR_TEXTO_ESCURO


class StyledTreeviewTable(ctk.CTkFrame):
    """Tabela responsiva rubi/dourado com rolagem vertical e callback de seleção de linha."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        colunas: Sequence[tuple[str, str, int]],
        altura: int = 10,
        on_select: Callable[[tuple[Any, ...]], None] | None = None,
    ) -> None:
        super().__init__(
            master,
            fg_color=COR_CARD_BRANCO,
            corner_radius=14,
            border_width=2,
            border_color=COR_DOURADO,
        )
        self.on_select = on_select
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Natal.Treeview",
            background=COR_CARD_BRANCO,
            foreground=COR_TEXTO_ESCURO,
            fieldbackground=COR_CARD_BRANCO,
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        style.configure(
            "Natal.Treeview.Heading",
            background="#3E060A",
            foreground=COR_OURO_CLARO,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 6),
        )
        style.map(
            "Natal.Treeview",
            background=[("selected", COR_DOURADO)],
            foreground=[("selected", "#3B0609")],
        )

        ids_colunas = [c[0] for c in colunas]
        self.tree = ttk.Treeview(
            self,
            columns=ids_colunas,
            show="headings",
            height=altura,
            style="Natal.Treeview",
            selectmode="browse",
        )

        for col_id, titulo, largura in colunas:
            self.tree.heading(col_id, text=titulo)
            anchor = "center" if col_id in ("id", "quantidade", "data", "disponivel") else "w"
            self.tree.column(col_id, width=largura, minwidth=60, anchor=anchor)

        self.tree.tag_configure("par", background="#560B10", foreground="#FFF9F0")
        self.tree.tag_configure("impar", background="#680E14", foreground="#FFF9F0")
        self.tree.tag_configure("alerta", background="#991B1B", foreground="#FFE4E6")

        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(2, 8), pady=8)

        if self.on_select is not None:
            self.tree.bind("<<TreeviewSelect>>", self._handle_select)

    def _handle_select(self, _event: object) -> None:
        selecionados = self.tree.selection()
        if selecionados and self.on_select:
            valores = self.tree.item(selecionados[0], "values")
            self.on_select(valores)

    def atualizar_linhas(
        self, linhas: Sequence[tuple[Any, ...]], alertas_indices: set[int] | None = None
    ) -> None:
        """Limpa e repovoa a tabela com alternância de cores e destaque opcional de alerta."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        alertas = alertas_indices or set()
        for idx, linha in enumerate(linhas):
            tag = "alerta" if idx in alertas else ("par" if idx % 2 == 0 else "impar")
            self.tree.insert("", "end", values=linha, tags=(tag,))

    def obter_selecionado(self) -> tuple[Any, ...] | None:
        """Retorna os valores da linha atualmente selecionada ou None."""
        selecionados = self.tree.selection()
        if not selecionados:
            return None
        return self.tree.item(selecionados[0], "values")
