# 🎄 Solidário Tech — Sistema de Gerenciamento de Doações de Natal

Projeto desenvolvido para o **Desafio Tech Solutions 2026** (**3º A – Técnico em Desenvolvimento de Sistemas**), integrando **Banco de Dados**, **Ciência de Dados** e **Desenvolvimento de Sistemas** em uma aplicação desktop completa com tema natalino.

---

## 🎯 Descrição do Projeto e Problema Resolvido

Durante as campanhas de Natal, ONGs e instituições de caridade recebem dezenas de doações heterogêneas (brinquedos, alimentos, roupas, recursos financeiros e cestas básicas) e precisam controlar rapidamente o que entrou, o que ainda está disponível e para quais famílias ou instituições cada item foi entregue.

O **Solidário Tech** resolve esse gargalo substituindo planilhas manuais por um sistema desktop com:
- **Cadastro completo (CRUD)** de doações com atualização automática de saldo;
- **Controle visual de estoque** com alerta em vermelho quando uma categoria fica abaixo de **5 unidades**;
- **Registro seguro de distribuições** que impede entregas acima do saldo disponível;
- **Painel analítico (Ciência de Dados)** com gráficos embutidos via Pandas, Matplotlib e Seaborn;
- **Auditoria e confiabilidade** com transações SQLite (`COMMIT`/`ROLLBACK`) e histórico de logs em `app.log`.

---

## 🛠️ Tecnologias Utilizadas

| Pilar | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| Linguagem & Arquitetura | **Python 3.11+ (POO)** | Camadas `UI → Service → Repository → Model → SQLite` |
| Interface Gráfica | **CustomTkinter** + **ttk.Treeview** | Sidebar natalina, cards, tabelas e pop-ups `CTkToplevel` |
| Banco de Dados | **SQLite 3** (`sqlite3`) | Persistência local relacional (`solidario_tech.db`) |
| Ciência de Dados | **Pandas**, **Matplotlib**, **Seaborn** | Agregações temporais e gráficos embutidos (`FigureCanvasTkAgg`) |
| Imagens & Ícones | **Pillow (PIL)** | Geração e exibição do logotipo do pinheiro natalino |

---

## 🚀 Instruções de Instalação e Execução

```bash
# 1. Acesse a pasta do projeto Python
cd solidario_tech

# 2. (Opcional) Crie e ative um ambiente virtual
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python main.py
```

> **Nota:** O banco `solidario_tech.db` já acompanha dados iniciais de exemplo para facilitar a demonstração imediata. Caso deseje reiniciar o banco do zero, apague `solidario_tech.db` e execute `python main.py` novamente (o esquema e o seed automático serão recriados).

---

## 📱 Telas do Sistema

1. **🎄 Dashboard:** Saudação natalina dinâmica, frases motivacionais rotativas, contador regressivo para 25 de dezembro, cards de resumo (Total Recebido, Total Distribuído, Itens em Estoque) e mini-tabela das 5 últimas doações.
2. **🎁 Doações:** Formulário completo (doador, tipo, quantidade, data e descrição opcional), botões Salvar / Limpar / Editar / Excluir, busca por doador e filtro por categoria.
3. **🧺 Estoque:** 5 cards com ícones natalinos (`🎁 🍪 🧥 💰 🧺`), destaque vermelho automático quando `< 5` unidades e painel de ajuste manual (entrada/saída).
4. **⭐ Distribuições:** Formulário com verificação rigorosa de saldo em estoque, atualização automática após entrega e tabela com busca por beneficiário.
5. **📊 Gráficos:** 4 gráficos Matplotlib/Seaborn (Barras por categoria, Pizza percentual, Linha dos últimos 30 dias e Comparativo Arrecadado vs. Distribuído).
6. **🎅 Sobre:** Contextualização social do projeto e créditos do Desafio Tech Solutions 2026.

---

## 💾 Estrutura do Banco de Dados (`solidario_tech.db`)

- **`doacoes`**: Armazena cada doação recebida (`id`, `doador`, `tipo`, `quantidade`, `data_doacao`, `descricao`, `criado_em`), com `CHECK` garantindo categorias válidas e `quantidade > 0`.
- **`estoque`**: Mantém 1 registro único por categoria (`brinquedo`, `alimento`, `roupa`, `dinheiro`, `cesta`) com `quantidade_disponivel >= 0` atualizada atomicamente pelas camadas de serviço.
- **`distribuicoes`**: Registra entregas realizadas (`id`, `doacao_id`, `item_tipo`, `quantidade`, `beneficiario`, `data_entrega`, `responsavel`, `criado_em`) com chave estrangeira para `doacoes(id)`.
