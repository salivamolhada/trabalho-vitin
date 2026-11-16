"""Identidade visual Natal Branco, paleta de cores, pisca-pisca, ícones Pillow e utilitários."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw

# Paleta Natal Branco (White Christmas) do Solidário Tech
COR_VERDE_PINHEIRO = "#0B3D2E"
COR_VERDE_ESCURO_HOVER = "#082C21"
COR_VERDE_CLARO_CARD = "#F1F5F9"
COR_VERMELHO_NATAL = "#C1272D"
COR_VERMELHO_HOVER = "#9E1F24"
COR_DOURADO = "#D4AF37"
COR_BRANCO_NEVE = "#F8FAFC"
COR_SIDEBAR_BRANCO = "#FFFFFF"
COR_SIDEBAR_HOVER = "#F1F5F9"
COR_CINZA_CLARO = "#E2E8F0"
COR_CARD_BRANCO = "#FFFFFF"
COR_TEXTO_ESCURO = "#122620"
COR_TEXTO_SUAVE = "#4B635B"
COR_ALERTA_FUNDO = "#FFF5F5"

# Cores do pisca-pisca natalino (aceso vs. apagado suave)
CORES_PISCA_ACESO: list[str] = [
    "#F59E0B",
    "#E11D48",
    "#10B981",
    "#FBBF24",
    "#38BDF8",
    "#D4AF37",
]
CORES_PISCA_APAGADO: list[str] = [
    "#FDE68A",
    "#FECDD3",
    "#A7F3D0",
    "#FEF3C7",
    "#BAE6FD",
    "#F3E8B8",
]

FRASES_SOLIDARIEDADE: list[str] = [
    "O melhor presente é aquele que aquece o coração.",
    "Pequenos gestos de solidariedade iluminam o Natal de muitas famílias.",
    "Doar é transformar carinho em esperança concreta.",
    "Quando compartilhamos, a magia do Natal se multiplica.",
    "Tecnologia e empatia unidas para cuidar de quem mais precisa.",
]

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "pine_logo.png"


def calcular_dias_para_natal(hoje: date | None = None) -> int:
    """Calcula quantos dias faltam para o dia 25 de dezembro."""
    ref = hoje or date.today()
    natal = date(ref.year, 12, 25)
    if ref > natal:
        natal = date(ref.year + 1, 12, 25)
    return (natal - ref).days


def formatar_data_atual_pt() -> str:
    """Retorna a data atual formatada em português para o cabeçalho."""
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    ]
    hoje = date.today()
    return f"{hoje.day:02d} de {meses[hoje.month - 1]} de {hoje.year}"


def garantir_logo_pinheiro() -> Path:
    """Gera o ícone de pinheiro estilizado com presente embaixo via Pillow, se ausente."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    if LOGO_PATH.exists():
        return LOGO_PATH

    tamanho = 128
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Círculo branco neve com borda dourada
    draw.ellipse((4, 4, 124, 124), fill=(248, 250, 252, 255), outline=(212, 175, 55, 255), width=4)

    # Estrela dourada no topo
    draw.polygon(
        [(64, 14), (68, 23), (78, 23), (70, 29), (73, 38), (64, 32), (55, 38), (58, 29), (50, 23), (60, 23)],
        fill=(212, 175, 55, 255),
    )

    # Camadas do pinheiro
    draw.polygon([(64, 30), (38, 60), (90, 60)], fill=(23, 117, 87, 255))
    draw.polygon([(64, 46), (30, 82), (98, 82)], fill=(11, 61, 46, 255))

    # Tronco
    draw.rectangle((58, 82, 70, 94), fill=(112, 68, 36, 255))

    # Presente vermelho com laço dourado embaixo da árvore
    draw.rounded_rectangle((46, 88, 82, 112), radius=4, fill=(193, 39, 45, 255), outline=(255, 255, 255, 220), width=2)
    draw.rectangle((61, 88, 67, 112), fill=(212, 175, 55, 255))
    draw.rectangle((46, 97, 82, 103), fill=(212, 175, 55, 255))

    img.save(LOGO_PATH, format="PNG")
    return LOGO_PATH


def carregar_imagem_logo(tamanho: tuple[int, int] = (46, 46)) -> Image.Image:
    """Carrega a imagem PIL do pinheiro natalino para uso no CustomTkinter e ícone da janela."""
    caminho = garantir_logo_pinheiro()
    return Image.open(caminho).resize(tamanho, Image.Resampling.LANCZOS)
