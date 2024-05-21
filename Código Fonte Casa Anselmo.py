import tkinter as tk
from tkinter import ttk, simpledialog, Scrollbar, messagebox
import mysql.connector
import tkinter.filedialog as filedialog
import textwrap
from tkinter import font
import subprocess
from tkcalendar import DateEntry
from datetime import datetime

class SistemaDeGerenciamento:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema de Gerenciamento")
        self.janela.configure(bg="#120a8f")  # Cor de fundo mais clara


        self.estilo = ttk.Style()
        self.estilo.configure('TButton', padding=6, relief="flat", background="#4CAF50", foreground="white")

        self.adicionar_componentes()

    def adicionar_componentes(self):
        tamanho_botao = 25
        altura_botao = 5

        label_cabecalho = tk.Label(self.janela, text="Casa de Orações Irmão Anselmo", font=("Arial", 25, "bold"),
                                   bg="#3498db", fg="white", pady=20)  # Cor de fundo azul
        label_cabecalho.grid(row=0, column=0, columnspan=10, sticky="ew")

        # Configura a coluna para expandir-se no centro
        self.janela.columnconfigure(0, weight=1)

        # Frame para os botões
        frame_botoes = tk.Frame(self.janela, bg="#120a8f")  # Cor de fundo cinza claro
        frame_botoes.grid(row=1, column=0, columnspan=2, pady=40)

        # Estilo para os botões
        estilo_botao = {"width": tamanho_botao, "bd": 2, "bg": "#3498db", "fg": "white", "font": ("Arial", 15, "bold")}

        botao_familias = tk.Button(frame_botoes, text="FAMÍLIAS", command=self.exibir_tela_familias, **estilo_botao)
        botao_familias.grid(row=0, column=0, padx=10, pady=10)
        botao_alimentos = tk.Button(frame_botoes, text="ALIMENTOS",
                                    command=self.exibir_tela_alimentos, **estilo_botao)
        botao_alimentos.grid(row=0, column=1, padx=10, pady=10)
        botao_entrega = tk.Button(frame_botoes, text="ENTREGA DE\nCESTAS BÁSICAS",
                                       command=self.exibir_tela_entrega, **estilo_botao)
        botao_entrega.grid(row=0, column=2, padx=10, pady=10)

        botao_voluntarios = tk.Button(frame_botoes, text="VOLUNTÁRIOS", command=self.exibir_tela_voluntarios,
                                      **estilo_botao)
        botao_voluntarios.grid(row=1, column=0, padx=10, pady=10)
        botao_inserir = tk.Button(frame_botoes, text="DOADORES", command=self.exibir_tela_doadores, **estilo_botao)
        botao_inserir.grid(row=1, column=1, padx=10, pady=10)
        botao_diretoria = tk.Button(frame_botoes, text="DIRETORIA\nADMINSTRAÇÃO", command=self.exibir_tela_diretoria, **estilo_botao)
        botao_diretoria.grid(row=1, column=2, padx=10, pady=10)

        # Ajusta a altura dos botões
        for botao in [botao_familias, botao_alimentos, botao_entrega, botao_voluntarios, botao_inserir,
                      botao_diretoria]:
            botao.config(height=altura_botao)


    def exibir_tela_familias(self):
        janela_familias = tk.Toplevel(self.janela)
        app_familias = TelaFamilias(janela_familias)
        janela_familias.resizable(False, False)  # Impede a maximização da tela de famílias

    def exibir_tela_diretoria(self):
        janela_diretoria = tk.Toplevel(self.janela)
        app_familias = TelaDiretoria(janela_diretoria)
        janela_diretoria.resizable(False, False)  # Impede a maximização da tela de diretoria

    def exibir_tela_voluntarios(self):
        janela_voluntarios = tk.Toplevel(self.janela)
        app_familias = TelaVoluntarios(janela_voluntarios)
        janela_voluntarios.resizable(False, False)  # Impede a maximização da tela de voluntarios

    def exibir_tela_doadores(self):
        janela_doadores = tk.Toplevel(self.janela)
        app_familias = TelaDoadores(janela_doadores)
        janela_doadores.resizable(False, False)  # Impede a maximização da tela de doadores

    def exibir_tela_alimentos(self):
        janela_alimentos = tk.Toplevel(self.janela)
        app_alimentos = TelaAlimentos(janela_alimentos)
        janela_alimentos.resizable(False, False)  # Impede a maximização da tela de doadores

    def exibir_tela_entrega(self):
        janela_entrega = tk.Toplevel(self.janela)
        app_entrega = TelaEntrega(janela_entrega)
        janela_entrega.resizable(False, False)  # Impede a maximização da tela de doadores

