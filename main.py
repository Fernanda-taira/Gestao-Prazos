from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
import database
from sqlalchemy import func

# Inicializa a API
app = FastAPI(title='MilestoneManager API')

# Ferramenta para abrir e fechar a conexão com o banco a cada acesso
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()    

#----------------------------------------------
# MOLDES DE DADOS (Pydantic) - Isso diz ao Front-End o que queremos
#----------------------------------------------
class ProjetoCreate(BaseModel):
    nome_projeto: str
    orcamento_teto: float
    data_limite: date
     




class FornecedorCreate(BaseModel):  
    nome_empresa: str
    categoria: str   





class LancamentoCreate(BaseModel):
    projeto_id: int
    fornecedor_id: int
    valor_contrato: float
    status_pagamento: str = 'Pendente'

class LancamentoUpdate(BaseModel):
    valor_contrato: float
    status_pagamento: str




#----------------------------------------------
# AS NOSSAS ROTAS
#----------------------------------------------
@app.post('/projetos/')
def criar_projeto(projeto: ProjetoCreate, db: Session = Depends(get_db)):
    novo_projeto = database.Projeto(
        nome_projeto=projeto.nome_projeto,
        orcamento_teto=projeto.orcamento_teto,
        data_limite=projeto.data_limite
    )
    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)
    return {'mensagem': 'Projeto cadastrado com sucesso"', 'dados': novo_projeto}

@app.post('/fornecedores/')
def criar_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    novo_fornecedor = database.Fornecedor(
        nome_empresa=fornecedor.nome_empresa,
        categoria=fornecedor.categoria
    )
    db.add(novo_fornecedor)
    db.commit()
    db.refresh(novo_fornecedor)
    return {'mensagem': 'Fornecedor cadastrado com sucesso!', 'dados': novo_fornecedor}

@app.post('/lancamentos/')
def criar_lancamento(lancamento: LancamentoCreate, db: Session = Depends(get_db)):
    novo_lancamento = database.Lancamento(
        projeto_id=lancamento.projeto_id,
        fornecedor_id=lancamento.fornecedor_id,
        valor_contrato=lancamento.valor_contrato,
        status_pagamento=lancamento.status_pagamento
    )
    db.add(novo_lancamento)
    db.commit()
    db.refresh(novo_lancamento)
    return {'mensagem': 'Lançamento financeiro registrado com sucesso!', 'dados': novo_lancamento}

@app.get('/status-projeto/{projeto_id}')
def status_projeto(projeto_id: int, db: Session = Depends(get_db)):
    # 1. Busca o projeto no banco
    projeto = db.query(database.Projeto).filter(database.Projeto.id == projeto_id).first()
    if not projeto:
        return {'erro': 'Projeto não encontrado'}
    
    # 2. Inteligência: Soma todos os contratos atrelados a este projeto
    total_gasto = db.query(func.sum(database.Lancamento.valor_contrato))\
                    .filter(database.Lancamento.projeto_id == projeto_id).scalar() or 0.0
    
    # 3. Regras de Negócio
    saldo_restante = projeto.orcamento_teto - total_gasto
    # Calcula exatamente os dias entre hoje e a data de entrega
    dias_restantes = (projeto.data_limite - date.today()).days 
    
    return {
        "projeto": projeto.nome_projeto,
        "orcamento_teto": projeto.orcamento_teto,
        "total_gasto": total_gasto,
        "saldo_restante": saldo_restante,
        "dias_restantes": dias_restantes,
        "alerta_orcamento": "ESTOURADO 🔴" if saldo_restante < 0 else "SAUDÁVEL 🟢"
    }

@app.get('/fornecedores/')
def listar_fornecedores(db: Session = Depends(get_db)):
    # Busca todos os prestadores salvols no banco
    fornecedores = db.query(database.Fornecedor).all()
    return {'total': len(fornecedores), 'lista': fornecedores}

@app.delete('/lancamentos/{lacamento_id}')
def deletar_lancamento(lancamento_id: int, db: Session = Depends(get_db)):
    #1. Procura o recibo específico no banco
    lancamento = db.query(database.Lancamento).filter(database.Lancamento.id == lancamento_id).first()

    #2. Se não achar, avisa o erro
    if not lancamento:
        return {'erro': 'Lançamento não encontrado no sistema'}
    
    #3. Se achar, usa a "borracha" do banco de dados
    db.delete(lancamento)
    db.commit()
    return {'mensagem': 'Lançamento excleuído com sucesso" Orçamento protegido.'}

@app.put('/lancamento/{lancamento_id}')
def atualizar_lancamento(lancamento_id: int, atualizacao: LancamentoUpdate, db: Session = Depends(get_db)):
    # 1. Procura o lançamento antigo
    lancamento = db.query(database.Lancamento).filter(database.Lancamento.id == lancamento_id).first()

    # 2. Verifica se existe
    if not lancamento:
        return {'erro': 'Lançamento não encontrado para edição'}
    
    #3. Substitui os valores antigos pelos novos
    lancamento.valor_contrato = atualizacao.valor_contrato
    lancamento.status_pagamento = atualizacao.status_pagamento
    db.commit()
    db.refresh(lancamento)

    return{'mensagem': 'Contrato renegociado e atualizado com sucesso', 'dados': lancamento}
