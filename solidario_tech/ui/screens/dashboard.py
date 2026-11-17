"""Tela Inicial (Dashboard) Vermelho Natalino 3D com renas voando, pisca-pisca e últimas 5 doações."""

from __future__ import annotations

import tkinter as tk
import customtkinter as ctk

from models.doacao import formatar_data_br
from services.distribuicao_service import DistribuicaoService
from services.doacao_service import DoacaoService
from ui.components.card import KPICard, PiscaPiscaStrip
from ui.components.table import StyledTreeviewTable
from ui.theme import (
    COR_BRANCO_NEVE,
    COR_DOURADO,
    COR_OURO_CLARO,
    COR_TEXTO_ESCURO,
    COR_TEXTO_SUAVE,
    COR_VERDE_ESCURO_HOVER,
    COR_VERDE_PINHEIRO,
    FRASES_SOLIDARIEDADE,
)


class RenasVoandoCanvas(tk.Canvas):
    """Faixa animada com Papai Noel e 3 renas voando sobre céu vermelho natalino."""

    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master, height=44, bg="#4A070B", highlightthickness=0, bd=0)
        self.pos_x = -240.0
        self.itens_grupo: list[int] = []
        self._desenhar_cenario()
        self._animar()

    def _desenhar_cenario(self) -> None:
        # Pequenas estrelas douradas
        for sx, sy in [(45, 10), (140, 16), (260, 8), (390, 15), (520, 9), (660, 14), (790, 10), (920, 15)]:
            self.create_oval(sx, sy, sx + 3, sy + 3, fill="#FDE047", outline="")

    def _desenhar_treno(self, x: float) -> None:
        for item_id in self.itens_grupo:
            self.delete(item_id)
        self.itens_grupo.clear()

        # Trenó 3D vermelho & ouro
        self.itens_grupo.append(
            self.create_line(x + 8, 34, x + 52, 34, fill="#F5C451", width=2.5)
        )
        self.itens_grupo.append(
            self.create_polygon(
                x + 10, 20, x + 46, 20, x + 42, 31, x + 14, 31,
                fill="#EF4444", outline="#FDE047", width=1.2,
            )
        )
        # Papai Noel
        self.itens_grupo.append(self.create_oval(x + 28, 12, x + 36, 20, fill="#FFE0BD", outline=""))
        self.itens_grupo.append(self.create_polygon(x + 28, 13, x + 32, 6, x + 36, 13, fill="#DC2626"))
        # Rédeas douradas
        self.itens_grupo.append(self.create_line(x + 46, 23, x + 146, 21, fill="#FDE047", width=1.2, dash=(3, 2)))

        # 3 reninhas voando
        for idx, offset in enumerate([72, 106, 140]):
            rx = x + offset
            ry = 20 - idx * 1.5
            self.itens_grupo.append(self.create_oval(rx, ry, rx + 18, ry + 10, fill="#B46234", outline="#7C3F1D"))
            self.itens_grupo.append(self.create_oval(rx + 14, ry - 5, rx + 22, ry + 3, fill="#C77342", outline=""))
            self.itens_grupo.append(self.create_line(rx + 17, ry - 5, rx + 15, ry - 10, fill="#FDE047", width=1.2))
            self.itens_grupo.append(self.create_line(rx + 20, ry - 5, rx + 22, ry - 10, fill="#FDE047", width=1.2))
            if idx == 2:
                # Nariz brilhante do Rudolph
                self.itens_grupo.append(self.create_oval(rx + 21, ry - 2, rx + 25, ry + 2, fill="#FF2E4D", outline=""))

    def _animar(self) -> None:
        largura = max(self.winfo_width(), 780)
        self.pos_x += 2.6
        if self.pos_x > largura + 40:
            self.pos_x = -200.0
        self._desenhar_treno(self.pos_x)
        self.after(36, self._animar)


