# 📊 Gestão de Prazos API

## 🎯 Sobre o Projeto
Uma API RESTful desenvolvida para resolver um desafio logístico real: o gerenciamento de orçamento e prazos críticos para a conclusão de uma reforma residencial (focada em marcenaria e infraestrutura) com uma data de entrega inegociável. 

O sistema atua como o "motor" inteligente para cruzar custos de fornecedores, monitorar o teto de gastos da obra e calcular a contagem regressiva exata em dias até o prazo final.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python
* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Banco de Dados:** SQLite
* **Integração Front-End:** Consumo preparado para React/Axios.

## ⚙️ Arquitetura e Funcionalidades
A API foi construída seguindo o padrão REST e contempla o ciclo completo de um CRUD:
* **Gestão de Projetos:** Definição de escopo, teto financeiro e data-limite.
* **Inteligência de Prazos:** Rota de cálculo em tempo real que avalia a saúde do orçamento (`SAUDÁVEL 🟢` ou `ESTOURADO 🔴`) e os dias restantes.
* **Controle de Fornecedores:** Cadastro e listagem de prestadores de serviço.
* **Lançamentos Financeiros:** Inserção, edição e exclusão de contratos, com recálculo automático do saldo.

## 🚀 Como rodar o projeto localmente
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`
3. Instale as dependências: `pip install fastapi uvicorn sqlalchemy pydantic`
4. Inicie o servidor: `uvicorn main:app --reload`
5. Acesse a documentação interativa: `http://127.0.0.1:8000/docs`