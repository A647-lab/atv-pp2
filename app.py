import os
from flask import Flask, render_template, request, redirect
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
        # Convertendo as strings de data para objetos de data
        data_inicio = datetime.strptime(request.form.get("data_inicio"), '%Y-%m-%d').date()
        data_fim = datetime.strptime(request.form.get("data_fim"), '%Y-%m-%d').date()
        
        # Verificar se o título já existe
        title = request.form.get("title")
        existing_book = supabase.table('atividade').select('*').eq('title', title).execute()

        if existing_book.data:
            print("Este título já existe. Não foi possível adicionar.")
        else:
            # Inserindo o registro no Supabase
            book = {
                'title': title,
                'descricao': request.form.get("descricao"),
                'data_inicio': data_inicio.isoformat(),
                'data_fim': data_fim.isoformat()
            }
            supabase.table('atividade').insert(book).execute()

    # Consultando todos os livros
    response = supabase.table('atividade').select('*').execute()
    books = response.data

    return render_template("index.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    newdescricao = request.form.get("newdescricao")
    newdata_inicio = datetime.strptime(request.form.get("newdata_inicio"), '%Y-%m-%d').date()
    newdata_fim = datetime.strptime(request.form.get("newdata_fim"), '%Y-%m-%d').date()

    # Atualizando o registro no Supabase
    supabase.table('atividade').update({
        'title': newtitle,
        'descricao': newdescricao,
        'data_inicio': newdata_inicio.isoformat(),
        'data_fim': newdata_fim.isoformat()
    }).eq('title', oldtitle).execute()

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    # Deletando o registro no Supabase
    supabase.table('atividade').delete().eq('title', title).execute()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
