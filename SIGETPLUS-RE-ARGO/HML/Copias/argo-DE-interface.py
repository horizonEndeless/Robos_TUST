from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                           QTableWidget, QTableWidgetItem, QCheckBox,
                           QScrollArea, QMessageBox, QGroupBox, QDialog)
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

class EmailAgentDialog(QDialog):
    """Janela de diálogo para adicionar email e agentes"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Email e Agentes")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Email
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite o email de login")
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)
        
        # Tabela de agentes
        layout.addWidget(QLabel("Agentes:"))
        self.agents_table = QTableWidget()
        self.agents_table.setColumnCount(2)
        self.agents_table.setHorizontalHeaderLabels(["Código ONS", "Nome do Agente"])
        layout.addWidget(self.agents_table)
        
        # Botões para agentes
        agent_buttons = QHBoxLayout()
        add_agent_btn = QPushButton("Adicionar Agente")
        add_agent_btn.clicked.connect(self.add_agent_row)
        remove_agent_btn = QPushButton("Remover Agente")
        remove_agent_btn.clicked.connect(self.remove_agent_row)
        agent_buttons.addWidget(add_agent_btn)
        agent_buttons.addWidget(remove_agent_btn)
        layout.addLayout(agent_buttons)
        
        # Botões de confirmação
        buttons = QHBoxLayout()
        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        # Adicionar primeira linha de agente
        self.add_agent_row()

    def add_agent_row(self):
        row = self.agents_table.rowCount()
        self.agents_table.insertRow(row)
        self.agents_table.setCellWidget(row, 0, QLineEdit())
        self.agents_table.setCellWidget(row, 1, QLineEdit())

    def remove_agent_row(self):
        current_row = self.agents_table.currentRow()
        if current_row >= 0:
            self.agents_table.removeRow(current_row)

    def get_data(self):
        """Retorna os dados inseridos"""
        email = self.email_input.text()
        agentes = {}
        for row in range(self.agents_table.rowCount()):
            codigo = self.agents_table.cellWidget(row, 0).text()
            nome = self.agents_table.cellWidget(row, 1).text()
            if codigo and nome:
                agentes[codigo] = nome
        return email, agentes

class SigetPlusDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIGET+ Downloader")
        self.setGeometry(100, 100, 800, 600)
        self.email_configs = []  # Lista para armazenar configurações de email/agentes
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Botão para adicionar novo email
        add_email_btn = QPushButton("Adicionar Novo Email")
        add_email_btn.clicked.connect(self.add_email_config)
        layout.addWidget(add_email_btn)

        # Lista de configurações
        self.config_table = QTableWidget()
        self.config_table.setColumnCount(3)
        self.config_table.setHorizontalHeaderLabels(["Email", "Agentes", "Ações"])
        layout.addWidget(self.config_table)

        # Seção de transmissoras
        self.setup_transmissoras_section(layout)

        # Botão de download
        download_btn = QPushButton("Iniciar Download")
        download_btn.clicked.connect(self.start_download)
        layout.addWidget(download_btn)

    def add_email_config(self):
        """Abre diálogo para adicionar novo email e agentes"""
        dialog = EmailAgentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            email, agentes = dialog.get_data()
            if email and agentes:
                self.email_configs.append({'email': email, 'agentes': agentes})
                self.update_config_table()

    def update_config_table(self):
        """Atualiza a tabela de configurações"""
        self.config_table.setRowCount(len(self.email_configs))
        for row, config in enumerate(self.email_configs):
            self.config_table.setItem(row, 0, QTableWidgetItem(config['email']))
            self.config_table.setItem(row, 1, QTableWidgetItem(str(len(config['agentes'])) + " agentes"))
            
            # Botão de ações
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            
            edit_btn = QPushButton("Editar")
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_config(r))
            remove_btn = QPushButton("Remover")
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_config(r))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(remove_btn)
            self.config_table.setCellWidget(row, 2, actions_widget)

    def edit_config(self, row):
        """Edita uma configuração existente"""
        config = self.email_configs[row]
        dialog = EmailAgentDialog(self)
        dialog.email_input.setText(config['email'])
        
        # Preencher agentes existentes
        for codigo, nome in config['agentes'].items():
            dialog.add_agent_row()
            last_row = dialog.agents_table.rowCount() - 1
            dialog.agents_table.cellWidget(last_row, 0).setText(codigo)
            dialog.agents_table.cellWidget(last_row, 1).setText(nome)
        
        if dialog.exec_() == QDialog.Accepted:
            email, agentes = dialog.get_data()
            if email and agentes:
                self.email_configs[row] = {'email': email, 'agentes': agentes}
                self.update_config_table()

    def remove_config(self, row):
        """Remove uma configuração"""
        self.email_configs.pop(row)
        self.update_config_table()

    def start_download(self):
        """Inicia o download para todos os emails e seus agentes"""
        all_downloads = []
        
        # Percorrer todas as seções de email
        for i in range(self.email_sections_layout.count()):
            section = self.email_sections_layout.itemAt(i).widget()
            if not isinstance(section, QGroupBox):
                continue
                
            # Obter email
            email_input = section.findChild(QLineEdit)
            email = email_input.text()
            
            # Obter agentes desta seção
            agents_table = section.findChild(QTableWidget)
            agentes = {}
            for row in range(agents_table.rowCount()):
                codigo = agents_table.cellWidget(row, 0).text()
                nome = agents_table.cellWidget(row, 1).text()
                if codigo and nome:
                    agentes[codigo] = nome
            
            # Coletar transmissoras selecionadas
            transmissoras_selecionadas = []
            for row in range(self.transmissoras_table.rowCount()):
                checkbox_widget = self.transmissoras_table.cellWidget(row, 0)
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox.isChecked():
                    codigo = self.transmissoras_table.item(row, 1).text()
                    nome = self.transmissoras_table.item(row, 2).text()
                    transmissoras_selecionadas.append((codigo, nome))
            
            if email and agentes:
                all_downloads.append({
                    'email': email,
                    'agentes': agentes,
                    'transmissoras': transmissoras_selecionadas
                })
        
        # Iniciar downloads
        for download in all_downloads:
            print(f"Iniciando download para:")
            print(f"Email: {download['email']}")
            print(f"Agentes: {download['agentes']}")
            print(f"Transmissoras selecionadas: {download['transmissoras']}")
            # Aqui você chamaria sua função original de download
            login_and_download(download['email'], download['agentes'])

    def setup_transmissoras_section(self, layout):
        """Configura a seção de transmissoras"""
        transmissoras_group = QWidget()
        transmissoras_layout = QVBoxLayout(transmissoras_group)
        
        # Botão de buscar transmissoras
        fetch_layout = QHBoxLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite o email de login")
        fetch_btn = QPushButton("Buscar Transmissoras")
        fetch_btn.clicked.connect(self.fetch_transmissoras)
        fetch_layout.addWidget(self.email_input)
        fetch_layout.addWidget(fetch_btn)
        transmissoras_layout.addLayout(fetch_layout)
        
        # Campo de busca
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar Transmissora:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite para filtrar transmissoras")
        self.search_input.textChanged.connect(self.filter_transmissoras)
        search_layout.addWidget(self.search_input)
        transmissoras_layout.addLayout(search_layout)
        
        # Checkbox para selecionar todas
        self.select_all_check = QCheckBox("Selecionar Todas as Transmissoras")
        self.select_all_check.stateChanged.connect(self.toggle_all_transmissoras)
        transmissoras_layout.addWidget(self.select_all_check)
        
        # Tabela de transmissoras
        self.transmissoras_table = QTableWidget()
        self.transmissoras_table.setColumnCount(3)
        self.transmissoras_table.setHorizontalHeaderLabels(["Selecionar", "Código ONS", "Nome da Transmissora"])
        self.transmissoras_table.horizontalHeader().setStretchLastSection(True)
        transmissoras_layout.addWidget(self.transmissoras_table)
        
        layout.addWidget(transmissoras_group)

    def filter_transmissoras(self):
        """Filtra as transmissoras com base no texto de busca"""
        search_text = self.search_input.text().lower()
        for row in range(self.transmissoras_table.rowCount()):
            nome = self.transmissoras_table.item(row, 2)
            if nome:  # Verifica se o item existe
                nome_text = nome.text().lower()
                self.transmissoras_table.setRowHidden(row, search_text not in nome_text)

    def toggle_all_transmissoras(self, state):
        """Seleciona ou desmarca todas as transmissoras"""
        for row in range(self.transmissoras_table.rowCount()):
            checkbox_widget = self.transmissoras_table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(state == Qt.Checked)

    def add_agent_row(self, agents_table):
        """Adiciona uma nova linha na tabela de agentes"""
        row_position = agents_table.rowCount()
        agents_table.insertRow(row_position)
        
        # Adicionar campos de entrada para código e nome
        codigo_input = QLineEdit()
        nome_input = QLineEdit()
        
        agents_table.setCellWidget(row_position, 0, codigo_input)
        agents_table.setCellWidget(row_position, 1, nome_input)

    def add_transmissora_row(self, codigo, nome):
        """Adiciona uma nova linha na tabela de transmissoras"""
        row_position = self.transmissoras_table.rowCount()
        self.transmissoras_table.insertRow(row_position)
        
        # Adicionar checkbox
        checkbox = QCheckBox()
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        
        self.transmissoras_table.setCellWidget(row_position, 0, checkbox_widget)
        self.transmissoras_table.setItem(row_position, 1, QTableWidgetItem(str(codigo)))
        self.transmissoras_table.setItem(row_position, 2, QTableWidgetItem(str(nome)))

    def fetch_transmissoras(self):
        """Busca as transmissoras disponíveis no SIGET+"""
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Erro", "Por favor, insira um email válido.")
            return
        
        try:
            # Configurar o WebDriver
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver, 20)
            
            # Login
            driver.get('https://sys.sigetplus.com.br/portal/login')
            email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
            email_field.send_keys(email)
            
            login_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div/div[2]/form/div/div/div/button')))
            login_button.click()
            
            # Limpar tabela atual
            self.transmissoras_table.setRowCount(0)
            
            # Buscar transmissoras
            page = 1
            while True:
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-striped")))
                    time.sleep(2)
                    
                    table = driver.find_element(By.CLASS_NAME, "table-striped")
                    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Pular cabeçalho
                    
                    for row in rows:
                        try:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if cells:
                                transmissora_text = cells[0].text.strip()
                                codigo_ons = transmissora_text.split('-')[0].strip()
                                nome = transmissora_text.split('-')[1].strip() if '-' in transmissora_text else transmissora_text
                                
                                if codigo_ons and nome:
                                    self.add_transmissora_row(codigo_ons, nome)
                        except Exception as e:
                            print(f"Erro ao processar linha: {str(e)}")
                    
                    # Tentar ir para próxima página
                    try:
                        next_button = driver.find_element(By.XPATH, '//a[@rel="next"]')
                        driver.execute_script("arguments[0].click();", next_button)
                        page += 1
                        time.sleep(2)
                    except NoSuchElementException:
                        break  # Não há mais páginas
                    
                except Exception as e:
                    print(f"Erro ao processar página {page}: {str(e)}")
                    break
            
            QMessageBox.information(self, "Sucesso", 
                f"Foram encontradas {self.transmissoras_table.rowCount()} transmissoras.")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar transmissoras: {str(e)}")
        finally:
            driver.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SigetPlusDownloader()
    window.show()
    sys.exit(app.exec_()) 