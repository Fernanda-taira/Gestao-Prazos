from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Conexão com o banco (Criará um arquivo local chamado milestone.db)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./milestone.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})

# 2. Sessão para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Modelagem das Tabelas
class Projeto(Base):
    __tablename__ = 'projetos'

    id = Column(Integer, primary_key=True, index=True)
    nome_projeto = Column(String, index=True)
    orcamento_teto = Column(Float)
    data_limite = Column(Date)

class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    
    id = Column(Integer, primary_key=True, index=True)
    nome_empresa = Column(String)
    categoria = Column(String)  #ex: Móveis Planejados
    status_confirmacao = Column(Boolean, default=False)

class Lancamento(Base):
   __tablename__ = 'lancamentos_financeiros'

   id = Column(Integer, primary_key=True, index=True)
   projeto_id = Column(Integer, ForeignKey('projetos.id'))   # Conecta ao projeto
   fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))  #Conecta ao prestador
   valor_contrato = Column(Float)
   status_pagamento = Column(String)  # Ex: Pendente, Pago

# 4. Comando final que cria as tabelas fisicamente
Base.metadata.create_all(bind=engine)


