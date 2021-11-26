from flask import Flask, jsonify, redirect
from flask import request
from flask import render_template

import pymysql
from datetime import date

import sqlite3
from sqlite3 import Error

#######################################################
# Instancia da Aplicacao Flask

app = Flask(__name__)

rds_host = 'mysqlserver.c91yee6tpto5.us-east-1.rds.amazonaws.com'
name = 'admin'
password = 'admin1980'
db_name = 'usuario'
port = 3306

rds_host2 = 'database-1.c91yee6tpto5.us-east-1.rds.amazonaws.com'
name2 = 'admin'
password2 = 'admin1980'
db_name2 = 'teste2'
port2 = 3306

# Cadastrar Livros
@app.route('/livros/cadastrar', methods=['GET', 'POST'])
def cadastrar_livro():
    if request.method == 'POST':

        nome = request.form['nome']
        autor = request.form['autor']
        preco = request.form['preco']
        quantidade = request.form['quantidade']

        mensagem = 'Erro - nao cadastrado'

        if nome and autor and preco and quantidade:
            try:

                conn = pymysql.connect(host=rds_host2, user=name2,
                                       passwd=password2, db=db_name2,
                                       connect_timeout=5,
                                       cursorclass=pymysql.cursors.DictCursor)

                sql = ''' INSERT INTO livros2(nome, autor, preco, quantidade)
                              VALUES(%s,%s,%s,%s) '''
                registro = (nome, autor, preco, quantidade)
                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - cadastrado'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('cadastrar.html')


# Excluir Livros
@app.route('/livros/excluir/<int:id>', methods=['GET'])
def excluir(id=None):
    conn = None
    if id is None:
        return jsonify({'mensagem': 'ID invalido'})
    else:
        try:
            conn = pymysql.connect(host=rds_host2, user=name2,
                                   passwd=password2, db=db_name2,
                                   connect_timeout=5,
                                   cursorclass=pymysql.cursors.DictCursor)
            sql = '''DELETE FROM livros2 WHERE id = ''' + str(id)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

            # return jsonify({'mensagem': 'registro excluido'})
            return redirect('http://127.0.0.1:5000/livros')

        except Error as e:
            return jsonify({'mensagem': e})
        finally:
            conn.close()


# Editar Livros
@app.route('/livros/editar/<string:quantidade_api>/<int:id>', methods=['GET'])
def editar_livro(id=None, quantidade_api=None):
    quantidade = 0
    if id is None:
        return jsonify({'mensagem': 'Valor invalido'})
    else:
        conn = None
        try:
            conn = pymysql.connect(host=rds_host2, user=name2,
                                   passwd=password2, db=db_name2,
                                   connect_timeout=5,
                                   cursorclass=pymysql.cursors.DictCursor)

            sql = '''SELECT * FROM livros2 WHERE id = ''' + str(id)

            cur = conn.cursor()
            cur.execute(sql)

            registros = cur.fetchall()

            for i in registros:
                print(i)
                if i['quantidade'] + int(quantidade_api) > 0:
                    quantidade = i['quantidade'] + int(quantidade_api)

            sql = '''UPDATE livros2 SET quantidade = %s WHERE id = %s '''
            cur = conn.cursor()
            registro = (quantidade, id)
            cur.execute(sql, registro)

            conn.commit()

            return redirect('http://127.0.0.1:5000/livros')

        except Error as e:
            return jsonify({'mensagem': e})
        finally:
            conn.close()


# Listar Livros
@app.route('/livros', methods=['GET'])
def listar():
    conn = None
    try:

        conn = pymysql.connect(host=rds_host2, user=name2,
                               passwd=password2, db=db_name2,
                               connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
        sql = '''SELECT * FROM livros2'''

        cur = conn.cursor()

        cur.execute(sql)

        registros = cur.fetchall()
        arrayRegistros = []

        for i in registros:
            array2 = [i['id'],i['nome'], i['autor'], i['preco'], i['quantidade']]
            arrayRegistros.append(array2)

        return render_template('listar.html', regs=arrayRegistros)

    except Error as e:
        print(e)
    finally:
        conn.close()


# Cadastros de Usuario
#######################################################################################################
@app.route('/', methods=['GET'])
def inicio():
    conn = None
    try:
        conn = pymysql.connect(host=rds_host, user=name,
                               passwd=password, db=db_name,
                               connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
        #conn = sqlite3.connect('db-usuario.db')
        sql = "select * from usuario"

        cur = conn.cursor()

        cur.execute(sql)

        registros = cur.fetchall()
        arrayRegistros = []

        for i in registros:
            array2 = [i['cpf'],i['nome'],i['telefone'],i['email'],i['senha']]
            arrayRegistros.append(array2)

        return render_template('Inicio.html', regs=arrayRegistros)

    except Error as e:
        print(e)
    finally:
        conn.close()


@app.route('/usuario/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':

        cpf = request.form['cpf']
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = request.form['senha']

        if cpf and nome and telefone and email and senha:
            conn = None
            try:

                conn = pymysql.connect(host=rds_host, user=name,
                                       passwd=password, db=db_name,
                                       connect_timeout=5,
                                       cursorclass=pymysql.cursors.DictCursor)
                sql = ''' INSERT INTO usuario(cpf, nome, telefone, email, senha)
                              VALUES(%s,%s,%s,%s,%s) '''

                registro = (cpf, nome, telefone, email, senha)
                cur = conn.cursor()

                cur.execute(sql,registro)

                conn.commit()

                mensagem = 'Sucesso - cadastrado'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('cadastrar_usuario.html')


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
                conn = pymysql.connect(host=rds_host, user=name,
                                       passwd=password, db=db_name,
                                       connect_timeout=5,
                                       cursorclass=pymysql.cursors.DictCursor)
                sql = '''UPDATE usuario set cpf = ?, nome = ?, telefone = ?, email = ?, senha = ? WHERE
                cpf = ? '''

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