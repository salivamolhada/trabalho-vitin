"""Identidade visual Natal Vermelho Vibrante & 3D Colorido, pisca-pisca, ícones Pillow e utilitários."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw

# Paleta Vermelho Natalino & 3D Colorido do Solidário Tech
COR_VERDE_PINHEIRO = "#127053"
COR_VERDE_ESCURO_HOVER = "#0B4F3A"
COR_VERDE_CLARO_CARD = "#0F513B"
COR_VERMELHO_NATAL = "#D93843"
COR_VERMELHO_HOVER = "#9E141D"
COR_DOURADO = "#F5C451"
COR_OURO_CLARO = "#FDE047"

# Fundos em vermelho natalino profundo e superfícies rubi
COR_BRANCO_NEVE = "#6E0E15"      # Fundo principal vermelho natalino rico
COR_SIDEBAR_BRANCO = "#4B080D"   # Sidebar veludo vermelho escuro
COR_SIDEBAR_HOVER = "#8C1620"
COR_CINZA_CLARO = "#A3222C"
COR_CARD_BRANCO = "#560B10"      # Superfície rubi para painéis e tabelas
COR_INPUT_FUNDO = "#360508"

COR_TEXTO_ESCURO = "#FFF9F0"     # Texto principal creme-neve (alto contraste sobre rubi)
COR_TEXTO_SUAVE = "#FFE9B3"      # Texto secundário dourado suave
COR_ALERTA_FUNDO = "#991B1B"

# Paleta 3D colorida por categoria de item
CORES_CATEGORIA_3D: dict[str, tuple[str, str]] = {
    "brinquedo": ("#127053", "#34D399"),
    "alimento": ("#C82333", "#FDA4AF"),
    "roupa": ("#1D4ED8", "#93C5FD"),
    "dinheiro": ("#B45309", "#FCD34D"),
    "cesta": ("#7E22CE", "#D8B4FE"),
}

# Cores do pisca-pisca 3D colorido (aceso brilhante vs. brilho suave)
CORES_PISCA_ACESO: list[str] = [
    "#FF3B5C",
    "#FFD43B",
    "#22E58A",
    "#38BDF8",
    "#C084FC",
    "#FB923C",
]
CORES_PISCA_APAGADO: list[str] = [
    "#881337",
    "#854D0E",
    "#065F46",
    "#075985",
    "#581C87",
    "#9A3412",
]

FRASES_SOLIDARIEDADE: list[str] = [
    "O melhor presente é aquele que aquece o coração.",
    "Pequenos gestos de solidariedade iluminam o Natal de muitas famílias.",
    "Doar é transformar carinho em esperança concreta.",
    "Quando compartilhamos, a magia do Natal se multiplica.",
    "Tecnologia e empatia unidas para cuidar de quem mais precisa.",
]

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "pine_logo_red3d.png"


def formatar_data_atual_pt() -> str:
    """Retorna a data atual formatada em português para o cabeçalho."""
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    ]
    hoje = date.today()
    return f"{hoje.day:02d} de {meses[hoje.month - 1]} de {hoje.year}"


def garantir_logo_pinheiro() -> Path:
    """Gera o ícone de pinheiro 3D com presente embaixo via Pillow sobre fundo rubi."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    if LOGO_PATH.exists():
        return LOGO_PATH

    tamanho = 128
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Círculo vermelho rubi com borda dourada brilhante
    draw.ellipse((4, 4, 124, 124), fill=(158, 20, 29, 255), outline=(245, 196, 81, 255), width=4)

    # Estrela dourada no topo
    draw.polygon(
        [(64, 14), (68, 23), (78, 23), (70, 29), (73, 38), (64, 32), (55, 38), (58, 29), (50, 23), (60, 23)],
        fill=(253, 224, 71, 255),
    )

    # Camadas do pinheiro esmeralda
    draw.polygon([(64, 30), (38, 60), (90, 60)], fill=(52, 211, 153, 255))
    draw.polygon([(64, 46), (30, 82), (98, 82)], fill=(18, 112, 83, 255))

    # Tronco
    draw.rectangle((58, 82, 70, 94), fill=(120, 53, 15, 255))

    # Presente vermelho vivo com laço dourado
    draw.rounded_rectangle((46, 88, 82, 112), radius=4, fill=(239, 68, 68, 255), outline=(253, 224, 71, 255), width=2)
    draw.rectangle((61, 88, 67, 112), fill=(253, 224, 71, 255))
    draw.rectangle((46, 97, 82, 103), fill=(253, 224, 71, 255))

    img.save(LOGO_PATH, format="PNG")
    return LOGO_PATH


def carregar_imagem_logo(tamanho: tuple[int, int] = (46, 46)) -> Image.Image:
    """Carrega a imagem PIL do pinheiro natalino para uso no CustomTkinter e ícone da janela."""
    caminho = garantir_logo_pinheiro()
    return Image.open(caminho).resize(tamanho, Image.Resampling.LANCZOS)
