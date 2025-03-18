import requests
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QPushButton, QVBoxLayout, QWidget


def baixar_arquivo(codigo, data, save_path):
    url = f"https://www.vsbtrans.com.br/getFiles.php?codigo={codigo}&data={data}"
    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.vsbtrans.com.br/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            json_response = response.json()
            zip_url = json_response.get("zipUrl")
            if zip_url:
                download_url = f"https://www.vsbtrans.com.br{zip_url.replace('\/', '/')}"
                download_zip(download_url, codigo, data, save_path)
            else:
                print(f"Erro: 'zipUrl' não encontrado no JSON para o código {codigo}.")
        except ValueError:
            print(f"Falha ao interpretar JSON para o código {codigo}. Conteúdo da resposta: {response.content[:200]}")
    else:
        print(f"Erro ao acessar o arquivo para o código {codigo}. Status code: {response.status_code}")


def download_zip(download_url, codigo, data, save_path):
    response = requests.get(download_url)

    if response.status_code == 200 and response.headers.get('Content-Type') == 'application/zip':
        filename = f"{data}_{codigo}_faturas.zip"
        file_path = os.path.join(save_path, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo baixado com sucesso: {file_path}")
    else:
        print(f"Falha ao baixar o arquivo ZIP para o código {codigo}. Status code: {response.status_code}")


def rio_energy(save_path):
    empresa = "Rio Energy"
    pasta_empresa = os.path.join(save_path, empresa)
    os.makedirs(pasta_empresa, exist_ok=True)
    
    codigos_rio = [
        "4313", "4314", "3430", "3431", "3432", "4415", "4315", "4316", "3502",
        "3497", "3503", "3530", "3498", "3531", "3532", "3537", "3538", "3947",
        "3948", "3969", "3970", "3976", "3972"
    ]
    for codigo in codigos_rio:
        baixar_arquivo(codigo, "2024.10", pasta_empresa)


def america(save_path):
    empresa = "America"
    pasta_empresa = os.path.join(save_path, empresa)
    os.makedirs(pasta_empresa, exist_ok=True)
    
    codigos_america = ["8011", "3740", "3741", "3750", "3859", "3860", "3861", "3862", "3863", "3864"]
    for codigo in codigos_america:
        baixar_arquivo(codigo, "2024.10", pasta_empresa)


def diamante_energia(save_path):
    empresa = "Diamante Energia"
    pasta_empresa = os.path.join(save_path, empresa)
    os.makedirs(pasta_empresa, exist_ok=True)
    
    codigo_diamante = "3748"
    baixar_arquivo(codigo_diamante, "2024.10", pasta_empresa)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Campo para digitar ou selecionar o diretório
        self.save_path_input = QLineEdit(self)
        self.save_path_input.setPlaceholderText("Digite ou selecione o local para salvar os arquivos")
        layout.addWidget(self.save_path_input)

        # Botão para localizar diretório
        self.browse_button = QPushButton("Localizar Diretório", self)
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        # Botão para Rio Energy
        self.button_rio = QPushButton("Rio Energy", self)
        self.button_rio.clicked.connect(self.run_rio_energy)
        layout.addWidget(self.button_rio)

        # Botão para America
        self.button_america = QPushButton("America", self)
        self.button_america.clicked.connect(self.run_america)
        layout.addWidget(self.button_america)

        # Botão para Diamante Energia
        self.button_diamante = QPushButton("Diamante Energia", self)
        self.button_diamante.clicked.connect(self.run_diamante_energia)
        layout.addWidget(self.button_diamante)

        # Configuração da janela principal
        self.setLayout(layout)
        self.setWindowTitle("Automatização de Empresas")
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a pasta")
        if folder:
            self.save_path_input.setText(folder)

    def run_rio_energy(self):
        save_path = self.save_path_input.text()
        if save_path:
            rio_energy(save_path)
        else:
            print("Por favor, selecione um diretório para salvar os arquivos.")

    def run_america(self):
        save_path = self.save_path_input.text()
        if save_path:
            america(save_path)
        else:
            print("Por favor, selecione um diretório para salvar os arquivos.")

    def run_diamante_energia(self):
        save_path = self.save_path_input.text()
        if save_path:
            diamante_energia(save_path)
        else:
            print("Por favor, selecione um diretório para salvar os arquivos.")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyApp()
    app.exec_()
