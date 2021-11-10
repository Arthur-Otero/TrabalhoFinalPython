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

@app.route('/livros/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':

        nome = request.form['nome']
        autor = request.form['autor']
        preco = request.form['preco']
        quantidade = request.form['quantidade']

        mensagem = 'Erro - nao cadastrado'

        if nome and autor and preco and quantidade:
            registro = (nome, autor, preco, quantidade)
            conn = None
            try:

                conn = sqlite3.connect('db-livros.db')

                sql = ''' INSERT INTO livros(nome, autor, preco, quantidade)
                              VALUES(?,?,?,?) '''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - cadastrado'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('cadastrar.html')


#  # EXCLUIR LIVRO
@app.route('/livros/excluir/<int:id>', methods=['GET'])
def excluir(id=None):
    conn = None
    if id is None:
        return jsonify({'mensagem': 'ID invalido'})
    else:
        try:
            conn = sqlite3.connect('db-livros.db')
            sql = '''DELETE FROM livros WHERE id = ''' + str(id)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

            return jsonify({'mensagem': 'registro excluido'})

        except Error as e:
            return jsonify({'mensagem': e})
        finally:
            conn.close()


# # EDITAR LIVRO
@app.route('/livros/editar/<int:id>', methods=['POST'])
def editar(id=None):
    if id is None:
        return jsonify({'mensagem': 'Valor invalido'})
    else:
        nome = request.form['nome']
        autor = request.form['autor']
        preco = request.form['preco']
        quantidade = request.form['quantidade']

        if nome and autor and preco and quantidade:
            registro = (nome, autor, preco, quantidade, id)
            conn = None
            try:
                conn = sqlite3.connect('db-livros.db')
                sql = '''UPDATE livros set nome = ?, autor = ?, preco = ?, quantidade = ? WHERE
                id = ? '''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                return jsonify({'mensagem': 'Livro atualizado'})

            except Error as e:
                return jsonify({'mensagem': e})
            finally:
                conn.close()


@app.route('/livros', methods=['GET'])
def listar():
    conn = None
    try:

        conn = sqlite3.connect('db-livros.db')
        sql = '''SELECT * FROM livros'''

        cur = conn.cursor()

        cur.execute(sql)

        registros = cur.fetchall()

        return render_template('listar.html', regs=registros)

    except Error as e:
        print(e)
    finally:
        conn.close()

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404


#######################################################
# Execucao da Aplicacao

if __name__ == '__main__':
    app.run()
