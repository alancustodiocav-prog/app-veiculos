from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB = "banco.db"

# Cria a tabela se não existir
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME TEXT,
            NOME_MAE TEXT,
            DATA_NASCIMENTO TEXT,
            CPF_CNPJ TEXT,
            CONTATO TEXT,
            ENDERECO TEXT,
            CIDADE TEXT,
            MARCA TEXT,
            ANO TEXT,
            MODELO TEXT,
            COR TEXT,
            PLACAS TEXT,
            TIPO_VEICULO TEXT,
            N_PROCESSO TEXT,
            BANCO TEXT,
            RESTRICOES TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Buscar veículos
def buscar_veiculos(placa=""):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if placa:
        c.execute("SELECT * FROM veiculos WHERE PLACAS LIKE ?", ('%'+placa+'%',))
    else:
        c.execute("SELECT * FROM veiculos")
    resultados = c.fetchall()
    conn.close()
    return resultados

# Adicionar veículo
def adicionar_veiculo(dados):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        INSERT INTO veiculos (
            NOME,NOME_MAE,DATA_NASCIMENTO,CPF_CNPJ,CONTATO,ENDERECO,CIDADE,
            MARCA,ANO,MODELO,COR,PLACAS,TIPO_VEICULO,N_PROCESSO,BANCO,RESTRICOES
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        dados["NOME"], dados["NOME_MAE"], dados["DATA_NASCIMENTO"], dados["CPF_CNPJ"],
        dados["CONTATO"], dados["ENDERECO"], dados["CIDADE"], dados["MARCA"],
        dados["ANO"], dados["MODELO"], dados["COR"], dados["PLACAS"],
        dados["TIPO_VEICULO"], dados["N_PROCESSO"], dados["BANCO"], dados["RESTRICOES"]
    ))
    conn.commit()
    conn.close()

# Inicializa banco
init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    query = ""
    resultados = buscar_veiculos()

    if request.method == 'POST':
        if 'buscar' in request.form:
            query = request.form.get('placa').upper()
            resultados = buscar_veiculos(query)
        elif 'adicionar' in request.form:
            novo = {
                "NOME": request.form.get("NOME"),
                "NOME_MAE": request.form.get("NOME_MAE"),
                "DATA_NASCIMENTO": request.form.get("DATA_NASCIMENTO"),
                "CPF_CNPJ": request.form.get("CPF_CNPJ"),
                "CONTATO": request.form.get("CONTATO"),
                "ENDERECO": request.form.get("ENDERECO"),
                "CIDADE": request.form.get("CIDADE"),
                "MARCA": request.form.get("MARCA"),
                "ANO": request.form.get("ANO"),
                "MODELO": request.form.get("MODELO"),
                "COR": request.form.get("COR"),
                "PLACAS": request.form.get("PLACAS"),
                "TIPO_VEICULO": request.form.get("TIPO_VEICULO"),
                "N_PROCESSO": request.form.get("N_PROCESSO"),
                "BANCO": request.form.get("BANCO"),
                "RESTRICOES": request.form.get("RESTRICOES")
            }
            adicionar_veiculo(novo)
            return redirect(url_for('home'))

    return render_template('index.html', veiculos=resultados, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
