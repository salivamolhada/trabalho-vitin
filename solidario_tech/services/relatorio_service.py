"""Serviço de Ciência de Dados e geração de gráficos natalinos (Pandas + Matplotlib + Seaborn)."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from database.connection import DatabaseConnection
from models.doacao import CATEGORIAS_VALIDAS

PALETA_NATAL = ["#0B3D2E", "#C1272D", "#D4AF37", "#1F6E56", "#8E1B20"]


class RelatorioService:
    """Executa agregações analíticas com Pandas e desenha gráficos em figuras Matplotlib."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db
        sns.set_theme(style="whitegrid")

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
        """Desenha gráfico de barras com total de doações recebidas por categoria."""
        fig.clear()
        ax = fig.add_subplot(111)
        df = self.obter_dataframe_doacoes()

        if df.empty:
            self._desenhar_estado_vazio(ax, "Sem doações registradas para exibir barras.")
            fig.tight_layout()
            return

        agrupado = (
            df.groupby("rotulo", as_index=False)["quantidade"]
            .sum()
            .sort_values("quantidade", ascending=False)
        )

        cores = PALETA_NATAL[: len(agrupado)]
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
                color="#0B3D2E",
                xytext=(0, 3),
                textcoords="offset points",
            )

        ax.set_title("Doações Recebidas por Tipo de Item", fontsize=11, fontweight="bold", color="#0B3D2E", pad=12)
        ax.set_xlabel("")
        ax.set_ylabel("Quantidade", fontsize=9, color="#334155")
        ax.tick_params(axis="x", labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FAFAFA")
        fig.tight_layout()

    def gerar_grafico_pizza(self, fig: Figure) -> None:
        """Desenha gráfico de pizza com participação percentual de cada categoria."""
        fig.clear()
        ax = fig.add_subplot(111)
        df = self.obter_dataframe_doacoes()

        if df.empty:
            self._desenhar_estado_vazio(ax, "Sem dados para distribuição percentual.")
            fig.tight_layout()
            return

        agrupado = df.groupby("rotulo")["quantidade"].sum()
        cores = PALETA_NATAL[: len(agrupado)]

        wedges, texts, autotexts = ax.pie(
            agrupado.values,
            labels=agrupado.index,
            autopct="%1.1f%%",
            startangle=120,
            colors=cores,
            pctdistance=0.75,
            wedgeprops={"edgecolor": "#FFFFFF", "linewidth": 2},
        )
        for text in texts:
            text.set_fontsize(9)
            text.set_color("#1E293B")
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_fontweight("bold")
            autotext.set_color("#FFFFFF")

        ax.set_title("Distribuição Percentual por Categoria", fontsize=11, fontweight="bold", color="#0B3D2E", pad=10)
        fig.patch.set_facecolor("#FFFFFF")
        fig.tight_layout()

    def gerar_grafico_linha_30_dias(self, fig: Figure) -> None:
        """Desenha série temporal dos últimos 30 dias usando Pandas + Matplotlib."""
        fig.clear()
        ax = fig.add_subplot(111)
        df = self.obter_dataframe_doacoes()

        if df.empty or df["data_dt"].dropna().empty:
            self._desenhar_estado_vazio(ax, "Sem histórico temporal nos últimos 30 dias.")
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
            color="#C1272D",
            linewidth=2.2,
            marker="o",
            markersize=4,
            markerfacecolor="#D4AF37",
            markeredgecolor="#0B3D2E",
        )
        ax.fill_between(diario.index, diario.values, color="#0B3D2E", alpha=0.12)

        ax.set_title("Evolução das Doações (Últimos 30 Dias)", fontsize=11, fontweight="bold", color="#0B3D2E", pad=12)
        ax.set_ylabel("Itens / Dia", fontsize=9, color="#334155")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.tick_params(axis="x", labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FAFAFA")
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
        cores = ["#0B3D2E", "#C1272D", "#D4AF37"]

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
                color="#1E293B",
            )

        ax.set_title(
            f"Balanço Geral (Taxa de Entrega: {kpis['taxa_distribuicao']}%)",
            fontsize=11,
            fontweight="bold",
            color="#0B3D2E",
            pad=12,
        )
        ax.set_xlim(0, max(valores + [10]) * 1.18)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FAFAFA")
        fig.tight_layout()

    @staticmethod
    def _desenhar_estado_vazio(ax: Any, mensagem: str) -> None:
        ax.text(0.5, 0.5, mensagem, ha="center", va="center", fontsize=10, color="#64748B")
        ax.set_axis_off()
