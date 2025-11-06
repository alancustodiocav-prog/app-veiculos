import csv
import os

# Configurações
ARQUIVO = "banco.csv"
CAMPOS = [
    "NOME", "NOME DA MÃE", "DATA DE NASCIMENTO", "CPF/CNPJ", "CONTATO",
    "ENDEREÇO", "CIDADE", "MARCA", "ANO", "MODELO", "COR", "PLACA",
    "TIPO DE VEICULO", "N DO PROCESSO", "BANCO", "RESTRIÇÕES", "OBSERVAÇÃO"
]

# Cria o arquivo CSV se não existir
def iniciar_arquivo():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(CAMPOS)

# Carrega dados do CSV
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        return list(leitor)

# Salva dados no CSV
def salvar_dados(dados):
    with open(ARQUIVO, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS)
        escritor.writeheader()
        for linha in dados:
            escritor.writerow(linha)

# Função: Cadastrar veículo
def cadastrar():
    dados = carregar_dados()
    registro = {campo: entradas[campo].get().upper() for campo in CAMPOS}
    if not registro["PLACA"]:
        messagebox.showerror("Erro", "O campo PLACA é obrigatório.")
        return
    dados.append(registro)
    salvar_dados(dados)
    for campo in CAMPOS:
        entradas[campo].delete(0, tk.END)
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")

# Função: Buscar por placa
def buscar():
    placa_busca = entrada_busca.get().strip().upper()
    dados = carregar_dados()
    resultados = [d for d in dados if d["PLACA"] == placa_busca]
    for item in tabela.get_children():
        tabela.delete(item)
    for row in resultados:
        tabela.insert("", tk.END, values=[row[c] for c in CAMPOS])
    if not resultados:
        messagebox.showinfo("Resultado", "Nenhum veículo encontrado com essa placa.")

# Função: Atualizar listagem completa
def atualizar_lista():
    for item in tabela.get_children():
        tabela.delete(item)
    dados = carregar_dados()
    for row in dados:
        tabela.insert("", tk.END, values=[row[c] for c in CAMPOS])

# Função: Excluir veículo selecionado
def excluir():
    item_selecionado = tabela.focus()
    if not item_selecionado:
        messagebox.showwarning("Atenção", "Selecione um registro para excluir.")
        return
    valores = tabela.item(item_selecionado, "values")
    placa = valores[11]
    dados = carregar_dados()
    novos = [d for d in dados if d["PLACA"] != placa]
    salvar_dados(novos)
    atualizar_lista()
    messagebox.showinfo("Sucesso", f"Veículo com placa {placa} excluído com sucesso!")

# ---------- INTERFACE ----------
iniciar_arquivo()
janela = tk.Tk()
janela.title("🚗 Sistema de Veículos")
janela.geometry("1300x700")
janela.configure(bg="#1e1e1e")

# Estilo Dark
style = ttk.Style(janela)
style.theme_use("clam")
style.configure("Treeview",
                background="#2b2b2b",
                foreground="white",
                rowheight=25,
                fieldbackground="#2b2b2b",
                font=("Segoe UI", 10))
style.map("Treeview", background=[("selected", "#444444")])
style.configure("Treeview.Heading",
                background="#1e1e1e",
                foreground="white",
                font=("Segoe UI", 10, "bold"))
style.configure("TButton",
                background="#3a3a3a",
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                padding=6)
style.map("TButton",
          background=[("active", "#505050")])

# ----- CAMPOS DE CADASTRO -----
frame_form = tk.Frame(janela, bg="#1e1e1e")
frame_form.pack(pady=10)

entradas = {}
colunas = [
    ("NOME", "NOME DA MÃE", "DATA DE NASCIMENTO", "CPF/CNPJ", "CONTATO"),
    ("ENDEREÇO", "CIDADE", "MARCA", "ANO", "MODELO"),
    ("COR", "PLACA", "TIPO DE VEICULO", "N DO PROCESSO", "BANCO"),
    ("RESTRIÇÕES", "OBSERVAÇÃO")
]

for linha in colunas:
    linha_frame = tk.Frame(frame_form, bg="#1e1e1e")
    linha_frame.pack(pady=2)
    for campo in linha:
        lbl = tk.Label(linha_frame, text=campo, fg="white", bg="#1e1e1e", width=15, anchor="w")
        lbl.pack(side="left")
        entrada = tk.Entry(linha_frame, width=25, bg="#2b2b2b", fg="white", insertbackground="white", relief="flat")
        entrada.pack(side="left", padx=5)
        entradas[campo] = entrada

# ----- BOTÕES -----
frame_btn = tk.Frame(janela, bg="#1e1e1e")
frame_btn.pack(pady=10)

ttk.Button(frame_btn, text="Cadastrar", command=cadastrar).pack(side="left", padx=10)
ttk.Button(frame_btn, text="Excluir", command=excluir).pack(side="left", padx=10)
ttk.Button(frame_btn, text="Atualizar Lista", command=atualizar_lista).pack(side="left", padx=10)

# ----- BUSCA -----
frame_busca = tk.Frame(janela, bg="#1e1e1e")
frame_busca.pack(pady=10)
tk.Label(frame_busca, text="Buscar por PLACA:", fg="white", bg="#1e1e1e").pack(side="left")
entrada_busca = tk.Entry(frame_busca, width=20, bg="#2b2b2b", fg="white", insertbackground="white", relief="flat")
entrada_busca.pack(side="left", padx=5)
ttk.Button(frame_busca, text="Buscar", command=buscar).pack(side="left", padx=10)

# ----- TABELA -----
frame_tab = tk.Frame(janela, bg="#1e1e1e")
frame_tab.pack(fill="both", expand=True, padx=10, pady=10)

tabela = ttk.Treeview(frame_tab, columns=CAMPOS, show="headings")
for campo in CAMPOS:
    tabela.heading(campo, text=campo)
    tabela.column(campo, width=120, anchor="center")
tabela.pack(fill="both", expand=True)

atualizar_lista()
janela.mainloop()
