import os
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from supabase import create_client

# Configurações do Supabase
url = "https://uqxenkoqehszhfjoqdby.supabase.co"  # Substitua pela URL do seu projeto
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVxeGVua29xZWhzemhmam9xZGJ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk4NjIwNDMsImV4cCI6MjA0NTQzODA0M30.HgVtvI-9-o8CwfQe56l-pivtA5pO4D6uDpQcL_TYv0Q"  # Substitua pela sua chave de API
supabase = create_client(url, key)

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title")
        descricao = request.form.get("descricao")
        data_inicio = request.form.get("data_inicio")
        data_fim = request.form.get("data_fim")

        if title and descricao and data_inicio and data_fim:
            try:
                # Convertendo as strings de data para o formato ISO
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date().isoformat()
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date().isoformat()

                # Verificar se o título já existe
                existing_book = supabase.table('atividade').select('*').eq('title', title).execute()

                if existing_book.data:
                    flash("Este título já existe. Não foi possível adicionar.")
                else:
                    # Inserindo o registro no Supabase
                    book = {
                        'title': title,
                        'descricao': descricao,
                        'data_inicio': data_inicio,
                        'data_fim': data_fim
                    }
                    response = supabase.table('atividade').insert(book).execute()

                    # Verificar se a inserção foi bem-sucedida

            except Exception as e:
                flash("Erro ao processar a solicitação: " + str(e))
        else:
            flash("Por favor, preencha todos os campos.")

    # Consultando todos os livros
    response = supabase.table('atividade').select('*').execute()
    books = response.data

    return render_template("index.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    oldtitle = request.form.get("oldtitle")
    newtitle = request.form.get("newtitle")
    newdescricao = request.form.get("newdescricao")
    newdata_inicio = request.form.get("newdata_inicio")
    newdata_fim = request.form.get("newdata_fim")

    if oldtitle and newtitle and newdescricao and newdata_inicio and newdata_fim:
        try:
            # Convertendo as strings de data para o formato ISO
            newdata_inicio = datetime.strptime(newdata_inicio, '%Y-%m-%d').date().isoformat()
            newdata_fim = datetime.strptime(newdata_fim, '%Y-%m-%d').date().isoformat()

            # Atualizando o registro no Supabase
            response = supabase.table('atividade').update({
                'title': newtitle,
                'descricao': newdescricao,
                'data_inicio': newdata_inicio,
                'data_fim': newdata_fim
            }).eq('title', oldtitle).execute()



        except Exception as e:
            flash("Erro ao processar a atualização: " + str(e))

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    if title:
        try:
            # Deletando o registro no Supabase
            response = supabase.table('atividade').delete().eq('title', title).execute()

        except Exception as e:
            flash("Erro ao processar a exclusão: " + str(e))

    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
