from config import db
from models.professor import buscar_professor_por_id

class Turma(db.Model):
    __tablename__ = 'turmas'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    ativo = db.Column(db.Boolean, default=True)
    
    professor = db.relationship('Professor', back_populates='turmas')
    alunos = db.relationship('Aluno', back_populates='turma', cascade="all, delete-orphan")

    def __init__(self, descricao, professor_id, ativo=True):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

class TurmaNaoEncontrada(Exception):
    pass

def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada.")
    return {
        'id': turma.id,
        'descricao': turma.descricao,
        'ativo': turma.ativo,
        'professor_id': turma.professor_id,
        'professor_nome': turma.professor.nome if turma.professor else None,
        'alunos': [{'id': aluno.id, 'nome': aluno.nome} for aluno in turma.alunos]
    }

def listar_turmas():
    turmas = Turma.query.all()
    return [{
        'id': turma.id,
        'descricao': turma.descricao,
        'ativo': turma.ativo,
        'professor_id': turma.professor_id,
        'professor_nome': turma.professor.nome if turma.professor else None
    } for turma in turmas]

class ProfessorNaoEncontrado(Exception):
    pass

def adicionar_turma(turma_data):
    """Adiciona uma nova turma ao banco de dados."""
    # Verifica se o ID do professor existe
    professor = buscar_professor_por_id(turma_data['professor_id'])
    if professor is None:
        raise ProfessorNaoEncontrado(f"Professor com ID {turma_data['professor_id']} não encontrado.")

    # Se o professor existe, cria a nova turma
    nova_turma = Turma(
        descricao=turma_data['descricao'],
        professor_id=turma_data['professor_id'],
        ativo=turma_data.get('ativo', True)
    )

    try:
        db.session.add(nova_turma)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada.")
    
    if 'professor_id' in novos_dados:
        professor = buscar_professor_por_id(novos_dados['professor_id'])
        if professor is None:
            raise ProfessorNaoEncontrado(f"Professor com ID {novos_dados['professor_id']} não encontrado.")

    turma.descricao = novos_dados.get('descricao', turma.descricao)
    turma.professor_id = novos_dados.get('professor_id', turma.professor_id)
    turma.ativo = novos_dados.get('ativo', turma.ativo)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def excluir_turma(id_turma):
    """Remove uma turma do banco de dados."""
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada.")
    
    try:
        db.session.delete(turma)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def buscar_turma_por_id(id_turma):
    """Busca uma turma pelo seu ID, retornando None se não for encontrada."""
    return Turma.query.get(id_turma)
