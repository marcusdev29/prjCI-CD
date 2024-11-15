from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.turma import TurmaNaoEncontrada, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma, ProfessorNaoEncontrado

turma_blueprint = Blueprint('turma', __name__)

@turma_blueprint.route('/turma', methods=["GET"])
def main():
    return 'Rotas para turma'

@turma_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template("turma/turmas.html", turmas=turmas)

@turma_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('/turma/turma_id.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turma_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('turma/criarTurma.html')

@turma_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    descricao = request.form['descricao']
    professor_id = request.form['professor_id']
    ativo = request.form.get('ativo') == 'on'
    nova_turma = {
        'descricao': descricao,
        'professor_id': professor_id,
        'ativo': ativo
    }
    
    try:
        adicionar_turma(nova_turma)
        return redirect(url_for('turma.get_turmas'))
    except ProfessorNaoEncontrado as e:
        # Renderiza o formulário com a mensagem de erro se o professor não for encontrado
        return render_template('turma/criarTurma.html', error_message=str(e))


@turma_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma/turma_update.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turma_blueprint.route('/turmas/<int:id_turma>', methods=['POST'])
def update_turma(id_turma):
    try:
        novos_dados = {
            'descricao': request.form['descricao'],
            'professor_id': request.form['professor_id'],
            'ativo': request.form.get('ativo') == 'on'
        }
        atualizar_turma(id_turma, novos_dados)
        return redirect(url_for('turma.get_turma', id_turma=id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turma_blueprint.route('/turmas/delete/<int:id_turma>', methods=['POST'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turma.get_turmas'))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
