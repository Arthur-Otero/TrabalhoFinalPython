from flask import Flask, jsonify
from flask import request
from flask import render_template

from datetime import date

import sqlite3
from sqlite3 import Error

#######################################################
# Instancia da Aplicacao Flask

app = Flask(__name__)


# 1-> Cadastro de usuario
# 2-> Validação de usuario

# 3-> Cadastrar livros
#######################################################
# 1. Cadastrar produtos

@app.route('/usuario/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':

        login = request.form['login']
        senha = request.form['senha']

        mensagem = 'Erro - nao cadastrado'

        if login and senha:
            registro = (login, senha)
            conn = None
            try:

                conn = sqlite3.connect('db-usuario.db')
                # todo validar login existente

                sql = ''' INSERT INTO usuario(login, senha)
                              VALUES(?,?) '''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - cadastrado'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('cadastrar.html')


# # EDITAR USUARIO
@app.route('/usuario/editar/<int:login>', methods=['POST'])
def editar(login=None):
    if login is None:
        return jsonify({'mensagem': 'Valor invalido'})
    else:
        senha = request.form['senha']

        if senha:
            registro = (login, senha, login)
            conn = None
            try:
                conn = sqlite3.connect('db-usuario.db')
                sql = '''UPDATE usuario set login = ?, senha = ? WHERE
                login = ? '''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                return jsonify({'mensagem': 'Senha mudada'})

            except Error as e:
                return jsonify({'mensagem': e})
            finally:
                conn.close()


@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404


#######################################################
# Execucao da Aplicacao

if __name__ == '__main__':
    app.run()
