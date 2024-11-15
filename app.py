import os
from config import app, db
from controller.alunos import alunos_blueprint
from controller.professor import professor_blueprint
from controller.turma import turma_blueprint  # Adicione esta linha se você também estiver usando o blueprint para turmas

# Registrando os blueprints
app.register_blueprint(alunos_blueprint)
app.register_blueprint(professor_blueprint)
app.register_blueprint(turma_blueprint)  # Registre o blueprint da turma aqui

# Criar todas as tabelas no banco de dados se elas não existirem
with app.app_context():
    db.create_all()

# Executar a aplicação
if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])
