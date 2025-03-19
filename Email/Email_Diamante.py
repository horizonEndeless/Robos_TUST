import win32com.client
import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import json
import tkinter as tk
from tkinter import ttk, messagebox

def carregar_mapeamento_cnpj():
    # Caminho para o arquivo de mapeamento
    arquivo_mapeamento = r"C:\Users\Bruno\Desktop\Workspace\Email\mapeamento_cnpj.json"
    
    try:
        with open(arquivo_mapeamento, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo de mapeamento não encontrado em: {arquivo_mapeamento}")
        return {}
    except Exception as e:
        print(f"Erro ao ler arquivo de mapeamento: {str(e)}")
        return {}

def extrair_cnpj_do_xml(caminho_xml):
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        
        # Procurar pelo CNPJ em qualquer namespace
        for elem in root.iter():
            if 'emit' in elem.tag:
                for child in elem:
                    if 'CNPJ' in child.tag:
                        return child.text
        return None
    except Exception as e:
        print(f"Erro ao ler XML: {str(e)}")
        return None

def baixar_anexos_outlook(remetente, dias_atras):
    # Criar uma instância do Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    # Configurar a conta de email
    for account in namespace.Accounts:
        if account.SmtpAddress == "services.easytust@outlook.com":
            inbox = account.DeliveryStore.GetDefaultFolder(6)
            break
    
    # Pasta para salvar os anexos
    pasta_destino = r"C:\Users\Bruno\Downloads\TUST\EMAIL\DE"
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Carregar mapeamento de CNPJs
    mapeamento_cnpj = carregar_mapeamento_cnpj()

    # Calcular a data inicial (dias atrás a partir de hoje)
    data_atual = datetime.now()
    data_inicial = data_atual - timedelta(days=dias_atras)
    print(f"Buscando emails de {data_inicial.strftime('%d/%m/%Y')} até {data_atual.strftime('%d/%m/%Y')}")

    # Filtrar emails
    emails = inbox.Items
    emails.Sort("[ReceivedTime]", True)

    for email in emails:
        try:
            if hasattr(email, 'ReceivedTime') and hasattr(email, 'SenderEmailAddress'):
                data_email = email.ReceivedTime.date()
                
                # Verificar se o email está dentro do período e é do remetente correto
                if (email.SenderEmailAddress.lower() == remetente.lower() and 
                    data_inicial.date() <= data_email <= data_atual.date()):
                    
                    data_hora_email = email.ReceivedTime.strftime("%Y%m%d_%H%M%S")
                    assunto = email.Subject[:30]
                    assunto = "".join(c for c in assunto if c.isalnum() or c in (' ', '-', '_')).strip()
                    nome_pasta_temp = f"{data_hora_email}_{assunto}"
                    pasta_email_temp = os.path.join(pasta_destino, nome_pasta_temp)
                    
                    if not os.path.exists(pasta_email_temp):
                        os.makedirs(pasta_email_temp)
                    
                    cnpj_encontrado = None
                    
                    # Primeiro, salvar todos os anexos
                    if email.Attachments.Count > 0:
                        for anexo in email.Attachments:
                            if anexo.FileName.lower().endswith(('.pdf', '.doc', '.docx', '.xml')):
                                caminho_arquivo = os.path.join(pasta_email_temp, anexo.FileName)
                                anexo.SaveAsFile(caminho_arquivo)
                                
                                # Se for XML, tentar extrair CNPJ
                                if anexo.FileName.lower().endswith('.xml'):
                                    cnpj = extrair_cnpj_do_xml(caminho_arquivo)
                                    if cnpj and cnpj in mapeamento_cnpj:
                                        cnpj_encontrado = cnpj
                    
                    # Renomear a pasta se encontrou CNPJ mapeado
                    if cnpj_encontrado:
                        nome_pasta_final = mapeamento_cnpj[cnpj_encontrado]
                        pasta_email_final = os.path.join(pasta_destino, nome_pasta_final)
                        
                        # Se já existir pasta com esse nome, adiciona um número
                        contador = 1
                        nome_pasta_base = nome_pasta_final
                        while os.path.exists(pasta_email_final):
                            nome_pasta_final = f"{nome_pasta_base}_{contador}"
                            pasta_email_final = os.path.join(pasta_destino, nome_pasta_final)
                            contador += 1
                        
                        os.rename(pasta_email_temp, pasta_email_final)
                        print(f"Pasta renomeada para: {nome_pasta_final}")
                    else:
                        print(f"CNPJ não encontrado ou não mapeado. Mantendo nome original: {nome_pasta_temp}")
        except Exception as e:
            print(f"Erro ao processar email: {str(e)}")
            continue

class EmailProcessadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Emails")
        self.root.geometry("600x400")
        
        # Carregar remetentes salvos
        self.remetentes_salvos = self.carregar_remetentes()
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Remetentes
        ttk.Label(main_frame, text="Remetente:").grid(row=0, column=0, sticky=tk.W)
        self.remetente_var = tk.StringVar()
        self.remetente_entry = ttk.Entry(main_frame, textvariable=self.remetente_var, width=40)
        self.remetente_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Botão adicionar remetente
        ttk.Button(main_frame, text="Adicionar", command=self.adicionar_remetente).grid(row=0, column=2, padx=5)
        
        # Lista de remetentes
        ttk.Label(main_frame, text="Remetentes salvos:").grid(row=1, column=0, sticky=tk.W, pady=(10,0))
        self.lista_remetentes = tk.Listbox(main_frame, width=50, height=8, selectmode=tk.MULTIPLE)
        self.lista_remetentes.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        self.atualizar_lista_remetentes()
        
        # Frame para botões de seleção
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.grid(row=3, column=0, columnspan=3, pady=5)
        
        # Botões Selecionar Todos e Limpar Seleção
        ttk.Button(botoes_frame, text="Selecionar Todos", 
                  command=self.selecionar_todos).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="Limpar Seleção", 
                  command=self.limpar_selecao).pack(side=tk.LEFT, padx=5)
        
        # Botão remover movido para depois dos botões de seleção
        ttk.Button(main_frame, text="Remover Selecionado", 
                  command=self.remover_remetente).grid(row=4, column=0, columnspan=3, pady=5)
        
        # Dias para busca
        ttk.Label(main_frame, text="Dias para buscar:").grid(row=5, column=0, sticky=tk.W, pady=(10,0))
        self.dias_var = tk.StringVar(value="30")
        dias_entry = ttk.Entry(main_frame, textvariable=self.dias_var, width=10)
        dias_entry.grid(row=5, column=1, sticky=tk.W)
        
        # Botão processar
        ttk.Button(main_frame, text="Processar", 
                  command=self.processar_emails).grid(row=6, column=0, columnspan=3, pady=20)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=7, column=0, columnspan=3)

    def carregar_remetentes(self):
        arquivo_remetentes = r"C:\Users\Bruno\Desktop\Workspace\Email\remetentes.json"
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(arquivo_remetentes):
                # Se não existir, cria com uma lista vazia
                self.salvar_remetentes([])
                return []
            
            # Se existir, tenta ler
            with open(arquivo_remetentes, 'r') as f:
                conteudo = f.read().strip()
                # Se estiver vazio, inicializa com lista vazia
                if not conteudo:
                    self.salvar_remetentes([])
                    return []
                # Se tiver conteúdo, carrega como JSON
                return json.loads(conteudo)
                
        except json.JSONDecodeError:
            # Se o arquivo estiver corrompido, reinicia com lista vazia
            self.salvar_remetentes([])
            return []
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar remetentes: {str(e)}")
            return []

    def salvar_remetentes(self, remetentes=None):
        arquivo_remetentes = r"C:\Users\Bruno\Desktop\Workspace\Email\remetentes.json"
        try:
            lista_para_salvar = remetentes if remetentes is not None else self.remetentes_salvos
            with open(arquivo_remetentes, 'w') as f:
                json.dump(lista_para_salvar, f, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar remetentes: {str(e)}")

    def atualizar_lista_remetentes(self):
        self.lista_remetentes.delete(0, tk.END)
        for remetente in self.remetentes_salvos:
            self.lista_remetentes.insert(tk.END, remetente)

    def adicionar_remetente(self):
        novo_remetente = self.remetente_var.get().strip()
        if novo_remetente:
            if novo_remetente not in self.remetentes_salvos:
                self.remetentes_salvos.append(novo_remetente)
                self.salvar_remetentes()
                self.atualizar_lista_remetentes()
                self.remetente_var.set("")
            else:
                messagebox.showwarning("Aviso", "Este remetente já está na lista!")

    def remover_remetente(self):
        selecao = self.lista_remetentes.curselection()
        if selecao:
            # Remove os itens selecionados (do último para o primeiro para manter os índices corretos)
            for index in sorted(selecao, reverse=True):
                remetente = self.lista_remetentes.get(index)
                self.remetentes_salvos.remove(remetente)
            self.salvar_remetentes()
            self.atualizar_lista_remetentes()

    def processar_emails(self):
        try:
            dias = int(self.dias_var.get())
            remetentes_selecionados = [self.lista_remetentes.get(idx) for idx in self.lista_remetentes.curselection()]
            
            if not remetentes_selecionados:
                messagebox.showwarning("Aviso", "Selecione pelo menos um remetente!")
                return
            
            self.status_var.set(f"Processando {len(remetentes_selecionados)} remetentes...")
            self.root.update()
            
            for i, remetente in enumerate(remetentes_selecionados, 1):
                self.status_var.set(f"Processando remetente {i} de {len(remetentes_selecionados)}: {remetente}")
                self.root.update()
                baixar_anexos_outlook(remetente, dias)
            
            self.status_var.set("Processamento concluído!")
            messagebox.showinfo("Sucesso", "Processamento concluído com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido de dias!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar emails: {str(e)}")
            self.status_var.set("Erro no processamento!")

    def selecionar_todos(self):
        """Seleciona todos os itens da lista"""
        self.lista_remetentes.select_set(0, tk.END)

    def limpar_selecao(self):
        """Remove a seleção de todos os itens"""
        self.lista_remetentes.selection_clear(0, tk.END)

def main():
    root = tk.Tk()
    app = EmailProcessadorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
