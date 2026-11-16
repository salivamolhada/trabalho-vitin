"""Janela principal e navegação lateral (sidebar) Natal Branco do Solidário Tech."""

from __future__ import annotations

import customtkinter as ctk
from PIL import ImageTk

from database.connection import DatabaseConnection
from services.distribuicao_service import DistribuicaoService
from services.doacao_service import DoacaoService
from services.relatorio_service import RelatorioService
from ui.components.card import PiscaPiscaStrip
from ui.screens.dashboard import DashboardScreen
from ui.screens.distribuicoes import DistribuicoesScreen
from ui.screens.doacoes import DoacoesScreen
from ui.screens.estoque import EstoqueScreen
from ui.screens.graficos import GraficosScreen
from ui.screens.sobre import SobreScreen
from ui.theme import (
    COR_BRANCO_NEVE,
    COR_CARD_BRANCO,
    COR_CINZA_CLARO,
    COR_DOURADO,
    COR_SIDEBAR_BRANCO,
    COR_SIDEBAR_HOVER,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
    COR_VERDE_PINHEIRO,
    carregar_imagem_logo,
    formatar_data_atual_pt,
)


class SolidarioTechApp(ctk.CTk):
    """Aplicação principal CustomTkinter com tema Natal Branco e pisca-pisca."""

    def __init__(self, db: DatabaseConnection) -> None:
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.db = db
        self.doacao_service = DoacaoService(db)
        self.distribuicao_service = DistribuicaoService(db)
        self.relatorio_service = RelatorioService(db)

        self.title("Solidário Tech — Natal Branco · Sistema de Doações")
        self.geometry("1220x760")
        self.minsize(1100, 700)
        self.configure(fg_color=COR_BRANCO_NEVE)

        try:
            pil_icon = carregar_imagem_logo((64, 64))
            self._tk_icon = ImageTk.PhotoImage(pil_icon)
            self.iconphoto(False, self._tk_icon)
        except Exception:
            pass

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.botoes_nav: dict[str, ctk.CTkButton] = {}
        self.telas: dict[str, ctk.CTkFrame] = {}
        self.titulos_telas: dict[str, str] = {
            "dashboard": "🎄 Painel Inicial — Natal Branco",
            "doacoes": "🎁 Cadastro e Gestão de Doações",
            "estoque": "🧺 Controle de Itens Disponíveis",
            "distribuicoes": "⭐ Registro de Distribuição Solidária",
            "graficos": "📊 Relatórios e Gráficos Analíticos",
            "sobre": "🦌 Sobre o Solidário Tech",
        }

        self._construir_sidebar()
        self._construir_area_principal()
        self.navegar_para("dashboard")

    def _construir_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(
            self,
            width=250,
            fg_color=COR_SIDEBAR_BRANCO,
            corner_radius=0,
            border_width=1,
            border_color=COR_CINZA_CLARO,
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(9, weight=1)

        logo_box = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_box.grid(row=0, column=0, padx=18, pady=(20, 8), sticky="ew")

        pil_logo = carregar_imagem_logo((44, 44))
        self.ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(44, 44))
        ctk.CTkLabel(logo_box, image=self.ctk_logo, text="").pack(side="left", padx=(0, 10))

        titulo_box = ctk.CTkFrame(logo_box, fg_color="transparent")
        titulo_box.pack(side="left", fill="x")
        ctk.CTkLabel(
            titulo_box,
            text="Solidário Tech",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COR_VERDE_PINHEIRO,
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            titulo_box,
            text="Natal Branco 2026",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#9A7B16",
            anchor="w",
        ).pack(anchor="w")

        PiscaPiscaStrip(sidebar, qtd_lampadas=7, bg_color=COR_SIDEBAR_BRANCO).grid(
            row=1, column=0, padx=12, pady=(2, 10), sticky="ew"
        )

        itens_menu = [
            ("dashboard", "🎄  Dashboard"),
            ("doacoes", "🎁  Doações"),
            ("estoque", "🧺  Estoque"),
            ("distribuicoes", "⭐  Distribuições"),
            ("graficos", "📊  Gráficos"),
            ("sobre", "🎅  Sobre"),
        ]

        for idx, (chave, rotulo) in enumerate(itens_menu, start=2):
            btn = ctk.CTkButton(
                sidebar,
                text=rotulo,
                height=42,
                corner_radius=10,
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="transparent",
                hover_color=COR_SIDEBAR_HOVER,
                text_color=COR_TEXTO_ESCURO,
                command=lambda c=chave: self.navegar_para(c),
            )
            btn.grid(row=idx, column=0, padx=14, pady=4, sticky="ew")
            self.botoes_nav[chave] = btn

        rodape = ctk.CTkFrame(
            sidebar,
            fg_color=COR_BRANCO_NEVE,
            corner_radius=10,
            border_width=1,
            border_color=COR_DOURADO,
        )
        rodape.grid(row=10, column=0, padx=14, pady=16, sticky="ew")
        ctk.CTkLabel(
            rodape,
            text="Desafio Tech Solutions 2026\n3º A • Desenv. de Sistemas",
            font=ctk.CTkFont(size=11),
            text_color=COR_TEXTO_SUAVE,
            justify="center",
        ).pack(padx=10, pady=10)

    def _construir_area_principal(self) -> None:
        main_area = ctk.CTkFrame(self, fg_color=COR_BRANCO_NEVE, corner_radius=0)
        main_area.grid(row=0, column=1, sticky="nsew")
        main_area.grid_columnconfigure(0, weight=1)
        main_area.grid_rowconfigure(1, weight=1)

        topbar = ctk.CTkFrame(
            main_area,
            fg_color=COR_CARD_BRANCO,
            corner_radius=0,
            border_width=1,
            border_color=COR_CINZA_CLARO,
        )
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_columnconfigure(0, weight=1)

        PiscaPiscaStrip(topbar, qtd_lampadas=18, bg_color=COR_CARD_BRANCO).grid(
            row=0, column=0, columnspan=2, padx=10, pady=(4, 0), sticky="ew"
        )

        self.lbl_titulo_tela = ctk.CTkLabel(
            topbar,
            text="Dashboard",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=COR_VERDE_PINHEIRO,
            anchor="w",
        )
        self.lbl_titulo_tela.grid(row=1, column=0, padx=22, pady=(6, 12), sticky="w")

        ctk.CTkLabel(
            topbar,
            text=f"📅 {formatar_data_atual_pt()}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COR_TEXTO_SUAVE,
            anchor="e",
        ).grid(row=1, column=1, padx=22, pady=(6, 12), sticky="e")

        self.content_container = ctk.CTkFrame(main_area, fg_color=COR_BRANCO_NEVE)
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=18)
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.telas = {
            "dashboard": DashboardScreen(
                self.content_container, self.doacao_service, self.distribuicao_service
            ),
            "doacoes": DoacoesScreen(
                self.content_container, self.doacao_service, self.atualizar_todas_telas
            ),
            "estoque": EstoqueScreen(
                self.content_container, self.distribuicao_service, self.atualizar_todas_telas
            ),
            "distribuicoes": DistribuicoesScreen(
                self.content_container, self.distribuicao_service, self.atualizar_todas_telas
            ),
            "graficos": GraficosScreen(self.content_container, self.relatorio_service),
            "sobre": SobreScreen(self.content_container),
        }

        for frame in self.telas.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def navegar_para(self, nome_tela: str) -> None:
        """Alterna o frame visível na área central e atualiza o estado da navegação."""
        for chave, botao in self.botoes_nav.items():
            ativo = chave == nome_tela
            botao.configure(
                fg_color=COR_VERDE_PINHEIRO if ativo else "transparent",
                text_color="#FFFFFF" if ativo else COR_TEXTO_ESCURO,
            )

        self.lbl_titulo_tela.configure(text=self.titulos_telas.get(nome_tela, "Solidário Tech"))
        tela = self.telas[nome_tela]
        if hasattr(tela, "atualizar_dados"):
            tela.atualizar_dados()
        tela.tkraise()

    def atualizar_todas_telas(self) -> None:
        """Sincroniza todas as telas após alterações em doações, estoque ou distribuições."""
        for tela in self.telas.values():
            if hasattr(tela, "atualizar_dados"):
                tela.atualizar_dados()
