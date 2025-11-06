from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = "troque_para_uma_chave_segura"

ARQUIVO = "banco.csv"
CAMPOS = [
    "NOME","NOME DA MÃE","DATA DE NASCIMENTO","CPF/CNPJ","CONTATO",
    "ENDEREÇO","CIDADE","MARCA","ANO","MODELO","COR","PLACAS",
    "TIPO DE VEICULO","N DO PROCESSO","BANCO","RESTRIÇÕES","OBSERVAÇÃO"
]

def iniciar_arquivo():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CAMPOS)

def carregar_dados():
    dados = []
    if not os.path.exists(ARQUIVO):
        return dados
    with open(ARQUIVO, "r", encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados.append(linha)
    return dados

def salvar_dados(dados):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        for row in dados:
            writer.writerow(row)

# Home: lista + busca
@app.route("/", methods=["GET"])
def index():
    iniciar_arquivo()
    q = request.args.get("q", "").strip().upper()
    dados = carregar_dados()
    if q:
        # Busca por placa, nome, processo, ou CPF/CNPJ
        resultados = []
        for r in dados:
            if (q in (r.get("PLACAS","") or "").upper()
                or q in (r.get("NOME","") or "").upper()
                or q in (r.get("N DO PROCESSO","") or "").upper()
                or q in (r.get("CPF/CNPJ","") or "").upper()):
                resultados.append(r)
        dados = resultados
    return render_template("index.html", registros=dados, campos=CAMPOS, query=q)

# Adicionar novo registro
@app.route("/adicionar", methods=["POST"])
def adicionar():
    iniciar_arquivo()
    dados = carregar_dados()
    novo = {}
    for campo in CAMPOS:
        # pega do form, se não existir coloca string vazia
        valor = request.form.get(campo, "").strip()
        # manter tudo em uppercase para consistência, exceto OBSERVAÇÃO (mantemos original)
        if campo == "OBSERVAÇÃO":
            novo[campo] = valor
        else:
            novo[campo] = valor.upper()
    # valida placa mínima
    if not novo.get("PLACAS"):
        flash("PLACA é obrigatória", "error")
        return redirect(url_for("index"))
    dados.append(novo)
    salvar_dados(dados)
    flash("Registro cadastrado com sucesso.", "success")
    return redirect(url_for("index"))

# Excluir pelo índice (id na tabela)
@app.route("/excluir/<int:idx>", methods=["POST"])
def excluir(idx):
    dados = carregar_dados()
    if 0 <= idx < len(dados):
        placa = dados[idx].get("PLACAS","")
        dados.pop(idx)
        salvar_dados(dados)
        flash(f"Registro com placa {placa} removido.", "success")
    else:
        flash("Índice inválido.", "error")
    return redirect(url_for("index"))

# Página de edição (form preenchido)
@app.route("/editar/<int:idx>", methods=["GET", "POST"])
def editar(idx):
    dados = carregar_dados()
    if idx < 0 or idx >= len(dados):
        flash("Registro não encontrado.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        for campo in CAMPOS:
            valor = request.form.get(campo, "").strip()
            if campo == "OBSERVAÇÃO":
                dados[idx][campo] = valor
            else:
                dados[idx][campo] = valor.upper()
        salvar_dados(dados)
        flash("Registro atualizado com sucesso.", "success")
        return redirect(url_for("index"))
    else:
        # GET -> mostra formulário com valores atuais
        registro = dados[idx]
        return render_template("index.html", registros=dados, campos=CAMPOS, edit_index=idx, edit_registro=registro)

if __name__ == "__main__":
    # para rodar local: flask usa porta dinâmica, Render define PORT var, usamos 0.0.0.0
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
