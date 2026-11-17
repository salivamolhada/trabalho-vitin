"""Serviço de Ciência de Dados e geração de gráficos natalinos coloridos (Pandas + Matplotlib + Seaborn)."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from database.connection import DatabaseConnection
from models.doacao import CATEGORIAS_VALIDAS

PALETA_3D_NATAL = ["#34D399", "#FB7185", "#60A5FA", "#FBBF24", "#C084FC"]
COR_FUNDO_FIGURA = "#560B10"
COR_FUNDO_EIXO = "#3E060A"


class RelatorioService:
    """Executa agregações analíticas com Pandas e desenha gráficos em figuras Matplotlib."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db
        sns.set_theme(style="darkgrid")

    def obter_dataframe_doacoes(self) -> pd.DataFrame:
        """Carrega todas as doações em um DataFrame Pandas tipado."""
        with self.db.connect() as conn:
            df = pd.read_sql_query("SELECT * FROM doacoes", conn)
        if df.empty:
            return pd.DataFrame(
                columns=["id", "doador", "tipo", "quantidade", "data_doacao", "descricao"]
            )
        df["data_dt"] = pd.to_datetime(df["data_doacao"], errors="coerce")
        df["rotulo"] = df["tipo"].map(lambda t: CATEGORIAS_VALIDAS.get(t, ("", t))[1])
        return df

    def obter_dataframe_distribuicoes(self) -> pd.DataFrame:
        """Carrega todas as distribuições em um DataFrame Pandas."""
        with self.db.connect() as conn:
            df = pd.read_sql_query("SELECT * FROM distribuicoes", conn)
        if df.empty:
            return pd.DataFrame(
                columns=["id", "doacao_id", "item_tipo", "quantidade", "beneficiario", "data_entrega", "responsavel"]
            )
        df["data_dt"] = pd.to_datetime(df["data_entrega"], errors="coerce")
        return df

    def obter_kpis(self) -> dict[str, Any]:
        """Calcula indicadores consolidados: arrecadado vs. distribuído e estoque."""
        with self.db.connect() as conn:
            total_arrecadado = int(
                conn.execute("SELECT COALESCE(SUM(quantidade), 0) FROM doacoes").fetchone()[0]
            )
            total_distribuido = int(
                conn.execute("SELECT COALESCE(SUM(quantidade), 0) FROM distribuicoes").fetchone()[0]
            )
            total_estoque = int(
                conn.execute("SELECT COALESCE(SUM(quantidade_disponivel), 0) FROM estoque").fetchone()[0]
            )
            qtd_registros_doacoes = int(
                conn.execute("SELECT COUNT(*) FROM doacoes").fetchone()[0]
            )
            qtd_entregas = int(
                conn.execute("SELECT COUNT(*) FROM distribuicoes").fetchone()[0]
            )

        taxa_distribuicao = (
            round((total_distribuido / total_arrecadado) * 100, 1)
            if total_arrecadado > 0
            else 0.0
        )
        return {
            "total_arrecadado": total_arrecadado,
            "total_distribuido": total_distribuido,
            "total_estoque": total_estoque,
            "taxa_distribuicao": taxa_distribuicao,
            "qtd_registros_doacoes": qtd_registros_doacoes,
            "qtd_entregas": qtd_entregas,
        }

    def gerar_grafico_barras(self, fig: Figure) -> None:
        """Desenha gráfico de barras colorido com total de doações recebidas por categoria."""
        fig.clear()
        ax = fig.add_subplot(111)
        df = self.obter_dataframe_doacoes()

        if df.empty:
            self._desenhar_estado_vazio(ax, fig, "Sem doações registradas para exibir barras.")
            fig.tight_layout()
            return

        agrupado = (
            df.groupby("rotulo", as_index=False)["quantidade"]
            .sum()
            .sort_values("quantidade", ascending=False)
        )

        cores = PALETA_3D_NATAL[: len(agrupado)]
        sns.barplot(
            data=agrupado,
            x="rotulo",
            y="quantidade",
            hue="rotulo",
            palette=cores,
            legend=False,
            ax=ax,
        )
        for patch in ax.patches:
            altura = patch.get_height()
            ax.annotate(
                f"{int(altura)}",
                (patch.get_x() + patch.get_width() / 2.0, altura),
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#FDE047",
                xytext=(0, 3),
                textcoords="offset points",
            )

        ax.set_title("Doações Recebidas por Tipo de Item", fontsize=11, fontweight="bold", color="#FDE047", pad=12)
        ax.set_xlabel("")
        ax.set_ylabel("Quantidade", fontsize=9, color="#FFE9B3")
        ax.tick_params(axis="x", labelsize=9, colors="#FFF9F0")
        ax.tick_params(axis="y", labelsize=9, colors="#FFE9B3")
        ax.grid(color="#FFFFFF", alpha=0.14)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#F5C451")
        ax.spines["bottom"].set_color("#F5C451")
        fig.patch.set_facecolor(COR_FUNDO_FIGURA)
        ax.set_facecolor(COR_FUNDO_EIXO)
        fig.tight_layout()

    def gerar_grafico_pizza(self, fig: Figure) -> None:
        """Desenha gráfico de pizza colorido com participação percentual de cada categoria."""
        fig.clear()
        ax = fig.add_subplot(111)
        df = self.obter_dataframe_doacoes()

        if df.empty:
            self._desenhar_estado_vazio(ax, fig, "Sem dados para distribuição percentual.")
            fig.tight_layout()
            return

        agrupado = df.groupby("rotulo")["quantidade"].sum()
        cores = PALETA_3D_NATAL[: len(agrupado)]

        _wedges, texts, autotexts = ax.pie(
            agrupado.values,
            labels=agrupado.index,
            autopct="%1.1f%%",
            startangle=120,
            colors=cores,
            pctdistance=0.75,
            wedgeprops={"edgecolor": COR_FUNDO_FIGURA, "linewidth": 2},
        )
        for text in texts:
            text.set_fontsize(9)
            text.set_color("#FFF9F0")
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_fontweight("bold")
            autotext.set_color("#1B0507")

        ax.set_title("Distribuição Percentual por Categoria", fontsize=11, fontweight="bold", color="#FDE047", pad=10)
        fig.patch.set_facecolor(COR_FUNDO_FIGURA)
        fig.tight_layout()

    def gerar_grafico_linha_30_dias(self, fig: Figure) -> None:
        """Desenha série temporal dos últimos 30 dias usando Pandas + Matplotlib."""
        fig.clear()
        ax = fig.add_subplot(111)
        df = self.obter_dataframe_doacoes()

        if df.empty or df["data_dt"].dropna().empty:
            self._desenhar_estado_vazio(ax, fig, "Sem histórico temporal nos últimos 30 dias.")
            fig.tight_layout()
            return

        referencia = max(df["data_dt"].max().normalize(), pd.Timestamp(datetime.now().date()))
        inicio = referencia - timedelta(days=29)
        calendario = pd.date_range(start=inicio, end=referencia, freq="D")

        diario = (
            df.dropna(subset=["data_dt"])
            .groupby(df["data_dt"].dt.normalize())["quantidade"]
            .sum()
            .reindex(calendario, fill_value=0)
        )

        ax.plot(
            diario.index,
            diario.values,
            color="#FDE047",
            linewidth=2.4,
            marker="o",
            markersize=4.5,
            markerfacecolor="#34D399",
            markeredgecolor="#FFF9F0",
        )
        ax.fill_between(diario.index, diario.values, color="#34D399", alpha=0.18)

        ax.set_title("Evolução das Doações (Últimos 30 Dias)", fontsize=11, fontweight="bold", color="#FDE047", pad=12)
        ax.set_ylabel("Itens / Dia", fontsize=9, color="#FFE9B3")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.tick_params(axis="x", labelsize=8, colors="#FFF9F0")
        ax.tick_params(axis="y", labelsize=8, colors="#FFE9B3")
        ax.grid(color="#FFFFFF", alpha=0.14)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#F5C451")
        ax.spines["bottom"].set_color("#F5C451")
        fig.patch.set_facecolor(COR_FUNDO_FIGURA)
        ax.set_facecolor(COR_FUNDO_EIXO)
        fig.tight_layout()

    def gerar_grafico_comparativo_kpi(self, fig: Figure) -> None:
        """Desenha comparativo direto entre Total Arrecadado, Distribuído e Estoque."""
        fig.clear()
        ax = fig.add_subplot(111)
        kpis = self.obter_kpis()

        categorias = ["Arrecadado", "Distribuído", "Em Estoque"]
        valores = [
            kpis["total_arrecadado"],
            kpis["total_distribuido"],
            kpis["total_estoque"],
        ]
        cores = ["#34D399", "#FB7185", "#FBBF24"]

        bars = ax.barh(categorias, valores, color=cores, height=0.52)
        for bar in bars:
            largura = bar.get_width()
            ax.annotate(
                f"{int(largura)}",
                (largura, bar.get_y() + bar.get_height() / 2),
                ha="left",
                va="center",
                xytext=(5, 0),
                textcoords="offset points",
                fontsize=9,
                fontweight="bold",
                color="#FFF9F0",
            )

        ax.set_title(
            f"Balanço Geral (Taxa de Entrega: {kpis['taxa_distribuicao']}%)",
            fontsize=11,
            fontweight="bold",
            color="#FDE047",
            pad=12,
        )
        ax.set_xlim(0, max(valores + [10]) * 1.18)
        ax.tick_params(axis="x", labelsize=9, colors="#FFE9B3")
        ax.tick_params(axis="y", labelsize=9, colors="#FFF9F0")
        ax.grid(color="#FFFFFF", alpha=0.14)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#F5C451")
        ax.spines["bottom"].set_color("#F5C451")
        fig.patch.set_facecolor(COR_FUNDO_FIGURA)
        ax.set_facecolor(COR_FUNDO_EIXO)
        fig.tight_layout()

    @staticmethod
    def _desenhar_estado_vazio(ax: Any, fig: Figure, mensagem: str) -> None:
        fig.patch.set_facecolor(COR_FUNDO_FIGURA)
        ax.set_facecolor(COR_FUNDO_EIXO)
        ax.text(0.5, 0.5, mensagem, ha="center", va="center", fontsize=10, color="#FFE9B3")
        ax.set_axis_off()
