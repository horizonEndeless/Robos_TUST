import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import os
import json
import io
import zipfile
import threading
import base64
from datetime import datetime

class TustImportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Importador TUST")
        self.root.geometry("700x500")
        
        # URL da API do TUST
        self.api_base_url = "https://api-tust.pollvo.com"
        self.import_endpoint = "/api/processoimportacaoexecucao"
        
        # Credenciais
        self.username = ""
        self.password = ""
        
        # Criar interface
        self.create_widgets()
        
        # Status da importação
        self.importing = False
    
    def create_widgets(self):
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Importador de Arquivos TUST", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Descrição
        desc_label = ttk.Label(main_frame, text="Selecione arquivos ZIP ou documentos individuais para importação no sistema TUST", 
                              wraplength=600)
        desc_label.pack(pady=5)
        
        # Frame para autenticação
        auth_frame = ttk.LabelFrame(main_frame, text="Credenciais", padding=10)
        auth_frame.pack(fill=tk.X, pady=10)
        
        # Campos de autenticação
        auth_grid = ttk.Frame(auth_frame)
        auth_grid.pack(fill=tk.X)
        
        ttk.Label(auth_grid, text="Usuário:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(auth_grid, textvariable=self.username_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(auth_grid, text="Senha:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(auth_grid, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Frame para seleção de arquivos
        files_frame = ttk.LabelFrame(main_frame, text="Arquivos para Importação", padding=10)
        files_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botões para selecionar arquivos
        btn_frame = ttk.Frame(files_frame)
        btn_frame.pack(pady=10)
        
        zip_btn = ttk.Button(btn_frame, text="Selecionar ZIP", command=self.select_zip)
        zip_btn.grid(row=0, column=0, padx=10)
        
        file_btn = ttk.Button(btn_frame, text="Selecionar Arquivos", command=self.select_files)
        file_btn.grid(row=0, column=1, padx=10)
        
        # Lista de arquivos selecionados
        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(list_frame)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botão de importação
        import_btn = ttk.Button(main_frame, text="Importar para TUST", command=self.start_import)
        import_btn.pack(pady=10)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill=tk.X, pady=5)
        
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para importação")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Armazenar arquivos selecionados
        self.selected_files = []
    
    def select_zip(self):
        zip_file = filedialog.askopenfilename(
            title="Selecione o arquivo ZIP",
            filetypes=[("Arquivos ZIP", "*.zip")]
        )
        
        if zip_file:
            self.selected_files = [zip_file]
            self.update_file_list()
            self.status_var.set(f"Arquivo ZIP selecionado: {os.path.basename(zip_file)}")
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Selecione os arquivos",
            filetypes=[("Todos os arquivos", "*.*"), ("Arquivos XML", "*.xml"), ("Arquivos PDF", "*.pdf")]
        )
        
        if files:
            self.selected_files = list(files)
            self.update_file_list()
            self.status_var.set(f"{len(files)} arquivos selecionados")
    
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def start_import(self):
        if self.importing:
            messagebox.showwarning("Aviso", "Importação já em andamento")
            return
            
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado para importação")
            return
        
        # Obter credenciais
        self.username = self.username_var.get()
        self.password = self.password_var.get()
        
        if not self.username or not self.password:
            messagebox.showwarning("Aviso", "Por favor, informe usuário e senha")
            return
        
        # Iniciar importação em uma thread separada para não bloquear a interface
        import_thread = threading.Thread(target=self.import_files)
        import_thread.daemon = True
        import_thread.start()
    
    def import_files(self):
        self.importing = True
        self.progress_var.set(0)
        self.status_var.set("Preparando arquivos para importação...")
        
        try:
            # Se for um único arquivo ZIP, enviamos diretamente
            if len(self.selected_files) == 1 and self.selected_files[0].lower().endswith('.zip'):
                with open(self.selected_files[0], 'rb') as f:
                    zip_data = f.read()
                    self.progress_var.set(30)
                    self.send_to_tust(zip_data, os.path.basename(self.selected_files[0]))
            else:
                # Se forem múltiplos arquivos, criamos um ZIP em memória
                self.status_var.set("Compactando arquivos...")
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for i, file_path in enumerate(self.selected_files):
                        zip_file.write(file_path, os.path.basename(file_path))
                        # Atualizar progresso
                        progress = (i + 1) / len(self.selected_files) * 30
                        self.progress_var.set(progress)
                
                zip_buffer.seek(0)
                self.send_to_tust(zip_buffer.read(), f"importacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao importar arquivos: {str(e)}"))
            self.status_var.set("Erro na importação")
            self.importing = False
    
    def send_to_tust(self, zip_data, filename):
        self.status_var.set("Enviando para o TUST...")
        self.progress_var.set(50)
        
        try:
            # Tentar diferentes abordagens para a API
            # 1. Tentar enviar diretamente com autenticação básica
            url = f"{self.api_base_url}{self.import_endpoint}"
            
            # Criar o objeto de processo de importação
            processo_importacao = {
                "Identificador": 0,
                "IdentificadorProcessoImportacao": 1,  # ID do processo de importação manual
                "Parametros": [
                    {
                        "Identificador": 0,
                        "IdentificadorProcessoImportacaoExecucao": 0,
                        "Nome": "ARQUIVO",
                        "Valor": "ARQUIVO",
                        "Tipo": "file"
                    }
                ]
            }
            
            # Preparar autenticação básica
            auth = (self.username, self.password)
            
            # Preparar o multipart/form-data
            files = {
                'json': ('json', json.dumps(processo_importacao), 'application/json'),
                'ARQUIVO': (filename, zip_data, 'application/zip')
            }
            
            # Enviar a requisição com autenticação básica
            self.progress_var.set(70)
            response = requests.post(url, files=files, auth=auth)
            
            # Verificar resposta
            self.progress_var.set(90)
            
            # Mostrar detalhes da resposta para debug
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code in [200, 201]:
                try:
                    result = response.json()
                    if not result.get("IsErro", True):
                        self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Arquivos importados com sucesso!"))
                        self.status_var.set("Importação concluída com sucesso")
                    else:
                        error_msg = result.get("Mensagem", "Erro desconhecido na importação")
                        self.root.after(0, lambda: messagebox.showwarning("Aviso", f"Erro na importação: {error_msg}"))
                        self.status_var.set("Importação com erros")
                except:
                    # Se não for JSON, pode ser uma resposta de sucesso simples
                    self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Arquivos enviados com sucesso!"))
                    self.status_var.set("Importação concluída")
            else:
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na comunicação com o servidor: {response.status_code}"))
                self.status_var.set(f"Erro na comunicação: {response.status_code}")
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao enviar arquivos: {str(e)}"))
            self.status_var.set("Erro ao enviar arquivos")
        finally:
            self.progress_var.set(100)
            self.importing = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TustImportApp(root)
    root.mainloop()