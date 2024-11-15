from flask import Blueprint, flash, request, jsonify, render_template, redirect, url_for
from models.alunos import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from models.turma import buscar_turma_por_id

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def getIndex():
    return render_template("index.html")

# ROTA PARA LISTAR TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("alunos/alunos.html", alunos=alunos)

# ROTA PARA OBTER UM ALUNO ESPECÍFICO POR ID
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

# ROTA PARA EXIBIR FORMULÁRIO DE CRIAÇÃO DE UM NOVO ALUNO
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('alunos/criarAlunos.html')

# ROTA PARA CRIAR UM NOVO ALUNO
from flask import jsonify, request, redirect, url_for
from werkzeug.exceptions import NotFound

@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    try:
        turma_id = int(request.form.get('turma_id'))
        
        turma = buscar_turma_por_id(turma_id)
        if not turma:
            return render_template('alunos/criarAlunos.html', error_message=f'A turma com ID {turma_id} não existe.')
        
        if not turma.ativo:
            return render_template('alunos/criarAlunos.html', error_message=f'A turma com ID {turma_id} não está ativa.')
        
        novo_aluno = {
            'nome': request.form['nome'],
            'idade': int(request.form['idade']),
            'data_nascimento': request.form.get('data_nascimento'),
            'nota_primeiro_semestre': float(request.form.get('nota_primeiro_semestre', 0)),
            'nota_segundo_semestre': float(request.form.get('nota_segundo_semestre', 0)),
            'turma_id': turma_id
        }

        # Função para adicionar aluno ao banco
        adicionar_aluno(novo_aluno)

        # Redireciona para a lista de alunos após a criação bem-sucedida
        return redirect(url_for('alunos.get_alunos'))
    
    except ValueError:
        # Redireciona para o formulário com mensagem de dados inválidos
        flash('Dados inválidos fornecidos', 'error')
        return redirect(url_for('alunos.get_aluno_form'))



# ROTA PARA EXIBIR FORMULÁRIO PARA EDITAR UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

from datetime import datetime

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['POST'])
def update_aluno(id_aluno):
    try:
        # Validar e converter a idade
        idade = request.form.get('idade')
        if idade is not None and idade.strip():
            idade = int(idade)
        else:
            raise ValueError("Idade não pode ser vazia")

        # Validar e converter o ID da turma
        turma_id = request.form.get('turma_id')
        if turma_id is not None and turma_id.strip():
            turma_id = int(turma_id)
        else:
            raise ValueError("Turma ID não pode ser vazio")

        # Verifica se a turma existe no banco de dados
        turma = buscar_turma_por_id(turma_id)
        if not turma:
            return jsonify({'message': f'A turma com ID {turma_id} não existe.'}), 404

        # Converter data_nascimento de string para date, caso seja fornecida
        data_nascimento_str = request.form.get('data_nascimento')
        if data_nascimento_str:
            try:
                data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Data de Nascimento deve estar no formato YYYY-MM-DD")
        else:
            data_nascimento = None

        # Montar o dicionário com os novos dados
        novos_dados = {
            'nome': request.form['nome'],
            'idade': idade,
            'data_nascimento': data_nascimento,  # Passa o objeto date aqui
            'nota_primeiro_semestre': float(request.form.get('nota_primeiro_semestre', 0)),
            'nota_segundo_semestre': float(request.form.get('nota_segundo_semestre', 0)),
            'turma_id': turma_id
        }

        # Chamar a função para atualizar o aluno
        atualizar_aluno(id_aluno, novos_dados)
        return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))

    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

# ROTA PARA DELETAR UM ALUNO
@alunos_blueprint.route('/alunos/delete/<int:id_aluno>', methods=['POST'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return redirect(url_for('alunos.get_alunos'))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
