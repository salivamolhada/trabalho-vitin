"""Script de seed idempotente para popular solidario_tech.db com dados natalinos de exemplo."""

from __future__ import annotations

from datetime import datetime, timedelta

from database.connection import DatabaseConnection
from services.distribuicao_service import DistribuicaoService
from services.doacao_service import DoacaoService


def popular_dados_exemplo(db: DatabaseConnection) -> bool:
    """Popula o banco caso esteja vazio; retorna True se inseriu novos registros."""
    db.inicializar_banco()

    with db.connect() as conn:
        existente = int(conn.execute("SELECT COUNT(*) FROM doacoes").fetchone()[0])
        if existente > 0:
            return False

    doacao_service = DoacaoService(db)
    distribuicao_service = DistribuicaoService(db)
    hoje = datetime.now().date()

    def dias_atras(n: int) -> str:
        return (hoje - timedelta(days=n)).strftime("%Y-%m-%d")

    doacoes_iniciais = [
        ("Supermercado Estrela do Sul", "cesta", 18, dias_atras(27), "Cestas básicas natalinas com panetone"),
        ("Colégio São José — Turma 3º A", "brinquedo", 32, dias_atras(24), "Bonecas, carrinhos e jogos educativos"),
        ("Padaria Bom Sabor", "alimento", 25, dias_atras(21), "Panetones, biscoitos e achocolatados"),
        ("Comunidade Vila Esperança", "roupa", 20, dias_atras(18), "Agasalhos infantis e camisetas novas"),
        ("Associação Comercial Local", "dinheiro", 15, dias_atras(15), "Cotas de apoio financeiro (R$ 100 cada)"),
        ("Família Andrade", "brinquedo", 14, dias_atras(12), "Bolas de futebol e kits de desenho"),
        ("Mercado Central Solidário", "alimento", 30, dias_atras(9), "Arroz, feijão, óleo e macarrão"),
        ("Loja Encanto Kids", "roupa", 16, dias_atras(7), "Conjuntos infantis de verão"),
        ("Empresa Tech Solutions", "cesta", 12, dias_atras(5), "Cestas completas para famílias cadastradas"),
        ("Grupo Voluntários do Bem", "brinquedo", 22, dias_atras(3), "Brinquedos embrulhados para entrega"),
        ("Dra. Camila Nogueira", "dinheiro", 8, dias_atras(2), "Cotas destinadas à ceia comunitária"),
        ("Igreja Matriz Santa Luzia", "alimento", 18, dias_atras(1), "Kits de café da manhã e doces natalinos"),
    ]

    ids_por_tipo: dict[str, int] = {}
    for doador, tipo, qtd, data_str, desc in doacoes_iniciais:
        criada = doacao_service.registrar_doacao(doador, tipo, qtd, data_str, desc)
        if criada.id is not None:
            ids_por_tipo[tipo] = criada.id

    # Distribuições deixando propositalmente 'dinheiro' (< 5) e 'cesta' próximos do alerta
    distribuicoes_iniciais = [
        ("cesta", 26, "Abrigo Lar Feliz", dias_atras(10), "Mariana Costa"),
        ("brinquedo", 38, "Creche Pequeno Príncipe", dias_atras(6), "Lucas Ferreira"),
        ("alimento", 45, "Cozinha Comunitária Esperança", dias_atras(4), "Ana Paula Silva"),
        ("roupa", 24, "Projeto Mãos Unidas", dias_atras(3), "Rafael Oliveira"),
        ("dinheiro", 20, "Casa de Apoio São Vicente", dias_atras(1), "Mariana Costa"),
    ]

    for tipo, qtd, benef, data_str, resp in distribuicoes_iniciais:
        distribuicao_service.registrar_distribuicao(
            item_tipo=tipo,
            quantidade=qtd,
            beneficiario=benef,
            data_entrega=data_str,
            responsavel=resp,
            doacao_id=ids_por_tipo.get(tipo),
        )

    return True


if __name__ == "__main__":
    database = DatabaseConnection()
    inseriu = popular_dados_exemplo(database)
    print("Seed concluído!" if inseriu else "Banco já possui registros; nenhuma alteração feita.")