class DashboardScreen(ctk.CTkFrame):
    """Exibe indicadores 3D coloridos, banner com renas voando, pisca-pisca e últimas doações."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        doacao_service: DoacaoService,
        distribuicao_service: DistribuicaoService,
    ) -> None:
        super().__init__(master, fg_color=COR_BRANCO_NEVE)
        self.doacao_service = doacao_service
        self.distribuicao_service = distribuicao_service
        self.frase_index = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Banner Vermelho Natalino 3D com pisca-pisca e faixa de renas voando
        banner = ctk.CTkFrame(
            self,
            fg_color="#8C141D",
            corner_radius=16,
            border_width=2,
            border_color=COR_DOURADO,
        )
        banner.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        banner.grid_columnconfigure(0, weight=1)

        PiscaPiscaStrip(banner, qtd_lampadas=14, bg_color="#8C141D").grid(
            row=0, column=0, columnspan=2, padx=10, pady=(6, 0), sticky="ew"
        )

        self.renas_canvas = RenasVoandoCanvas(banner)
        self.renas_canvas.grid(row=1, column=0, columnspan=2, padx=14, pady=(2, 4), sticky="ew")

        ctk.CTkLabel(
            banner,
            text="🎄 Feliz Natal! Que a solidariedade transforme vidas.",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFF9F0",
            anchor="w",
        ).grid(row=2, column=0, padx=20, pady=(6, 4), sticky="w")

        self.lbl_frase = ctk.CTkLabel(
            banner,
            text=f"⭐ \"{FRASES_SOLIDARIEDADE[0]}\"",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color=COR_TEXTO_SUAVE,
            anchor="w",
        )
        self.lbl_frase.grid(row=3, column=0, padx=20, pady=(0, 14), sticky="w")

        progresso_box = ctk.CTkFrame(
            banner,
            fg_color="#4E080D",
            corner_radius=12,
            border_width=2,
            border_color=COR_DOURADO,
        )
        progresso_box.grid(row=2, column=1, rowspan=2, padx=20, pady=10, sticky="e")

        self.lbl_progresso = ctk.CTkLabel(
            progresso_box,
            text="🎅 Campanha Solidária Ativa",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COR_OURO_CLARO,
        )
        self.lbl_progresso.pack(padx=14, pady=10)

        # Cards 3D super coloridos de Resumo (KPIs) com pisca-pisca
        cards_row = ctk.CTkFrame(self, fg_color="transparent")
        cards_row.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        for col in range(3):
            cards_row.grid_columnconfigure(col, weight=1)

        self.card_doado = KPICard(
            cards_row,
            titulo="🎁 Total de Doações Recebidas",
            valor="0",
            subtitulo="Soma acumulada na campanha",
            cor_destaque="#FFFFFF",
            cor_fundo="#127053",
            cor_borda="#34D399",
        )
        self.card_doado.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.card_distribuido = KPICard(
            cards_row,
            titulo="⭐ Total Distribuído",
            valor="0",
            subtitulo="Itens entregues às famílias",
            cor_destaque="#FFFFFF",
            cor_fundo="#C82333",
            cor_borda="#FDA4AF",
        )
        self.card_distribuido.grid(row=0, column=1, sticky="ew", padx=4)

        self.card_estoque = KPICard(
            cards_row,
            titulo="🎄 Itens em Estoque",
            valor="0",
            subtitulo="Prontos para distribuição",
            cor_destaque="#FFFFFF",
            cor_fundo="#B45309",
            cor_borda="#FDE047",
        )
        self.card_estoque.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        # Cabeçalho da mini-tabela
        sec_header = ctk.CTkFrame(self, fg_color="transparent")
        sec_header.grid(row=2, column=0, sticky="ew", pady=(4, 6))
        sec_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            sec_header,
            text="🎁 Últimos 5 Registros de Doação",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COR_OURO_CLARO,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            sec_header,
            text="Atualizar",
            width=105,
            height=32,
            corner_radius=8,
            fg_color=COR_VERDE_PINHEIRO,
            hover_color=COR_VERDE_ESCURO_HOVER,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.atualizar_dados,
        ).grid(row=0, column=1, sticky="e")

        self.tabela = StyledTreeviewTable(
            self,
            colunas=[
                ("id", "ID", 60),
                ("doador", "Doador", 240),
                ("tipo", "Categoria", 150),
                ("quantidade", "Qtd.", 90),
                ("data", "Data", 110),
                ("descricao", "Descrição", 260),
            ],
            altura=8,
        )
        self.tabela.grid(row=3, column=0, sticky="nsew")

        self._agendar_rotacao_frase()

    def _agendar_rotacao_frase(self) -> None:
        """Alterna automaticamente a frase motivacional natalina a cada 8 segundos."""
        self.frase_index = (self.frase_index + 1) % len(FRASES_SOLIDARIEDADE)
        self.lbl_frase.configure(text=f"⭐ \"{FRASES_SOLIDARIEDADE[self.frase_index]}\"")
        self.after(8000, self._agendar_rotacao_frase)

    def atualizar_dados(self) -> None:
        """Recarrega os indicadores e as últimas 5 doações do SQLite."""
        total_doado = self.doacao_service.obter_total_doado()
        total_dist = self.distribuicao_service.obter_total_distribuido()
        total_est = self.distribuicao_service.obter_total_em_estoque()

        taxa = round((total_dist / total_doado) * 100, 1) if total_doado > 0 else 0.0
        self.lbl_progresso.configure(text=f"🎅 {taxa}% dos itens já entregues")

        self.card_doado.atualizar_valor(f"{total_doado}")
        self.card_distribuido.atualizar_valor(f"{total_dist}")

        estoque_itens = self.distribuicao_service.listar_estoque()
        baixos = sum(1 for item in estoque_itens if item.esta_baixo())
        sub_est = (
            f"⚠️ {baixos} categoria(s) abaixo de 5 un."
            if baixos > 0
            else "Todas as categorias em nível seguro"
        )
        self.card_estoque.atualizar_valor(f"{total_est}", sub_est)

        ultimas = self.doacao_service.obter_ultimas_doacoes(limite=5)
        linhas = [
            (
                d.id,
                d.doador,
                f"{d.emoji} {d.tipo_rotulo}",
                d.quantidade,
                formatar_data_br(d.data_doacao),
                d.descricao or "—",
            )
            for d in ultimas
        ]
        self.tabela.atualizar_linhas(linhas)
