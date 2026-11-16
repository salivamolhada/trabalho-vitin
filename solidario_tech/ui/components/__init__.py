"""Componentes reutilizáveis de interface do Solidário Tech."""

from ui.components.card import EstoqueCategoryCard, KPICard, PiscaPiscaStrip
from ui.components.dialog import ask_christmas_confirm, show_christmas_dialog
from ui.components.table import StyledTreeviewTable

__all__ = [
    "PiscaPiscaStrip",
    "KPICard",
    "EstoqueCategoryCard",
    "StyledTreeviewTable",
    "show_christmas_dialog",
    "ask_christmas_confirm",
]