class TelaFamilias:
    HOST = "localhost"
    USUARIO = "nil"
    SENHA = "1234"
    BANCO_DE_DADOS = "db1"

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Famílias")

        #  Grade para exibir os dados
        colunas = ("N°", "NOME", "TELEFONE", "ENDEREÇO", "OBSERVAÇÕES")
        self.grade = ttk.Treeview(self.janela, columns=colunas, show="headings", height=15)

        # Configura as colunas
        for coluna in colunas:
            self.grade.heading(coluna, text=coluna)
            self.grade.column(coluna, anchor="center")

        # Barra de rolagem vertical
        self.barra_rolagem_vertical = Scrollbar(self.janela, orient="vertical", command=self.grade.yview)
        self.barra_rolagem_vertical.pack(side="right", fill="y")
        self.grade.configure(yscrollcommand=self.barra_rolagem_vertical.set)

        # Adiciona a grade à janela
        self.grade.pack(padx=10, pady=10)

        # Adiciona botões e rótulos
        self.adicionar_componentes()

        # Preenche a grade inicialmente e atualiza a quantidade de famílias
        self.preencher_grade()
        self.atualizar_quantidade_familias()

    def adicionar_componentes(self):
        fonte_negrito = font.Font(family="Arial", size=16, weight="bold")
        rotulo_familias = tk.Label(self.janela, text="FAMÍLIAS", font=fonte_negrito)
        rotulo_familias.pack(side="top", pady=10)

        # Botão para atualizar os dados e a quantidade de famílias
        botao_atualizar = tk.Button(self.janela, text="Atualizar Lista",
                                    command=lambda: [self.preencher_grade(), self.atualizar_quantidade_familias()])
        botao_atualizar.pack(side="left", padx=10, pady=5)

        #  Botão para localizar um registro e atualizar a quantidade de famílias
        botao_localizar = tk.Button(self.janela, text="Localizar Família",
                                    command=lambda: [self.localizar_registro(), self.atualizar_quantidade_familias()])
        botao_localizar.pack(side="left", padx=10, pady=5)

        # Botão para editar uma família
        botao_editar = tk.Button(self.janela, text="Editar Família", command=self.editar_dados)
        botao_editar.pack(side="left", padx=10, pady=5)

        # Botão para visualizar detalhes de uma família
        botao_detalhes = tk.Button(self.janela, text="Visualizar Família", command=self.visualizar_detalhes)
        botao_detalhes.pack(side="left", padx=10, pady=5)

        # Rótulo para exibir a quantidade de famílias
        self.rotulo_quantidade = tk.Label(self.janela, text="Quantidade de Famílias: 0")
        self.rotulo_quantidade.pack(side="right", padx=40, pady=40)

        # Botão para inserir dados e atualizar a quantidade de famílias
        botao_inserir = tk.Button(self.janela, text="Inserir Família",
                                  command=lambda: [self.inserir_familia(), self.atualizar_quantidade_familias()])

        # Opções visuais para destacar o botão
        botao_inserir.config(bg="cyan", fg="black",
                             relief=tk.RAISED)

        botao_inserir.pack(side="right", padx=10, pady=5)

    def obter_input_usuario(self, titulo, mensagem):
        return simpledialog.askstring(titulo, mensagem)

    def obter_dados(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT * FROM familias")
                    dados = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")

        return dados

    def preencher_grade(self):
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados
        for linha in dados:
            self.grade.insert("", "end", values=linha)

    def inserir_familia(self):
        janela_inserir = tk.Toplevel(self.janela)
        janela_inserir.title("Inserir Família")
        janela_inserir.resizable(False, False)

        novo_nome = tk.StringVar()
        novo_telefone = tk.StringVar()
        novo_endereco = tk.StringVar()
        novas_observacoes = tk.StringVar()

        tk.Label(janela_inserir, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Endereço:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_endereco, width=80).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_inserir, wrap=tk.WORD, width=40, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def realizar_insercao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "INSERT INTO familias (nome, telefone, endereco, observacoes) VALUES (%s, %s, %s, %s)"
                        valores = (novo_nome.get(), novo_telefone.get(), novo_endereco.get(), novas_observacoes_texto)
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Inserção", f"Erro ao inserir dados: {e}")

            self.preencher_grade()
            janela_inserir.destroy()

        tk.Button(janela_inserir, text="Inserir", command=realizar_insercao).grid(row=4, column=0, columnspan=2,
                                                                                  pady=10)

    def localizar_registro(self):
        criterio_busca = self.obter_input_usuario("Localizar Registro", "Digite o critério de busca:")
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados que atendem ao critério de busca
        for linha in dados:
            if criterio_busca is not None and criterio_busca.lower() in str(linha).lower():
                self.grade.insert("", "end", values=linha)

    def obter_quantidade_familias(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM familias")
                    quantidade = cursor.fetchone()[0]

        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Consulta", f"Erro ao obter quantidade de famílias: {e}")

        return quantidade

    def atualizar_quantidade_familias(self):
        quantidade = self.obter_quantidade_familias()
        self.rotulo_quantidade.config(text=f"Quantidade de Famílias: {quantidade}")

    def editar_dados(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Edição de Dados", "Selecione uma família para editar.", parent=self.janela)
            return

        dados_familia = self.grade.item(item_selecionado)['values']

        janela_edicao = tk.Toplevel(self.janela)
        janela_edicao.title("Editar Família")
        janela_edicao.resizable(False, False)

        novo_nome = tk.StringVar(value=dados_familia[1])
        novo_telefone = tk.StringVar(value=dados_familia[2])
        novo_endereco = tk.StringVar(value=dados_familia[3])
        novas_observacoes = tk.StringVar(value=dados_familia[4])

        tk.Label(janela_edicao, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Endereço:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_endereco, width=80).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_edicao, wrap=tk.WORD, width=80, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def aplicar_edicao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "UPDATE familias SET nome=%s, telefone=%s, endereco=%s, observacoes=%s WHERE id=%s"
                        valores = (novo_nome.get(), novo_telefone.get(), novo_endereco.get(), novas_observacoes_texto,
                                   dados_familia[0])
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Edição", f"Erro ao editar dados: {e}")

            self.preencher_grade()
            janela_edicao.destroy()

        # Botão para aplicar a edição
        tk.Button(janela_edicao, text="Gravar Edição", command=aplicar_edicao).grid(row=4, column=0, columnspan=2,
                                                                                    pady=10)

    def visualizar_detalhes(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Visualização de Detalhes", "Selecione uma família para visualizar detalhes.", parent=self.janela)
            return

        dados_familia = self.grade.item(item_selecionado)['values']

        janela_detalhes = tk.Toplevel(self.janela)
        janela_detalhes.title("Detalhes da Família")
        janela_detalhes.resizable(False, False)

        rotulos_detalhes = ["ID", "Nome", "Telefone", "Endereço", "Observações"]
        for i, rotulo in enumerate(rotulos_detalhes):
            tk.Label(janela_detalhes, text=rotulo).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            if rotulo == "Observações":
                observacoes = dados_familia[i]
                observacoes_text = tk.Text(janela_detalhes, wrap=tk.WORD, width=80, height=10)
                observacoes_text.insert(tk.END, "\n".join(textwrap.wrap(observacoes, width=40)))
                observacoes_text.config(state=tk.DISABLED)
                observacoes_text.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            else:
                tk.Label(janela_detalhes, text=dados_familia[i]).grid(row=i, column=1, sticky="w", padx=5, pady=5)

class TelaDiretoria:
    HOST = "localhost"
    USUARIO = "nil"
    SENHA = "1234"
    BANCO_DE_DADOS = "db1"

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Diretoria")

        # Grade para exibir os dados
        colunas = ("N°", "NOME", "TELEFONE", "CARGO", "OBSERVAÇÕES")
        self.grade = ttk.Treeview(self.janela, columns=colunas, show="headings", height=15)

        # Configurar as colunas
        for coluna in colunas:
            self.grade.heading(coluna, text=coluna)
            self.grade.column(coluna, anchor="center")

        # Barra de rolagem vertical
        self.barra_rolagem_vertical = Scrollbar(self.janela, orient="vertical", command=self.grade.yview)
        self.barra_rolagem_vertical.pack(side="right", fill="y")
        self.grade.configure(yscrollcommand=self.barra_rolagem_vertical.set)

        # Adicionar a grade à janela
        self.grade.pack(padx=10, pady=10)

        # Adicionar botões e rótulos
        self.adicionar_componentes()

        # Preencher a grade inicialmente e atualizar a quantidade de diretores
        self.preencher_grade()
        self.atualizar_quantidade_diretores()

    def adicionar_componentes(self):
        # Rótulo DIRETORIA
        fonte_negrito = font.Font(family="Arial", size=16, weight="bold")
        rotulo_diretoria = tk.Label(self.janela, text="DIRETORIA", font=fonte_negrito)
        rotulo_diretoria.pack(side="top", pady=10)

        # Frame para os botões de ação
        frame_acoes = tk.Frame(self.janela)
        frame_acoes.pack(side="top", pady=5)

        # Botão para atualizar os dados e a quantidade de diretores
        botao_atualizar = tk.Button(frame_acoes, text="Atualizar Lista",
                                    command=lambda: [self.preencher_grade(), self.atualizar_quantidade_diretores()])
        botao_atualizar.pack(side="left", padx=10)

        # Botão para localizar um registro e atualizar a quantidade de diretores
        botao_localizar = tk.Button(frame_acoes, text="Localizar Diretor",
                                    command=lambda: [self.localizar_registro(), self.atualizar_quantidade_diretores()])
        botao_localizar.pack(side="left", padx=10)

        # Botão para editar um diretor
        botao_editar = tk.Button(frame_acoes, text="Editar Diretor", command=self.editar_dados)
        botao_editar.pack(side="left", padx=10)

        # Botão para visualizar detalhes de um diretor
        botao_detalhes = tk.Button(frame_acoes, text="Visualizar Diretor", command=self.visualizar_detalhes)
        botao_detalhes.pack(side="left", padx=10)

        # Botão para inserir dados e atualizar a quantidade de diretores
        botao_inserir = tk.Button(frame_acoes, text="Inserir DIRETOR",
                                  command=lambda: [self.inserir_diretor(), self.atualizar_quantidade_diretores()])
        botao_inserir.config(bg="pink", fg="black", relief=tk.RAISED)
        botao_inserir.pack(side="left", padx=10)

        # Frame para os botões de backup
        frame_backup = tk.Frame(self.janela)
        frame_backup.pack(side="top", pady=5)

        # Botão para efetuar backup
        botao_backup = tk.Button(frame_backup , text="Efetuar Backup", command=self.exportar_backup)
        botao_backup.pack(side="left", padx=10)

        # Botão para restaurar backup
        botao_restaurar = tk.Button(frame_backup, text="Restaurar Backup", command=self.restaurar_backup)
        botao_restaurar.pack(side="left", padx=10)

        # Rótulo para exibir a quantidade de diretores
        self.rotulo_quantidade = tk.Label(self.janela, text="Quantidade de Diretores: 0")
        self.rotulo_quantidade.pack(side="bottom", padx=40, pady=10)

    def exportar_backup(self):
        try:
            # Definir o nome do arquivo de backup
            nome_arquivo = "SistGer_BackUP.sql"

            # Concatenar o nome do arquivo com o diretório onde será salvo
            local_backup = filedialog.asksaveasfilename(parent=self.janela , defaultextension=".sql" ,
                                                        initialfile=nome_arquivo)

            if local_backup:
                # Executar o comando mysqldump para exportar o backup do banco de dados
                subprocess.run(
                    ["mysqldump", "-h", self.HOST, "-u", self.USUARIO , "-p" + self.SENHA , self.BANCO_DE_DADOS ,
                     "--result-file=" + local_backup])
                messagebox.showinfo("Backup realizado", "Backup do banco de dados realizado com sucesso.", parent=self.janela)
        except Exception as e:
            messagebox.showerror("Erro ao realizar o backup", str(e))

    import subprocess

    def restaurar_backup(self):
        try:
            # Solicitar a senha ao usuário
            senha = simpledialog.askstring("Senha" , "Insira a senha para prosseguir:")

            # Verificar se a senha inserida está correta
            if senha == "2304":
                # Solicitar ao usuário o local do arquivo de backup
                arquivo_backup = filedialog.askopenfilename(parent=self.janela , defaultextension=".sql")

                if arquivo_backup:
                    # Abrir o arquivo de backup
                    with open(arquivo_backup , 'rb') as f:
                        # Executar o comando mysql para restaurar o backup
                        subprocess.run(
                            ["mysql" , "-h" , self.HOST , "-u" , "nil" , "-p1234" , self.BANCO_DE_DADOS] ,
                            stdin=f ,
                            text=True ,
                            check=True
                        )
                        messagebox.showinfo("Backup restaurado", "Backup do banco de dados restaurado com sucesso.", parent=self.janela)
            else:
                messagebox.showerror("Erro ao restaurar o backup" , "Senha incorreta.", parent=self.janela)
        except Exception as e:
            messagebox.showerror("Erro ao restaurar o backup" , str(e) , parent=self.janela)

    def obter_input_usuario(self, titulo, mensagem):
        return simpledialog.askstring(titulo, mensagem)

    def obter_dados(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT * FROM diretoria")
                    dados = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")

        return dados

    def preencher_grade(self):
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados
        for linha in dados:
            self.grade.insert("", "end", values=linha)

    def inserir_diretor(self):
        janela_inserir = tk.Toplevel(self.janela)
        janela_inserir.title("Inserir Diretor")
        janela_inserir.resizable(False, False)

        novo_nome = tk.StringVar()
        novo_telefone = tk.StringVar()
        novo_cargo = tk.StringVar()
        novas_observacoes = tk.StringVar()

        tk.Label(janela_inserir, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Cargo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_cargo, width=80).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_inserir, wrap=tk.WORD, width=40, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def realizar_insercao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "INSERT INTO diretoria (nome, telefone, cargo, observacoes) VALUES (%s, %s, %s, %s)"
                        valores = (novo_nome.get(), novo_telefone.get(), novo_cargo.get(), novas_observacoes_texto)
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Inserção", f"Erro ao inserir dados: {e}")

            self.preencher_grade()
            janela_inserir.destroy()

        tk.Button(janela_inserir, text="Inserir", command=realizar_insercao).grid(row=4, column=0, columnspan=2, pady=10)

    def localizar_registro(self):
        criterio_busca = self.obter_input_usuario("Localizar Registro", "Digite o critério de busca:")
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados que atendem ao critério de busca
        for linha in dados:
            if criterio_busca is not None and criterio_busca.lower() in str(linha).lower():
                self.grade.insert("", "end", values=linha)

    def obter_quantidade_diretores(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM diretoria")
                    quantidade = cursor.fetchone()[0]

        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Consulta", f"Erro ao obter quantidade de famílias: {e}")

        return quantidade

    def atualizar_quantidade_diretores(self):
        quantidade = self.obter_quantidade_diretores()
        self.rotulo_quantidade.config(text=f"Quantidade de Diretores: {quantidade}")

    def editar_dados(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Edição de Dados", "Selecione uma diretor para editar.", parent=self.janela)
            return

        dados_diretor = self.grade.item(item_selecionado)['values']

        janela_edicao = tk.Toplevel(self.janela)
        janela_edicao.title("Editar Diretor")
        janela_edicao.resizable(False, False)

        novo_nome = tk.StringVar(value=dados_diretor[1])
        novo_telefone = tk.StringVar(value=dados_diretor[2])
        novo_cargo = tk.StringVar(value=dados_diretor[3])
        novas_observacoes = tk.StringVar(value=dados_diretor[4])

        tk.Label(janela_edicao, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Cargo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_cargo, width=80).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_edicao, wrap=tk.WORD, width=80, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def aplicar_edicao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "UPDATE diretoria SET nome=%s, telefone=%s, cargo=%s, observacoes=%s WHERE id=%s"
                        valores = (novo_nome.get(), novo_telefone.get(), novo_cargo.get(), novas_observacoes_texto,
                                   dados_diretor[0])
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Edição", f"Erro ao editar dados: {e}")

            self.preencher_grade()
            janela_edicao.destroy()

        # Botão para aplicar a edição
        tk.Button(janela_edicao, text="Gravar Edição", command=aplicar_edicao).grid(row=4, column=0, columnspan=2,
                                                                                    pady=10)

    def visualizar_detalhes(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Visualização de Detalhes", "Selecione uma diretor para visualizar detalhes.", parent=self.janela)
            return

        dados_diretor = self.grade.item(item_selecionado)['values']

        janela_detalhes = tk.Toplevel(self.janela)
        janela_detalhes.title("Detalhes do Diretor")
        janela_detalhes.resizable(False, False)

        rotulos_detalhes = ["ID", "Nome", "Telefone", "Cargo", "Observações"]
        for i, rotulo in enumerate(rotulos_detalhes):
            tk.Label(janela_detalhes, text=rotulo).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            if rotulo == "Observações":
                observacoes = dados_diretor[i]
                observacoes_text = tk.Text(janela_detalhes, wrap=tk.WORD, width=80, height=10)
                observacoes_text.insert(tk.END, "\n".join(textwrap.wrap(observacoes, width=40)))
                observacoes_text.config(state=tk.DISABLED)
                observacoes_text.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            else:
                tk.Label(janela_detalhes, text=dados_diretor[i]).grid(row=i, column=1, sticky="w", padx=5, pady=5)

class TelaVoluntarios:
    HOST = "localhost"
    USUARIO = "nil"
    SENHA = "1234"
    BANCO_DE_DADOS = "db1"

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Voluntários")

        # Grade para exibir os dados
        colunas = ("id", "NOME", "TELEFONE", "OBSERVAÇÕES")
        self.grade = ttk.Treeview(self.janela, columns=colunas, show="headings", height=15)

        # Configurar as colunas
        for coluna in colunas:
            self.grade.heading(coluna, text=coluna)

        # Atribuir larguras específicas para cada coluna
        largura_id = 1
        largura_NOME = (self.janela.winfo_width() - largura_id) // 3
        largura_TELEFONE = largura_NOME
        largura_OBSERVAÇÕES = self.janela.winfo_width() - largura_id - largura_NOME - largura_TELEFONE

        self.grade.column("id", anchor="center", width=largura_id)
        self.grade.column("NOME", anchor="center", width=largura_NOME)
        self.grade.column("TELEFONE", anchor="center", width=largura_TELEFONE)
        self.grade.column("OBSERVAÇÕES", anchor="center", width=largura_OBSERVAÇÕES)

        # Barra de rolagem vertical
        self.barra_rolagem_vertical = Scrollbar(self.janela, orient="vertical", command=self.grade.yview)
        self.barra_rolagem_vertical.pack(side="right", fill="y")

        # Adicionar a grade à janela
        self.grade.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.grade.configure(yscrollcommand=self.barra_rolagem_vertical.set)

        # Adicionar botões e rótulos
        self.adicionar_componentes()

        # Preencher a grade inicialmente e atualizar a quantidade de famílias
        self.preencher_grade()
        self.atualizar_quantidade_voluntarios()

    def adicionar_componentes(self):
        fonte_negrito = font.Font(family="Arial", size=16, weight="bold")


        # Botão para atualizar os dados e a quantidade de voluntários
        botao_atualizar = tk.Button(self.janela, text="Atualizar Lista",
                                    command=lambda: [self.preencher_grade(), self.atualizar_quantidade_voluntarios()])
        botao_atualizar.pack(side="left", padx=10, pady=5)

        # Botão para localizar um registro e atualizar a quantidade de voluntários
        botao_localizar = tk.Button(self.janela, text="Localizar Voluntários",
                                    command=lambda: [self.localizar_registro(), self.atualizar_quantidade_voluntarios()])
        botao_localizar.pack(side="left", padx=10, pady=5)

        # Botão para editar um voluntário
        botao_editar = tk.Button(self.janela, text="Editar Voluntário", command=self.editar_dados)
        botao_editar.pack(side="left", padx=10, pady=5)

        # Botão para visualizar detalhes de um voluntário
        botao_detalhes = tk.Button(self.janela, text="Visualizar Voluntário", command=self.visualizar_detalhes)
        botao_detalhes.pack(side="left", padx=10, pady=5)

        # Criar um rótulo para exibir a quantidade de voluntários
        self.rotulo_quantidade = tk.Label(self.janela, text="")
        self.rotulo_quantidade.pack(side="right", padx=40, pady=40)

        # Botão para inserir dados e atualizar a quantidade de voluntários
        botao_inserir = tk.Button(self.janela, text="INSERIR VOLUNTÁRIO",
                                  command=lambda: [self.inserir_voluntario(), self.atualizar_quantidade_voluntarios()])

        # Ajustar opções visuais para destacar o botão
        botao_inserir.config(bg="yellow", fg="black", relief=tk.RAISED)
        botao_inserir.pack(side="right", padx=1, pady=5)


    def obter_input_usuario(self, titulo, mensagem):
        return simpledialog.askstring(titulo, mensagem)

    def obter_dados(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT id, nome, telefone, observacoes FROM voluntarios")
                    dados = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")

        return dados

    def preencher_grade(self):
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados
        for linha in dados:
            self.grade.insert("", "end", values=linha)

    def inserir_voluntario(self):
        janela_inserir = tk.Toplevel(self.janela)
        janela_inserir.title("Inserir Voluntário")
        janela_inserir.resizable(False, False)

        novo_nome = tk.StringVar()
        novo_telefone = tk.StringVar()
        novas_observacoes = tk.StringVar()

        tk.Label(janela_inserir, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_inserir, wrap=tk.WORD, width=40, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def realizar_insercao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "INSERT INTO voluntarios (nome, telefone, observacoes) VALUES (%s, %s, %s)"
                        valores = (novo_nome.get(), novo_telefone.get(), novas_observacoes_texto)
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Inserção", f"Erro ao inserir dados: {e}")

            self.preencher_grade()
            janela_inserir.destroy()

        tk.Button(janela_inserir, text="Inserir", command=realizar_insercao).grid(row=4, column=0, columnspan=2,
                                                                                  pady=10)

    def localizar_registro(self):
        criterio_busca = self.obter_input_usuario("Localizar Registro", "Digite o critério de busca:")
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados que atendem ao critério de busca
        for linha in dados:
            if criterio_busca is not None and criterio_busca.lower() in str(linha).lower():
                self.grade.insert("", "end", values=linha)

    def obter_quantidade_voluntarios(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM voluntarios")
                    quantidade = cursor.fetchone()[0]

        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Consulta", f"Erro ao obter quantidade de voluntários: {e}")

        return quantidade

    def atualizar_quantidade_voluntarios(self, quantidade=None):
        if quantidade is None:
            quantidade = self.obter_quantidade_voluntarios()

        self.rotulo_quantidade.config(text=f"Quantidade de Voluntários: {quantidade}")

    def editar_dados(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Edição de Dados", "Selecione um voluntário para editar.", parent=self.janela)
            return

        dados_voluntario = self.grade.item(item_selecionado)['values']

        janela_edicao = tk.Toplevel(self.janela)
        janela_edicao.title("Editar Voluntário")
        janela_edicao.resizable(False, False)

        novo_nome = tk.StringVar(value=dados_voluntario[1])
        novo_telefone = tk.StringVar(value=dados_voluntario[2])
        novas_observacoes = tk.StringVar(value=dados_voluntario[3])

        tk.Label(janela_edicao, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_edicao, wrap=tk.WORD, width=80, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def aplicar_edicao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "UPDATE voluntarios SET nome=%s, telefone=%s, observacoes=%s WHERE id=%s"
                        valores = (novo_nome.get(), novo_telefone.get(), novas_observacoes_texto,
                                   dados_voluntario[0])
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Edição", f"Erro ao editar dados: {e}")

            self.preencher_grade()
            janela_edicao.destroy()

        # Botão para aplicar a edição
        tk.Button(janela_edicao, text="Gravar Edição", command=aplicar_edicao).grid(row=4, column=0, columnspan=2,
                                                                                    pady=10)

    def visualizar_detalhes(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Visualização de Detalhes", "Selecione um voluntário para visualizar detalhes.", parent=self.janela)
            return

        dados_voluntario = self.grade.item(item_selecionado)['values']

        janela_detalhes = tk.Toplevel(self.janela)
        janela_detalhes.title("Detalhes do Voluntário")
        janela_detalhes.resizable(False, False)

        rotulos_detalhes = ["ID", "Nome", "Telefone", "Observações"]
        for i, rotulo in enumerate(rotulos_detalhes):
            tk.Label(janela_detalhes, text=rotulo).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            if rotulo == "Observações":
                observacoes = dados_voluntario[i]
                observacoes_text = tk.Text(janela_detalhes, wrap=tk.WORD, width=80, height=10)
                observacoes_text.insert(tk.END, "\n".join(textwrap.wrap(observacoes, width=40)))
                observacoes_text.config(state=tk.DISABLED)
                observacoes_text.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            else:
                tk.Label(janela_detalhes, text=dados_voluntario[i]).grid(row=i, column=1, sticky="w", padx=5, pady=5)

class TelaDoadores:
    HOST = "localhost"
    USUARIO = "nil"
    SENHA = "1234"
    BANCO_DE_DADOS = "db1"

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Doadores")

        # Crade para exibir os dados
        colunas = ("N°", "NOME", "TELEFONE", "OBSERVAÇÕES")
        self.grade = ttk.Treeview(self.janela, columns=colunas, show="headings", height=15)

        # Configurar as colunas
        for coluna in colunas:
            self.grade.heading(coluna, text=coluna)
            self.grade.column(coluna, anchor="center")

        # Barra de rolagem vertical
        self.barra_rolagem_vertical = Scrollbar(self.janela, orient="vertical", command=self.grade.yview)
        self.barra_rolagem_vertical.pack(side="right", fill="y")
        self.grade.configure(yscrollcommand=self.barra_rolagem_vertical.set)

        # Adicionar a grade à janela
        self.grade.pack(padx=10, pady=10)

        # Adicionar botões e rótulos
        self.adicionar_componentes()

        # Preencher a grade inicialmente e atualizar a quantidade de doadores
        self.preencher_grade()
        self.atualizar_quantidade_doadores()

    def adicionar_componentes(self):
       # Adicionar rotulo doadores
        fonte_negrito = font.Font(family="Arial", size=16, weight="bold")
        rotulo_doadores = tk.Label(self.janela, text="DOADORES", font=fonte_negrito)
        rotulo_doadores.pack(side="top", pady=10)

        # Botão para atualizar os dados e a quantidade de doadores
        botao_atualizar = tk.Button(self.janela, text="Atualizar Lista",
                                    command=lambda: [self.preencher_grade(), self.atualizar_quantidade_doadores()])
        botao_atualizar.pack(side="left", padx=10, pady=5)

        # Botão para localizar um registro e atualizar a quantidade de doadores
        botao_localizar = tk.Button(self.janela, text="Localizar Doador",
                                    command=lambda: [self.localizar_registro(), self.atualizar_quantidade_doadores()])
        botao_localizar.pack(side="left", padx=10, pady=5)

        # Botão para editar um doador
        botao_editar = tk.Button(self.janela, text="Editar Doador", command=self.editar_dados)
        botao_editar.pack(side="left", padx=10, pady=5)

        # Botão para visualizar detalhes de um doador
        botao_detalhes = tk.Button(self.janela, text="Visualizar Doadores", command=self.visualizar_detalhes)
        botao_detalhes.pack(side="left", padx=10, pady=5)

        # Criar um rótulo para exibir a quantidade de doadores
        self.rotulo_quantidade = tk.Label(self.janela, text="Quantidade de Doadores: 0")
        self.rotulo_quantidade.pack(side="right", padx=40, pady=40)

        # Botão para inserir dados e atualizar a quantidade de doadores
        botao_inserir = tk.Button(self.janela, text="Inserir Doador",
                                  command=lambda: [self.inserir_doador(), self.atualizar_quantidade_doadores()])

        # Opções visuais para destacar o botão
        botao_inserir.config(bg="yellow", fg="black",
                             relief=tk.RAISED)
        botao_inserir.pack(side="right", padx=10, pady=5)

    def obter_input_usuario(self, titulo, mensagem):
        return simpledialog.askstring(titulo, mensagem)

    def obter_dados(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT * FROM doadores")
                    dados = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")

        return dados

    def preencher_grade(self):
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados
        for linha in dados:
            self.grade.insert("", "end", values=linha)

    def inserir_doador(self):
        janela_inserir = tk.Toplevel(self.janela)
        janela_inserir.title("Inserir doador")
        janela_inserir.resizable(False, False)

        novo_nome = tk.StringVar()
        novo_telefone = tk.StringVar()
        novas_observacoes = tk.StringVar()

        tk.Label(janela_inserir, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_inserir, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_inserir, wrap=tk.WORD, width=40, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def realizar_insercao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "INSERT INTO doadores (nome, telefone, observacoes) VALUES (%s, %s, %s)"
                        valores = (novo_nome.get(), novo_telefone.get(), novas_observacoes_texto)
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Inserção", f"Erro ao inserir dados: {e}")

            self.preencher_grade()
            janela_inserir.destroy()

        tk.Button(janela_inserir, text="Inserir", command=realizar_insercao).grid(row=4, column=0, columnspan=2,
                                                                                  pady=10)

    def localizar_registro(self):
        criterio_busca = self.obter_input_usuario("Localizar Registro", "Digite o critério de busca:")
        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados que atendem ao critério de busca
        for linha in dados:
            if criterio_busca is not None and criterio_busca.lower() in str(linha).lower():
                self.grade.insert("", "end", values=linha)

    def obter_quantidade_doadores(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM doadores")
                    quantidade = cursor.fetchone()[0]

        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Consulta", f"Erro ao obter quantidade de doadores: {e}")

        return quantidade

    def atualizar_quantidade_doadores(self):
        quantidade = self.obter_quantidade_doadores()
        self.rotulo_quantidade.config(text=f"Quantidade de Doadores: {quantidade}")

    def editar_dados(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Edição de Dados", "Selecione um doador para editar.", parent=self.janela)
            return

        dados_doador = self.grade.item(item_selecionado)['values']

        janela_edicao = tk.Toplevel(self.janela)
        janela_edicao.title("Editar Doador")
        janela_edicao.resizable(False, False)

        novo_nome = tk.StringVar(value=dados_doador[1])
        novo_telefone = tk.StringVar(value=dados_doador[2])
        novas_observacoes = tk.StringVar(value=dados_doador[3])

        tk.Label(janela_edicao, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_nome, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_telefone, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")


        tk.Label(janela_edicao, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_edicao, wrap=tk.WORD, width=80, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def aplicar_edicao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "UPDATE doadores SET nome=%s, telefone=%s, observacoes=%s WHERE id=%s"
                        valores = (novo_nome.get(), novo_telefone.get(), novas_observacoes_texto,
                                   dados_doador[0])
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Edição", f"Erro ao editar dados: {e}")

            self.preencher_grade()
            janela_edicao.destroy()

        # Botão para aplicar a edição
        tk.Button(janela_edicao, text="Gravar Edição", command=aplicar_edicao).grid(row=4, column=0, columnspan=2,
                                                                                    pady=10)

    def visualizar_detalhes(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Visualização de Detalhes", "Selecione uma doador para visualizar detalhes.", parent=self.janela)
            return

        dados_doador = self.grade.item(item_selecionado)['values']

        janela_detalhes = tk.Toplevel(self.janela)
        janela_detalhes.title("Detalhes do Doador")
        janela_detalhes.resizable(False, False)

        rotulos_detalhes = ["ID", "Nome", "Telefone", "Observações"]
        for i, rotulo in enumerate(rotulos_detalhes):
            tk.Label(janela_detalhes, text=rotulo).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            if rotulo == "Observações":
                observacoes = dados_doador[i]
                observacoes_text = tk.Text(janela_detalhes, wrap=tk.WORD, width=80, height=10)
                observacoes_text.insert(tk.END, "\n".join(textwrap.wrap(observacoes, width=40)))
                observacoes_text.config(state=tk.DISABLED)
                observacoes_text.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            else:
                tk.Label(janela_detalhes, text=dados_doador[i]).grid(row=i, column=1, sticky="w", padx=5, pady=5)

class TelaAlimentos:
    HOST = "localhost"
    USUARIO = "nil"
    SENHA = "1234"
    BANCO_DE_DADOS = "db1"

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Alimentos")
        self.janela.geometry("1100x500")

        # Frame para conter a grade
        self.frame_grade = tk.Frame(self.janela)
        self.frame_grade.pack(expand=True, fill=tk.BOTH)

        # grade para exibir os dados
        colunas = ("id", "TIPO", "QTD", "OBSERVAÇÕES", "ATIVO")
        self.grade = ttk.Treeview(self.frame_grade, columns=colunas, show="headings", height=15)

        # Configurar as colunas
        for coluna in colunas:
            self.grade.heading(coluna, text=coluna)
            self.grade.column(coluna, anchor="center")

        # Barra de rolagem vertical
        self.barra_rolagem_vertical = Scrollbar(self.frame_grade, orient="vertical", command=self.grade.yview)
        self.barra_rolagem_vertical.pack(side="right", fill="y")
        self.grade.configure(yscrollcommand=self.barra_rolagem_vertical.set)

        # Adicionar a grade à Frame
        self.grade.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Linha para ocultar a coluna "id"
        self.grade.column("id", width=0, stretch=tk.NO)

        # Ajustar a largura das colunas "TIPO" e "OBSERVAÇÕES"
        self.grade.column("TIPO", width=100)
        self.grade.column("OBSERVAÇÕES", width=300)
        self.grade.column("QTD", width=100)

        # Adicionar botões e rótulos
        self.adicionar_componentes()

        # Preencher a grade inicialmente e atualizar a quantidade de ALIMENTOS
        self.preencher_grade_completa()
        self.atualizar_quantidade_alimentos()

    def atualizar_status_alimento(self, id_alimento, novo_status):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("UPDATE alimentos SET ativo = %s WHERE id = %s", (novo_status, id_alimento))
                    conexao.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Atualização", f"Erro ao atualizar status do alimento: {e}")

    def alternar_status_alimento(self):
        item_selecionado = self.grade.selection()
        if not item_selecionado:
            messagebox.showwarning("Alternar Status", "Selecione um alimento para ativar/inativar.", parent=self.janela)
            return

        # Obter o ID do alimento selecionado
        id_alimento = self.grade.item(item_selecionado)['values'][0]

        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    # Alternar o status diretamente no banco de dados
                    cursor.execute("UPDATE alimentos SET ativo = NOT ativo WHERE id = %s", (id_alimento,))
                    conexao.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Atualização", f"Erro ao alternar status do alimento: {e}")

        # Atualizar a grade para refletir as mudanças
        self.preencher_grade()

    def adicionar_componentes(self):
        # Adiciona rótulo para alimentos
        fonte_negrito = font.Font(family="Arial", size=16, weight="bold")
        rotulo_alimentos = tk.Label(self.janela, text="ALIMENTOS", font=fonte_negrito)
        rotulo_alimentos.pack(side="top", pady=10)

        # Botão para atualizar lista e quantidade de alimentos
        botao_atualizar = tk.Button(self.janela, text="Atualizar Lista",
                                    command=lambda: [self.preencher_grade_completa(),
                                                     self.atualizar_quantidade_alimentos()])
        botao_atualizar.pack(side="left", padx=10, pady=5)

        # Botão para localizar um alimento
        botao_localizar = tk.Button(self.janela, text="Localizar Alimento",
                                    command=lambda: [self.localizar_registro(), self.atualizar_quantidade_alimentos()])
        botao_localizar.pack(side="left", padx=10, pady=5)

        # Botão para editar um alimento
        botao_editar = tk.Button(self.janela, text="Editar Alimento", command=self.editar_dados)
        botao_editar.pack(side="left", padx=10, pady=5)

        # Botão para visualizar detalhes de um alimento
        botao_detalhes = tk.Button(self.janela, text="Visualizar Alimentos", command=self.visualizar_detalhes)
        botao_detalhes.pack(side="left", padx=10, pady=5)

        # Botão para inserir dados e atualizar a quantidade de alimentos
        botao_inserir = tk.Button(self.janela, text="INSERIR ALIMENTO",
                                  command=lambda: [self.inserir_alimento(), self.atualizar_quantidade_alimentos()])
        # Ajusta opções visuais para destacar o botão
        botao_inserir.config(bg="cyan", fg="black", relief=tk.RAISED)
        botao_inserir.pack(side="left", padx=10, pady=5)

        # Botão para ativar/desativar alimentos
        botao_ativa_desativa = tk.Button(self.janela, text="ATIVA / DESATIVA ALIMENTO", command=self.alternar_status_alimento)
        botao_ativa_desativa.pack(side="left", padx=10, pady=5)
        botao_ativa_desativa.config(bg="pink", fg="black", relief=tk.RAISED)

    def obter_input_usuario(self, titulo, mensagem):
        return simpledialog.askstring(titulo, mensagem)

    def obter_dados(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT * FROM alimentos")
                    dados = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")

        return dados

    def preencher_grade(self):
        dados = self.obter_dados()
        self.preencher_grade_completa(dados)

    def preencher_grade_completa(self, dados=None):
        if dados is None:
            dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Ordenar os dados pelo tipo de alimento (coluna 1)
        dados_ordenados = sorted(dados, key=lambda x: x[1].lower())

        # Preencher a grade com os dados ordenados
        for linha in dados_ordenados:
            # Converter o status de ativação/inativação para "Ativo" ou "Inativo"
            status = "Ativo" if linha[4] == 1 else "Inativo"
            # Define a cor da fonte para vermelho se o alimento estiver inativo
            cor_fonte = "red" if status == "Inativo" else "black"
            self.grade.insert("", "end", values=(linha[0], linha[1], linha[2], linha[3], status), tags=(status,))
            # Aplica a cor da fonte na última coluna (status)
            self.grade.tag_configure(status, foreground=cor_fonte)

    def localizar_registro(self):
        # Obter o tipo do alimento a ser localizado
        tipo_alimento = self.obter_input_usuario("Localizar Alimento",
                                                 "Digite parte do tipo de alimento a ser localizado:")

        if tipo_alimento:
            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        # Buscar todos os registros
                        cursor.execute("SELECT * FROM alimentos")
                        todos_os_dados = cursor.fetchall()

                        # Filtrar registros com base no tipo de alimento
                        resultado = [linha for linha in todos_os_dados if tipo_alimento.lower() in linha[1].lower()]

                        if resultado:
                            self.preencher_grade_completa(resultado)
                        else:
                            messagebox.showinfo("Localizar Alimento",
                                                f"Nenhum registro encontrado para o tipo: {tipo_alimento}")

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Consulta", f"Erro ao localizar alimento: {e}")

    def inserir_alimento(self):
        janela_inserir = tk.Toplevel(self.janela)
        janela_inserir.title("Inserir Alimento")
        janela_inserir.resizable(False, False)

        novo_tipo = tk.StringVar()
        novo_qtd = tk.StringVar()

        # Adicionar um menu suspenso para escolher o tipo de alimento
        tk.Label(janela_inserir, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        opcoes_tipos = ["AÇÚCAR","ARROZ", "BOLACHA", "CAFÉ", "FARINHA DE MILHO", "FEIJÃO", "LEITE", "MACARRÃO", "MOLHO DE TOMATE",
                        "SAL", "OLEO", "OUTROS"]
        menu_tipo = ttk.Combobox(janela_inserir, textvariable=novo_tipo, values=opcoes_tipos, state="readonly")
        menu_tipo.set("Selecione um Alimento")  # Define "SELECIONE" como valor inicial
        menu_tipo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Adicionar mensagem sobre observações
        mensagem_observacoes = tk.Label(janela_inserir,
                                        text="Para inserir observações, utilize a opção\n'EDITAR ALIMENTO'")
        mensagem_observacoes.grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(janela_inserir, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_inserir, textvariable=novo_qtd, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        def realizar_insercao():
            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        cursor.execute("SELECT * FROM alimentos WHERE tipo = %s", (novo_tipo.get(),))
                        resultado = cursor.fetchone()
                        cursor.fetchall()  # Garante que todos os resultados sejam lidos

                        if resultado and novo_tipo.get() == 'OUTROS':
                            # Define a janela principal como superior
                            self.janela.attributes('-topmost', 1)

                            confirmacao = messagebox.askquestion(
                                "Duplicar 'OUTROS'",
                                "Já existe um registro para 'OUTROS'. Deseja duplicar?",
                                parent=self.janela
                            )

                            # Redefine o atributo após a caixa de diálogo ser fechada
                            self.janela.attributes('-topmost', 0)

                            if confirmacao == 'yes':
                                consulta = "INSERT INTO alimentos (tipo, qtd) VALUES (%s, %s)"
                                valores = (novo_tipo.get(), novo_qtd.get())
                            else:
                                return  # Retorna aqui para evitar a execução do código abaixo
                        elif resultado:
                            consulta = "UPDATE alimentos SET qtd = qtd + %s WHERE tipo = %s"
                            valores = (novo_qtd.get(), novo_tipo.get())
                        else:
                            consulta = "INSERT INTO alimentos (tipo, qtd) VALUES (%s, %s)"
                            valores = (novo_tipo.get(), novo_qtd.get())

                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                if e.errno == mysql.connector.errorcode.ER_NO_DEFAULT_FOR_FIELD:
                    mensagem_erro = "Erro ao inserir dados: Selecione a quantidade do Alimento."
                else:
                    mensagem_erro = f"Erro ao inserir dados: {e}"

                janela_erro = tk.Toplevel(self.janela)
                janela_erro.title("Erro de Inserção")

                tk.Label(janela_erro, text=mensagem_erro, padx=20, pady=20).pack()
                tk.Button(janela_erro, text="OK", command=janela_erro.destroy).pack()

            self.preencher_grade()
            janela_inserir.destroy()

        tk.Button(janela_inserir, text="Inserir", command=realizar_insercao).grid(row=3, column=0, columnspan=2)

    def obter_quantidade_alimentos(self):
        try:
            with mysql.connector.connect(
                    host=self.HOST,
                    user=self.USUARIO,
                    password=self.SENHA,
                    database=self.BANCO_DE_DADOS
            ) as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM alimentos")
                    quantidade = cursor.fetchone()[0]

        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Consulta", f"Erro ao obter quantidade de alimentos: {e}")

        return quantidade

    def atualizar_quantidade_alimentos(self):
        quantidade = self.obter_quantidade_alimentos()

    def editar_dados(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Edição de Dados", "Selecione um alimento para editar.", parent=self.janela)
            return

        dados_alimento = self.grade.item(item_selecionado)['values']

        janela_edicao = tk.Toplevel(self.janela)
        janela_edicao.title("Editar Alimentos")
        janela_edicao.resizable(False, False)

        novo_tipo = tk.StringVar(value=dados_alimento[1])
        novo_qtd = tk.StringVar(value=dados_alimento[2])
        novas_observacoes = tk.StringVar(value=dados_alimento[3])

        tk.Label(janela_edicao, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_tipo, width=80).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="QTD:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(janela_edicao, textvariable=novo_qtd, width=80).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_edicao, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        campo_observacoes = tk.Text(janela_edicao, wrap=tk.WORD, width=80, height=10)
        campo_observacoes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        campo_observacoes.insert(tk.END, novas_observacoes.get())

        def aplicar_edicao():
            novas_observacoes_texto = campo_observacoes.get("1.0", tk.END).strip()

            try:
                with mysql.connector.connect(
                        host=self.HOST,
                        user=self.USUARIO,
                        password=self.SENHA,
                        database=self.BANCO_DE_DADOS
                ) as conexao:
                    with conexao.cursor() as cursor:
                        consulta = "UPDATE alimentos SET tipo=%s, qtd=%s, observacoes=%s WHERE id=%s"
                        valores = (novo_tipo.get(), novo_qtd.get(), novas_observacoes_texto,
                                   dados_alimento[0])
                        cursor.execute(consulta, valores)
                        conexao.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro de Edição", f"Erro ao editar dados: {e}")

            self.preencher_grade()
            janela_edicao.destroy()

        # Botão para aplicar a edição
        tk.Button(janela_edicao, text="Aplicar Edição", command=aplicar_edicao).grid(row=4, column=0, columnspan=2)

    def visualizar_detalhes(self):
        item_selecionado = self.grade.selection()

        if not item_selecionado:
            messagebox.showwarning("Visualizar Detalhes", "Selecione um alimento para visualizar detalhes.",
                                   parent=self.janela)
            return

        dados_alimento = self.grade.item(item_selecionado)['values']

        janela_detalhes = tk.Toplevel(self.janela)
        janela_detalhes.title("Detalhes do Alimento")
        janela_detalhes.resizable(False, False)

        # Exibir detalhes do alimento
        tk.Label(janela_detalhes, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(janela_detalhes, text=dados_alimento[1]).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_detalhes, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(janela_detalhes, text=dados_alimento[2]).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_detalhes, text="Observações:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(janela_detalhes, text=dados_alimento[3]).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(janela_detalhes, text="Ativo:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ativo = "Sim" if dados_alimento[4] == "Ativo" else "Não"
        tk.Label(janela_detalhes, text=ativo).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botão para fechar a janela de detalhes
        tk.Button(janela_detalhes, text="Fechar", command=janela_detalhes.destroy).grid(row=4, column=0, columnspan=2)

class TelaEntrega:
    HOST = "localhost"
    USUARIO = "nil"
    SENHA = "1234"
    BANCO_DE_DADOS = "db1"

    def __init__(self, janela):
        self.janela = janela
        self.conexao = None
        self.janela.title("Entrega de Cestas Básicas e Doações")

        colunas = ("N°", "NOME", "TELEFONE", "ENDEREÇO", "OBSERVAÇÕES")
        self.grade = ttk.Treeview(self.janela, columns=colunas, show="headings", height=15)

        for coluna in colunas:
            self.grade.heading(coluna, text=coluna)
            self.grade.column(coluna, anchor="center")

        self.barra_rolagem_vertical = Scrollbar(self.janela, orient="vertical", command=self.grade.yview)
        self.barra_rolagem_vertical.pack(side="right", fill="y")
        self.grade.configure(yscrollcommand=self.barra_rolagem_vertical.set)

        self.grade.pack(padx=10, pady=10)

        self.adicionar_componentes()
        self.preencher_grade()
        self.atualizar_quantidade_familias()

        self.lista_alimentos = None
        self.alimentos_por_familia = {}

    def adicionar_componentes(self):
        fonte_negrito = font.Font(family="Arial", size=16, weight="bold")
        rotulo_entrega = tk.Label(self.janela, text="ENTREGA DE CESTAS BÁSICAS", font=fonte_negrito)
        rotulo_entrega.pack(side="top", pady=10)

        botao_atualizar = tk.Button(self.janela, text="Atualizar Lista",
                                    command=lambda: [self.preencher_grade(), self.atualizar_quantidade_familias()])
        botao_atualizar.pack(side="left", padx=10, pady=5)

        botao_registrar = tk.Button(self.janela, text="Registrar Entrega", command=self.registrar_entrega)
        botao_registrar.pack(side="left", padx=10, pady=5)

        botao_relatorio = tk.Button(self.janela, text="Relatório",
                                    command=lambda: self.exibir_relatorio(self.obter_familia_selecionada()))
        botao_relatorio.pack(side="left", padx=10, pady=5)

        botao_localizar = tk.Button(self.janela, text="Localizar Família", command=self.localizar_registro)
        botao_localizar.pack(side="left", padx=10, pady=5)

    def obter_familia_selecionada(self):
        item_selecionado = self.grade.selection()
        if item_selecionado:
            return self.grade.item(item_selecionado)['values'][0]
        else:
            return None

    def escolher_alimentos(self):
        janela_escolha = JanelaEscolha(self, self.janela)
        # Centralizar a sub-janela em relação à janela principal
        janela_escolha.geometry("+%d+%d" % (self.janela.winfo_rootx() + 50, self.janela.winfo_rooty() + 50))
        janela_escolha.grab_set()
        janela_escolha.wait_window()

    def adicionar_alimento_lista(self , alimento_id , alimento_nome , quantidade , observacoes , data_entrega ,
                                 familia):
        if familia in self.alimentos_por_familia:
            # Adicionar o novo alimento à lista existente
            self.alimentos_por_familia[familia].append(
                (alimento_id , alimento_nome , quantidade , observacoes , data_entrega))
        else:
            # Limpar a lista de alimentos da nova família antes de adicionar o novo alimento
            self.alimentos_por_familia[familia] = []
            # Adicionar o novo alimento à lista
            self.alimentos_por_familia[familia].append(
                (alimento_id , alimento_nome , quantidade , observacoes , data_entrega))

        # Verifica se a referência ao Treeview está definida
        if self.lista_alimentos:
            self.lista_alimentos.delete(*self.lista_alimentos.get_children())
            for alimento in self.alimentos_por_familia.get(familia , []):
                self.lista_alimentos.insert("" , "end" , values=alimento)

    def obter_dados(self):
        try:
            conexao = mysql.connector.connect(
                host=self.HOST,
                user=self.USUARIO,
                password=self.SENHA,
                database=self.BANCO_DE_DADOS
            )
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM familias")
                dados = cursor.fetchall()
            return dados
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")
            return []

    def preencher_grade(self):
        dados = self.obter_dados()

        for row in self.grade.get_children():
            self.grade.delete(row)

        for linha in dados:
            self.grade.insert("", "end", values=linha)

    def exibir_relatorio(self , familia_id_selecionada=None):
        # Verifica se uma família foi selecionada
        if familia_id_selecionada is None:
            messagebox.showerror("Erro" , "Por favor, selecione uma família antes de visualizar o relatório.", parent=self.janela)
            return

        janela_relatorio = tk.Toplevel(self.janela)
        janela_relatorio.title("Relatório de Alimentos Entregues")

        # Centralizar a sub-janela em relação à janela principal
        janela_relatorio.geometry("+%d+%d" % (self.janela.winfo_rootx() + 50 , self.janela.winfo_rooty() + 50))

        tk.Label(janela_relatorio , text="Histórico de Alimentos Entregues por Data" ,
                 font=("Arial" , 12 , "bold")).pack(
            pady=10)

        # Widgets para selecionar o intervalo de datas
        frame_filtro = tk.Frame(janela_relatorio)
        frame_filtro.pack(pady=10)

        tk.Label(frame_filtro , text="De:").grid(row=0 , column=0 , padx=5)
        data_inicio_calendario = DateEntry(frame_filtro)
        data_inicio_calendario.grid(row=0 , column=1 , padx=5)

        tk.Label(frame_filtro , text="Até:").grid(row=0 , column=2 , padx=5)
        data_fim_calendario = DateEntry(frame_filtro)
        data_fim_calendario.grid(row=0 , column=3 , padx=5)

        def filtrar_relatorio():
            data_inicio = data_inicio_calendario.get_date()
            data_fim = data_fim_calendario.get_date()
            if data_inicio > data_fim:
                messagebox.showerror("Erro" , "A data de início deve ser anterior à data de término.")
                return
            else:
                treeview.delete(*treeview.get_children())
                # Obtendo dados filtrados do banco de dados
                try:
                    conexao = mysql.connector.connect(
                        host=self.HOST ,
                        user=self.USUARIO ,
                        password=self.SENHA ,
                        database=self.BANCO_DE_DADOS
                    )
                    with conexao.cursor() as cursor:
                        cursor.execute(
                            "SELECT data_entrega, tipo, qtd_entregue, observacoes FROM movimentacao INNER JOIN alimentos ON movimentacao.id_alimento = alimentos.id WHERE id_familia = %s AND data_entrega BETWEEN %s AND %s",
                            (familia_id_selecionada , data_inicio , data_fim))
                        dados = cursor.fetchall()
                        for row in dados:
                            data_entrega = row[0].strftime("%d/%m/%Y")  # Formatando a data
                            alimento = row[1]
                            quantidade = row[2]
                            observacoes = row[3]
                            treeview.insert("" , "end" , values=(data_entrega , alimento , quantidade , observacoes))
                except mysql.connector.Error as e:
                    messagebox.showerror("Erro de Conexão" , f"Erro: {e}")

        tk.Button(frame_filtro , text="Filtrar" , command=filtrar_relatorio).grid(row=0 , column=4 , padx=5)

        # Criando Treeview para exibir o relatório
        treeview = ttk.Treeview(janela_relatorio , columns=("Data", "Alimento", "Quantidade", "Observações"),
                                show="headings")
        treeview.heading("Data" , text="Data")
        treeview.heading("Alimento" , text="Alimento")
        treeview.heading("Quantidade" , text="Quantidade")
        treeview.heading("Observações" , text="Observações")

        # Barra de rolagem vertical ao treeview
        scrollbar = Scrollbar(janela_relatorio , orient="vertical" , command=treeview.yview)
        scrollbar.pack(side="right" , fill="y")
        treeview.configure(yscrollcommand=scrollbar.set)

        treeview.pack(padx=10 , pady=10 , fill="both" , expand=True)

        if familia_id_selecionada is not None:
            filtrar_relatorio()


    def obter_input_usuario(self, titulo, mensagem):
        return simpledialog.askstring(titulo, mensagem)

    def localizar_registro(self):
        criterio_busca = self.obter_input_usuario("Localizar Registro", "Digite o critério de busca:")

        # Verifica se o critério de busca é None (ou seja, se o usuário fechou a caixa de diálogo sem digitar nada)
        if criterio_busca is None:
            return

        dados = self.obter_dados()

        # Limpar a grade existente
        for row in self.grade.get_children():
            self.grade.delete(row)

        # Preencher a grade com os dados que atendem ao critério de busca
        for linha in dados:
            if criterio_busca.lower() in str(linha).lower():
                self.grade.insert("", "end", values=linha)

    def atualizar_quantidade_familias(self):
        pass

    def selecionar_familia(self, event):
        item_selecionado = self.grade.selection()
        if item_selecionado:
            familia_id_selecionada = self.grade.item(item_selecionado)['values'][0]
            self.exibir_relatorio(familia_id_selecionada)

    def registrar_entrega(self):
        item_selecionado = self.grade.selection()
        if not item_selecionado:
            messagebox.showerror("Erro" , "Por favor, selecione uma família antes de registrar a entrega.", parent=self.janela)
            return

        janela_registro = tk.Toplevel(self.janela)
        janela_registro.title("Registrar Entrega")

        # Centralizar a sub-janela em relação à janela principal
        janela_registro.geometry("+%d+%d" % (self.janela.winfo_rootx() + 50 , self.janela.winfo_rooty() + 50))

        item_selecionado = self.grade.selection()
        if item_selecionado:
            familia_id_selecionada = self.grade.item(item_selecionado)['values'][0]
            familia_selecionada = self.grade.item(item_selecionado)['values'][1]

            tk.Label(janela_registro , text="ID da Família:").grid(row=0 , column=0 , padx=5 , pady=5)
            id_familia_entry = tk.Entry(janela_registro)
            id_familia_entry.insert(0 , familia_id_selecionada)
            id_familia_entry.configure(state='readonly')
            id_familia_entry.grid(row=0 , column=1 , padx=5 , pady=5)

            tk.Label(janela_registro , text="Nome da Família:").grid(row=1 , column=0 , padx=5 , pady=5)
            nome_familia_entry = tk.Entry(janela_registro)
            nome_familia_entry.insert(0 , familia_selecionada)
            nome_familia_entry.configure(state='readonly')
            nome_familia_entry.grid(row=1 , column=1 , padx=5 , pady=5)

            tk.Label(janela_registro , text="Data da Entrega:").grid(row=2 , column=0 , padx=5 , pady=5)
            data_entrega_calendario = DateEntry(janela_registro)
            data_entrega_calendario.grid(row=2 , column=1 , padx=5 , pady=5)

            lista_alimentos = ttk.Treeview(janela_registro , columns=(
                "ID" , "Alimento" , "Quantidade" , "Observações" , "Data de Entrega") , show="headings")
            self.lista_alimentos = lista_alimentos
            lista_alimentos.heading("ID" , text="ID")
            lista_alimentos.heading("Alimento" , text="Alimento")
            lista_alimentos.heading("Quantidade" , text="Quantidade")
            lista_alimentos.heading("Observações" , text="Observações")
            lista_alimentos.heading("Data de Entrega" , text="Data de Entrega")

            # Barra de rolagem vertical ao Treeview
            scrollbar_alimentos = Scrollbar(janela_registro , orient="vertical" , command=lista_alimentos.yview)
            scrollbar_alimentos.grid(row=5 , column=2 ,
                                     sticky="ns")  # Usando grid para posicionar a barra de rolagem vertical

            lista_alimentos.configure(yscrollcommand=scrollbar_alimentos.set)

            lista_alimentos.configure(yscrollcommand=scrollbar_alimentos.set)

            lista_alimentos.grid(row=5 , column=0 , columnspan=2 , padx=5 , pady=5 , sticky="nsew")

            # Exibir lista de alimentos vazia inicialmente
            self.lista_alimentos.delete(*self.lista_alimentos.get_children())

            def excluir_alimento():
                item_selecionado = self.lista_alimentos.focus()
                if item_selecionado:
                    alimento_selecionado = self.lista_alimentos.item(item_selecionado)["values"]
                    familia_selecionada = self.grade.item(self.grade.selection())['values'][1]
                    if familia_selecionada in self.alimentos_por_familia:
                        idx = next((i for i , x in enumerate(self.alimentos_por_familia[familia_selecionada]) if
                                    x[:2] == alimento_selecionado[:2]) , None)
                        if idx is not None:
                            self.alimentos_por_familia[familia_selecionada].pop(idx)
                    self.lista_alimentos.delete(item_selecionado)

            def concluir_registro():
                item_selecionado = self.grade.selection()
                if item_selecionado:
                    data_entrega = data_entrega_calendario.get()
                    try:
                        conexao = mysql.connector.connect(
                            host=self.HOST ,
                            user=self.USUARIO ,
                            password=self.SENHA ,
                            database=self.BANCO_DE_DADOS
                        )
                        with conexao.cursor() as cursor:
                            for familia , alimentos in self.alimentos_por_familia.items():
                                for alimento in alimentos:
                                    id_alimento , nome_alimento , qtd_entregue , observacoes , data_entrega_alimento = alimento
                                    # Converter a string para objeto datetime
                                    data_entrega_alimento_formatada = datetime.strptime(data_entrega_alimento ,
                                                                                        '%d/%m/%Y').strftime('%Y-%m-%d')

                                    cursor.execute(
                                        "INSERT INTO movimentacao (id_familia, id_alimento, data_entrega, qtd_entregue) VALUES (%s, %s, %s, %s)" ,
                                        (familia_id_selecionada , id_alimento , data_entrega_alimento_formatada ,
                                         qtd_entregue)
                                    )

                                    cursor.execute(
                                        "UPDATE alimentos SET qtd = qtd - %s WHERE id = %s" ,
                                        (qtd_entregue , id_alimento)
                                    )
                        conexao.commit()

                        janela_registro.destroy()  # Destruir a janela de registro
                        exibir_mensagem_sucesso()  # Exibir a mensagem de sucesso após a destruição da janela

                        self.preencher_grade()

                        # Limpar a lista de alimentos após concluir o registro
                        self.alimentos_por_familia.clear()
                        self.lista_alimentos = None

                    except mysql.connector.Error as e:
                        messagebox.showerror("Erro" , f"Erro ao salvar no banco de dados: {e}")

            def exibir_mensagem_sucesso():
                messagebox.showinfo("Sucesso" , "Registro concluído com sucesso.", parent=self.janela)
                self.preencher_grade()



            tk.Button(janela_registro , text="Concluir Registro" , command=concluir_registro).grid(row=6 , column=0 ,
                                                                                                   padx=5 , pady=5 ,
                                                                                                   sticky="w")
            tk.Button(janela_registro , text="Excluir Alimento da Lista" , command=excluir_alimento).grid(row=6 ,
                                                                                                          column=1 ,
                                                                                                          padx=5 ,
                                                                                                          pady=5 ,
                                                                                                          sticky="w")
            tk.Button(janela_registro , text="Escolher Alimento" , command=self.escolher_alimentos).grid(row=4 ,
                                                                                                         column=0 ,
                                                                                                         columnspan=2 ,
                                                                                                         padx=5 ,
                                                                                                         pady=5)


class JanelaEscolha(tk.Toplevel):
    def __init__(self, tela_entrega, master=None, familia=None):
        super().__init__(master)
        self.title("Escolher Alimentos")
        self.tela_entrega = tela_entrega
        self.familia = familia
        self.alimentos = self.obter_alimentos()

        # Geometria da sub-janela
        self.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))

        # Cria o frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Adiciona o Treeview ao frame principal
        self.alimentos_treeview = ttk.Treeview(main_frame)
        self.alimentos_treeview["columns"] = ("ID", "Nome", "Quantidade Disponível", "Observações")
        self.alimentos_treeview.heading("#0", text="", anchor="center")
        self.alimentos_treeview.column("#0", width=0)
        self.alimentos_treeview.heading("ID", text="ID", anchor="center")
        self.alimentos_treeview.heading("Nome", text="Nome", anchor="center")
        self.alimentos_treeview.heading("Quantidade Disponível", text="Quantidade Disponível", anchor="center")
        self.alimentos_treeview.heading("Observações", text="Observações", anchor="center")

        for alimento in self.alimentos:
            self.alimentos_treeview.insert("", "end", values=alimento)

        # Barra de rolagem vertical ao Treeview
        scrollbar = Scrollbar(main_frame, orient="vertical", command=self.alimentos_treeview.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.alimentos_treeview.configure(yscrollcommand=scrollbar.set)

        # Empacotar o Treeview no frame principal
        self.alimentos_treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar redimensionamento das colunas e linhas do Treeview
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Adicionar campo de entrada para quantidade
        tk.Label(self , text="Quantidade:").pack()
        self.quantidade_entry = tk.Entry(self)
        self.quantidade_entry.pack()

        # Cria o widget DateEntry e armazena sua referência
        tk.Label(self, text="Data da Entrega:").pack()
        self.calendario = DateEntry(self)
        self.calendario.pack(padx=10, pady=10)

        tk.Button(self, text="Selecionar", command=self.selecionar_alimento).pack(pady=10)



    def obter_familia_selecionada(self):
        item_selecionado = self.grade.selection()
        if item_selecionado:
            return self.grade.item(item_selecionado)['values'][0]
        else:
            return None

    def selecionar_alimento(self):
        item_selecionado = self.alimentos_treeview.focus()
        if item_selecionado:
            alimento_selecionado = self.alimentos_treeview.item(item_selecionado)["values"]
            quantidade = self.quantidade_entry.get()
            observacoes = alimento_selecionado[3]

            try:
                quantidade = int(quantidade)
                if quantidade < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Digite uma quantidade válida (número inteiro).",parent=self)
                return

            # Obtendo a data selecionada do DateEntry
            data_entrega = self.calendario.get()
            self.tela_entrega.adicionar_alimento_lista(alimento_selecionado[0], alimento_selecionado[1], quantidade,
                                                       observacoes, data_entrega, self.familia)
            self.destroy()

    @staticmethod
    def obter_alimentos():
        try:
            conexao = mysql.connector.connect(
                host=TelaEntrega.HOST,
                user=TelaEntrega.USUARIO,
                password=TelaEntrega.SENHA,
                database=TelaEntrega.BANCO_DE_DADOS
            )
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM alimentos WHERE ativo = 1")
                dados = cursor.fetchall()
            return dados
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")
            return []


if __name__ == "__main__":
    janela = tk.Tk()
    janela.resizable(False, False)
    app = SistemaDeGerenciamento(janela)
    janela.geometry("1050x450")
    janela.mainloop()



