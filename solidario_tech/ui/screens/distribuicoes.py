"""Tela de Registro de Distribuição com bloqueio automático acima do estoque."""

from __future__ import annotations

from datetime import date
from typing import Callable

import customtkinter as ctk

from models.doacao import CATEGORIAS_VALIDAS, formatar_data_br
from services.distribuicao_service import DistribuicaoService
from ui.components.dialog import show_christmas_dialog
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


class DistribuicoesScreen(ctk.CTkFrame):
    """Permite registrar entregas às famílias/instituições e pesquisar o histórico."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        distribuicao_service: DistribuicaoService,
        on_data_changed: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color=COR_BRANCO_NEVE)
        self.distribuicao_service = distribuicao_service
        self.on_data_changed = on_data_changed
        self._label_para_tipo: dict[str, str] = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._construir_formulario()
        self._construir_busca()
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
        for col in range(3):
            form.grid_columnconfigure(col, weight=1)

        ctk.CTkLabel(
            form,
            text="⭐ Registrar Entrega / Distribuição Solidária",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_VERDE_PINHEIRO,
        ).grid(row=0, column=0, columnspan=3, padx=16, pady=(12, 8), sticky="w")

        ctk.CTkLabel(form, text="Item do Estoque *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=1, column=0, padx=(16, 6), sticky="w"
        )
        ctk.CTkLabel(form, text="Quantidade a Distribuir *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=1, column=1, padx=6, sticky="w"
        )
        ctk.CTkLabel(form, text="Data da Entrega (DD/MM/AAAA) *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=1, column=2, padx=(6, 16), sticky="w"
        )

        self.combo_item = ctk.CTkOptionMenu(
            form,
            values=["Carregando estoque..."],
            height=34,
            fg_color=COR_VERDE_PINHEIRO,
            button_color=COR_VERDE_ESCURO_HOVER,
        )
        self.combo_item.grid(row=2, column=0, padx=(16, 6), pady=(2, 8), sticky="ew")

        self.entry_qtd = ctk.CTkEntry(form, placeholder_text="Ex.: 5", height=34)
        self.entry_qtd.grid(row=2, column=1, padx=6, pady=(2, 8), sticky="ew")

        self.entry_data = ctk.CTkEntry(form, placeholder_text="DD/MM/AAAA", height=34)
        self.entry_data.insert(0, date.today().strftime("%d/%m/%Y"))
        self.entry_data.grid(row=2, column=2, padx=(6, 16), pady=(2, 8), sticky="ew")

        ctk.CTkLabel(form, text="Nome do Beneficiário *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=3, column=0, padx=(16, 6), sticky="w"
        )
        ctk.CTkLabel(form, text="Responsável pela Entrega *", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_ESCURO).grid(
            row=3, column=1, padx=6, sticky="w"
        )

        self.entry_beneficiario = ctk.CTkEntry(form, placeholder_text="Ex.: Família Silva / Abrigo Lar Feliz", height=34)
        self.entry_beneficiario.grid(row=4, column=0, padx=(16, 6), pady=(2, 14), sticky="ew")

        self.entry_responsavel = ctk.CTkEntry(form, placeholder_text="Ex.: Mariana Costa", height=34)
        self.entry_responsavel.grid(row=4, column=1, padx=6, pady=(2, 14), sticky="ew")

        ctk.CTkButton(
            form,
            text="⭐ Confirmar Distribuição",
            height=36,
            corner_radius=8,
            fg_color=COR_VERMELHO_NATAL,
            hover_color=COR_VERMELHO_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._registrar,
        ).grid(row=4, column=2, padx=(6, 16), pady=(2, 14), sticky="ew")

    def _construir_busca(self) -> None:
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
            text="🔍 Buscar Beneficiário:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
        ).grid(row=0, column=0, padx=(14, 8), pady=10)

        self.entry_busca = ctk.CTkEntry(barra, placeholder_text="Digite o nome do beneficiário...", height=32)
        self.entry_busca.grid(row=0, column=1, padx=(6, 14), pady=10, sticky="ew")
        self.entry_busca.bind("<KeyRelease>", lambda _e: self.atualizar_dados())

    def _construir_tabela(self) -> None:
        self.tabela = StyledTreeviewTable(
            self,
            colunas=[
                ("id", "ID", 55),
                ("item", "Item", 150),
                ("quantidade", "Qtd.", 80),
                ("beneficiario", "Beneficiário", 250),
                ("data", "Data Entrega", 115),
                ("responsavel", "Responsável", 200),
            ],
            altura=11,
        )
        self.tabela.grid(row=2, column=0, sticky="nsew")

    def _registrar(self) -> None:
        try:
            rotulo = self.combo_item.get()
            item_tipo = self._label_para_tipo.get(rotulo, "brinquedo")

            qtd_texto = self.entry_qtd.get().strip()
            if not qtd_texto.isdigit():
                raise ValueError("Informe uma quantidade inteira positiva para distribuir.")
            quantidade = int(qtd_texto)

            beneficiario = self.entry_beneficiario.get().strip()
            data_entrega = self.entry_data.get().strip()
            responsavel = self.entry_responsavel.get().strip()

            criada = self.distribuicao_service.registrar_distribuicao(
                item_tipo=item_tipo,
                quantidade=quantidade,
                beneficiario=beneficiario,
                data_entrega=data_entrega,
                responsavel=responsavel,
            )

            self.entry_qtd.delete(0, "end")
            self.entry_beneficiario.delete(0, "end")
            self.entry_responsavel.delete(0, "end")
            self.on_data_changed()

            show_christmas_dialog(
                self,
                "Entrega Registrada!",
                f"{criada.quantidade}x {criada.item_rotulo} entregues para {criada.beneficiario}. Estoque atualizado!",
                icone="⭐",
            )
        except Exception as exc:
            show_christmas_dialog(self, "Distribuição Bloqueada", str(exc), icone="⚠️", tipo="erro")

    def atualizar_dados(self) -> None:
        """Atualiza o dropdown com os saldos do estoque e recarrega o histórico."""
        estoque_lista = self.distribuicao_service.listar_estoque()
        self._label_para_tipo.clear()
        opcoes = []
        for item in estoque_lista:
            label = f"{item.emoji} {item.nome_exibicao} ({item.quantidade_disponivel} disp.)"
            self._label_para_tipo[label] = item.tipo
            opcoes.append(label)

        if opcoes:
            atual = self.combo_item.get()
            tipo_atual = self._label_para_tipo.get(atual)
            self.combo_item.configure(values=opcoes)
            if tipo_atual and any(self._label_para_tipo[o] == tipo_atual for o in opcoes):
                matching = next(o for o in opcoes if self._label_para_tipo[o] == tipo_atual)
                self.combo_item.set(matching)
            else:
                self.combo_item.set(opcoes[0])

        busca = self.entry_busca.get() if hasattr(self, "entry_busca") else ""
        registros = self.distribuicao_service.listar_distribuicoes(filtro_beneficiario=busca)
        linhas = [
            (
                d.id,
                f"{CATEGORIAS_VALIDAS.get(d.item_tipo, ('⭐', d.item_tipo))[0]} {d.item_rotulo}",
                d.quantidade,
                d.beneficiario,
                formatar_data_br(d.data_entrega),
                d.responsavel,
            )
            for d in registros
        ]
        self.tabela.atualizar_linhas(linhas)
