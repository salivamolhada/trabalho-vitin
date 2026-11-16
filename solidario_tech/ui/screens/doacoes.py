"""Tela de Cadastro de Doações (CRUD completo com atualização automática do estoque)."""

from __future__ import annotations

from datetime import date
from typing import Any, Callable

import customtkinter as ctk

from models.doacao import CATEGORIAS_VALIDAS, formatar_data_br
from services.doacao_service import DoacaoService
from ui.components.dialog import ask_christmas_confirm, show_christmas_dialog
from ui.components.table import StyledTreeviewTable
from ui.theme import (
    COR_BRANCO_NEVE,
    COR_CARD_BRANCO,
    COR_CINZA_CLARO,
    COR_DOURADO,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
    COR_VERDE_ESCURO_HOVER,
    COR_VERDE_PINHEIRO,
    COR_VERMELHO_HOVER,
    COR_VERMELHO_NATAL,
)


class DoacoesScreen(ctk.CTkFrame):
    """Gerencia o CRUD completo de doações com filtros e sincronização de estoque."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        doacao_service: DoacaoService,
        on_data_changed: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color=COR_BRANCO_NEVE)
        self.doacao_service = doacao_service
        self.on_data_changed = on_data_changed
        self.doacao_selecionada_id: int | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._opcoes_rotulo_para_chave = {
            f"{emoji} {rotulo}": chave for chave, (emoji, rotulo) in CATEGORIAS_VALIDAS.items()
        }
        self._chave_para_rotulo = {
            chave: f"{emoji} {rotulo}" for chave, (emoji, rotulo) in CATEGORIAS_VALIDAS.items()
        }

        self._construir_formulario()
        self._construir_barra_busca()
        self._construir_tabela()

    def _construir_formulario(self) -> None:
        form = ctk.CTkFrame(
            self,
            fg_color=COR_CARD_BRANCO,
            corner_radius=12,
            border_width=1,
            border_color=COR_DOURADO,
        )
        form.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        for col in range(4):
            form.grid_columnconfigure(col, weight=1)

        ctk.CTkLabel(
            form,
            text="🎁 Cadastro e Edição de Doações",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_VERDE_PINHEIRO,
        ).grid(row=0, column=0, columnspan=4, padx=16, pady=(12, 8), sticky="w")

        # Linha 1 de campos
        ctk.CTkLabel(form, text="Nome do Doador *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=1, column=0, padx=(16, 6), sticky="w"
        )
        ctk.CTkLabel(form, text="Tipo de Item *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=1, column=1, padx=6, sticky="w"
        )
        ctk.CTkLabel(form, text="Quantidade *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=1, column=2, padx=6, sticky="w"
        )
        ctk.CTkLabel(form, text="Data (DD/MM/AAAA) *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=1, column=3, padx=(6, 16), sticky="w"
        )

        self.entry_doador = ctk.CTkEntry(form, placeholder_text="Ex.: Supermercado Estrela", height=34)
        self.entry_doador.grid(row=2, column=0, padx=(16, 6), pady=(2, 8), sticky="ew")

        self.combo_tipo = ctk.CTkOptionMenu(
            form,
            values=list(self._opcoes_rotulo_para_chave.keys()),
            height=34,
            fg_color=COR_VERDE_PINHEIRO,
            button_color=COR_VERDE_ESCURO_HOVER,
        )
        self.combo_tipo.grid(row=2, column=1, padx=6, pady=(2, 8), sticky="ew")

        self.entry_qtd = ctk.CTkEntry(form, placeholder_text="Ex.: 10", height=34)
        self.entry_qtd.grid(row=2, column=2, padx=6, pady=(2, 8), sticky="ew")

        self.entry_data = ctk.CTkEntry(form, placeholder_text="DD/MM/AAAA", height=34)
        self.entry_data.insert(0, date.today().strftime("%d/%m/%Y"))
        self.entry_data.grid(row=2, column=3, padx=(6, 16), pady=(2, 8), sticky="ew")

        # Linha 2: Descrição multiline + botões
        ctk.CTkLabel(
            form,
            text="Descrição Opcional",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COR_TEXTO_ESCURO,
        ).grid(row=3, column=0, padx=16, sticky="w")

        self.txt_descricao = ctk.CTkTextbox(form, height=58, border_width=1, border_color=COR_CINZA_CLARO)
        self.txt_descricao.grid(row=4, column=0, columnspan=2, padx=(16, 8), pady=(2, 14), sticky="ew")

        botoes = ctk.CTkFrame(form, fg_color="transparent")
        botoes.grid(row=4, column=2, columnspan=2, padx=(8, 16), pady=(2, 14), sticky="sew")

        ctk.CTkButton(
            botoes,
            text="💾 Salvar",
            height=36,
            width=105,
            corner_radius=8,
            fg_color=COR_VERDE_PINHEIRO,
            hover_color=COR_VERDE_ESCURO_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._salvar,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text="✏️ Editar",
            height=36,
            width=105,
            corner_radius=8,
            fg_color="#B08A17",
            hover_color="#8F6E10",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._editar,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            botoes,
            text="🗑️ Excluir",
            height=36,
            width=105,
            corner_radius=8,
            fg_color=COR_VERMELHO_NATAL,
            hover_color=COR_VERMELHO_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._excluir,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            botoes,
            text="Limpar",
            height=36,
            width=90,
            corner_radius=8,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color=COR_TEXTO_ESCURO,
            command=self.limpar_formulario,
        ).pack(side="left", padx=(6, 0))

    def _construir_barra_busca(self) -> None:
        barra = ctk.CTkFrame(
            self,
            fg_color=COR_CARD_BRANCO,
            corner_radius=10,
            border_width=1,
            border_color=COR_CINZA_CLARO,
        )
        barra.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        barra.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            barra,
            text="🔍 Buscar Doador:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
        ).grid(row=0, column=0, padx=(14, 8), pady=10)

        self.entry_busca = ctk.CTkEntry(barra, placeholder_text="Digite o nome do doador...", height=32)
        self.entry_busca.grid(row=0, column=1, padx=6, pady=10, sticky="ew")
        self.entry_busca.bind("<KeyRelease>", lambda _e: self.atualizar_dados())

        opcoes_filtro = ["Todos os tipos"] + list(self._opcoes_rotulo_para_chave.keys())
        self.combo_filtro = ctk.CTkOptionMenu(
            barra,
            values=opcoes_filtro,
            height=32,
            fg_color=COR_VERDE_PINHEIRO,
            command=lambda _v: self.atualizar_dados(),
        )
        self.combo_filtro.grid(row=0, column=2, padx=(6, 14), pady=10)

    def _construir_tabela(self) -> None:
        self.tabela = StyledTreeviewTable(
            self,
            colunas=[
                ("id", "ID", 55),
                ("doador", "Doador", 220),
                ("tipo", "Categoria", 145),
                ("quantidade", "Qtd.", 80),
                ("data", "Data", 105),
                ("descricao", "Descrição", 300),
            ],
            altura=11,
            on_select=self._ao_selecionar_linha,
        )
        self.tabela.grid(row=2, column=0, sticky="nsew")

    def _ao_selecionar_linha(self, valores: tuple[Any, ...]) -> None:
        if not valores:
            return
        doacao_id = int(valores[0])
        self.doacao_selecionada_id = doacao_id
        self.entry_doador.delete(0, "end")
        self.entry_doador.insert(0, str(valores[1]))

        rotulo_tipo = str(valores[2])
        if rotulo_tipo in self._opcoes_rotulo_para_chave:
            self.combo_tipo.set(rotulo_tipo)

        self.entry_qtd.delete(0, "end")
        self.entry_qtd.insert(0, str(valores[3]))

        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, str(valores[4]))

        self.txt_descricao.delete("1.0", "end")
        desc = "" if str(valores[5]) == "—" else str(valores[5])
        self.txt_descricao.insert("1.0", desc)

    def _ler_campos(self) -> tuple[str, str, int, str, str]:
        doador = self.entry_doador.get().strip()
        rotulo = self.combo_tipo.get()
        tipo = self._opcoes_rotulo_para_chave.get(rotulo, "brinquedo")
        qtd_texto = self.entry_qtd.get().strip()
        if not qtd_texto.isdigit():
            raise ValueError("A quantidade deve ser um número inteiro positivo (ex.: 10).")
        quantidade = int(qtd_texto)
        data_str = self.entry_data.get().strip()
        descricao = self.txt_descricao.get("1.0", "end").strip()
        return doador, tipo, quantidade, data_str, descricao

    def _salvar(self) -> None:
        try:
            doador, tipo, quantidade, data_str, descricao = self._ler_campos()
            criada = self.doacao_service.registrar_doacao(doador, tipo, quantidade, data_str, descricao)
            self.limpar_formulario()
            self.on_data_changed()
            show_christmas_dialog(
                self,
                "Doação Registrada!",
                f"Doação de {criada.doador} ({criada.quantidade}x {criada.tipo_rotulo}) salva e adicionada ao estoque.",
                icone="🎁",
            )
        except Exception as exc:
            show_christmas_dialog(self, "Erro ao Salvar Doação", str(exc), icone="⚠️", tipo="erro")

    def _editar(self) -> None:
        if self.doacao_selecionada_id is None:
            show_christmas_dialog(
                self,
                "Selecione uma Doação",
                "Clique em uma linha da tabela abaixo antes de clicar em Editar.",
                icone="🎄",
                tipo="erro",
            )
            return
        try:
            doador, tipo, quantidade, data_str, descricao = self._ler_campos()
            atualizada = self.doacao_service.atualizar_doacao(
                self.doacao_selecionada_id, doador, tipo, quantidade, data_str, descricao
            )
            self.limpar_formulario()
            self.on_data_changed()
            show_christmas_dialog(
                self,
                "Doação Atualizada!",
                f"Registro #{atualizada.id} atualizado e estoque recalculado automaticamente.",
                icone="🎁",
            )
        except Exception as exc:
            show_christmas_dialog(self, "Erro ao Editar Doação", str(exc), icone="⚠️", tipo="erro")

    def _excluir(self) -> None:
        if self.doacao_selecionada_id is None:
            show_christmas_dialog(
                self,
                "Selecione uma Doação",
                "Selecione na tabela a doação que deseja excluir.",
                icone="🎄",
                tipo="erro",
            )
            return
        confirmado = ask_christmas_confirm(
            self,
            "Confirmar Exclusão",
            f"Deseja excluir a doação #{self.doacao_selecionada_id}? O saldo correspondente será estornado do estoque.",
            icone="🗑️",
        )
        if not confirmado:
            return
        try:
            self.doacao_service.excluir_doacao(self.doacao_selecionada_id)
            self.limpar_formulario()
            self.on_data_changed()
            show_christmas_dialog(
                self,
                "Doação Excluída",
                "O registro foi removido e o estoque foi atualizado.",
                icone="🎁",
            )
        except Exception as exc:
            show_christmas_dialog(self, "Não Foi Possível Excluir", str(exc), icone="⚠️", tipo="erro")

    def limpar_formulario(self) -> None:
        """Restaura os campos do formulário para um novo cadastro."""
        self.doacao_selecionada_id = None
        self.entry_doador.delete(0, "end")
        self.combo_tipo.set(self._chave_para_rotulo["brinquedo"])
        self.entry_qtd.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, date.today().strftime("%d/%m/%Y"))
        self.txt_descricao.delete("1.0", "end")

    def atualizar_dados(self) -> None:
        """Recarrega a listagem filtrada de doações na tabela."""
        busca = self.entry_busca.get() if hasattr(self, "entry_busca") else ""
        filtro_rotulo = self.combo_filtro.get() if hasattr(self, "combo_filtro") else "Todos os tipos"
        filtro_tipo = self._opcoes_rotulo_para_chave.get(filtro_rotulo, "todos")

        doacoes = self.doacao_service.listar_doacoes(filtro_doador=busca, filtro_tipo=filtro_tipo)
        linhas = [
            (
                d.id,
                d.doador,
                f"{d.emoji} {d.tipo_rotulo}",
                d.quantidade,
                formatar_data_br(d.data_doacao),
                d.descricao or "—",
            )
            for d in doacoes
        ]
        self.tabela.atualizar_linhas(linhas)
