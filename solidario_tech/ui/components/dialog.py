"""Pop-ups natalinos 3D personalizados em vermelho e dourado com CTkToplevel."""

from __future__ import annotations

import customtkinter as ctk

from ui.theme import (
    COR_BRANCO_NEVE,
    COR_CARD_BRANCO,
    COR_DOURADO,
    COR_OURO_CLARO,
    COR_TEXTO_ESCURO,
    COR_VERDE_ESCURO_HOVER,
    COR_VERDE_PINHEIRO,
    COR_VERMELHO_HOVER,
    COR_VERMELHO_NATAL,
)


def show_christmas_dialog(
    master: ctk.CTkBaseClass,
    titulo: str,
    mensagem: str,
    icone: str = "🎁",
    tipo: str = "sucesso",
) -> None:
    """Exibe um pop-up estilizado (CTkToplevel) com tema natalino vermelho e foco modal."""
    cor_borda = "#FF6B81" if tipo == "erro" else COR_DOURADO
    cor_cabecalho = "#FDA4AF" if tipo == "erro" else COR_OURO_CLARO

    dialog = ctk.CTkToplevel(master)
    dialog.title(titulo)
    dialog.geometry("430x230")
    dialog.resizable(False, False)
    dialog.configure(fg_color=COR_BRANCO_NEVE)
    dialog.transient(master.winfo_toplevel())
    dialog.grab_set()

    container = ctk.CTkFrame(
        dialog,
        fg_color=COR_CARD_BRANCO,
        corner_radius=14,
        border_width=2,
        border_color=cor_borda,
    )
    container.pack(fill="both", expand=True, padx=14, pady=14)

    ctk.CTkLabel(
        container,
        text=f"{icone}  {titulo}",
        font=ctk.CTkFont(size=17, weight="bold"),
        text_color=cor_cabecalho,
    ).pack(pady=(18, 8), padx=16)

    ctk.CTkLabel(
        container,
        text=mensagem,
        font=ctk.CTkFont(size=13),
        text_color=COR_TEXTO_ESCURO,
        wraplength=360,
        justify="center",
    ).pack(pady=(4, 18), padx=18, expand=True)

    ctk.CTkButton(
        container,
        text="Fechar",
        width=130,
        height=36,
        corner_radius=8,
        fg_color=COR_VERMELHO_NATAL if tipo == "erro" else COR_VERDE_PINHEIRO,
        hover_color=COR_VERMELHO_HOVER if tipo == "erro" else COR_VERDE_ESCURO_HOVER,
        text_color="#FFFFFF",
        font=ctk.CTkFont(size=13, weight="bold"),
        command=dialog.destroy,
    ).pack(pady=(0, 16))

    dialog.wait_window()


def ask_christmas_confirm(
    master: ctk.CTkBaseClass,
    titulo: str,
    mensagem: str,
    icone: str = "🎄",
) -> bool:
    """Exibe um diálogo modal de confirmação Sim/Não e retorna a escolha booleana."""
    resultado = {"confirmado": False}

    dialog = ctk.CTkToplevel(master)
    dialog.title(titulo)
    dialog.geometry("430x230")
    dialog.resizable(False, False)
    dialog.configure(fg_color=COR_BRANCO_NEVE)
    dialog.transient(master.winfo_toplevel())
    dialog.grab_set()

    container = ctk.CTkFrame(
        dialog,
        fg_color=COR_CARD_BRANCO,
        corner_radius=14,
        border_width=2,
        border_color=COR_DOURADO,
    )
    container.pack(fill="both", expand=True, padx=14, pady=14)

    ctk.CTkLabel(
        container,
        text=f"{icone}  {titulo}",
        font=ctk.CTkFont(size=17, weight="bold"),
        text_color=COR_OURO_CLARO,
    ).pack(pady=(18, 8), padx=16)

    ctk.CTkLabel(
        container,
        text=mensagem,
        font=ctk.CTkFont(size=13),
        text_color=COR_TEXTO_ESCURO,
        wraplength=360,
        justify="center",
    ).pack(pady=(4, 16), padx=18, expand=True)

    botoes = ctk.CTkFrame(container, fg_color="transparent")
    botoes.pack(pady=(0, 16))

    def confirmar() -> None:
        resultado["confirmado"] = True
        dialog.destroy()

    ctk.CTkButton(
        botoes,
        text="Cancelar",
        width=120,
        height=36,
        corner_radius=8,
        fg_color="#3E060A",
        hover_color="#5A0B10",
        text_color="#FFF9F0",
        command=dialog.destroy,
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        botoes,
        text="Confirmar",
        width=120,
        height=36,
        corner_radius=8,
        fg_color=COR_VERMELHO_NATAL,
        hover_color=COR_VERMELHO_HOVER,
        text_color="#FFFFFF",
        font=ctk.CTkFont(size=13, weight="bold"),
        command=confirmar,
    ).pack(side="left", padx=8)

    dialog.wait_window()
    return resultado["confirmado"]
