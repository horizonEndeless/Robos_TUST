from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime, timedelta
import zipfile

# Lista de códigos ONS
CODIGOS_ONS = [
    "3859", "3860", "3861", "3862", "3863", "3864", 
    "3740", "3741", "3750", "8011"
    
]

def criar_pasta_ae():
    pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    pasta_ae = os.path.join(pasta_downloads, "AE")
    
    if not os.path.exists(pasta_ae):
        os.makedirs(pasta_ae)
        print("Pasta AE criada com sucesso!")
    
    return pasta_ae

def obter_mes_referencia():
    # Obtém a data atual
    data_atual = datetime.now()
    # Subtrai um mês para obter o mês de referência
    mes_referencia = data_atual - timedelta(days=30)
    return mes_referencia

def extrair_zip(pasta_ae):
    # Aguarda um pouco para garantir que o download foi concluído
    time.sleep(5)
    
    # Lista todos os arquivos na pasta
    arquivos = os.listdir(pasta_ae)
    
    # Procura por arquivos ZIP
    for arquivo in arquivos:
        if arquivo.endswith('.zip'):
            caminho_zip = os.path.join(pasta_ae, arquivo)
            try:
                # Extrai o conteúdo do ZIP
                with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                    zip_ref.extractall(pasta_ae)
                # Remove o arquivo ZIP após extrair
                os.remove(caminho_zip)
                print(f"Arquivo {arquivo} extraído com sucesso!")
            except Exception as e:
                print(f"Erro ao extrair {arquivo}: {str(e)}")

def processar_empresa(driver, codigo_ons):
    try:
        print(f"\nProcessando empresa código: {codigo_ons}")
        
        # Obtém o mês de referência
        mes_referencia = obter_mes_referencia()
        
        # Acessar o site inicial (se não for a primeira empresa)
        if driver.current_url != "https://dompedroenergia.com.br/":
            driver.get("https://dompedroenergia.com.br/")
            time.sleep(2)
        
        # Inserir o código ONS
        campo_codigo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        campo_codigo.clear()
        campo_codigo.send_keys(codigo_ons)
        
        # Clicar no botão de acesso
        botao = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                "button.inline-flex.items-center.justify-center"))
        )
        botao.click()
        
        # Aguardar a tabela carregar
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tableFaturas"))
        )
        time.sleep(2)
        
        # Encontrar todas as seções de faturas usando o seletor correto
        secoes_faturas = driver.find_elements(By.CSS_SELECTOR, "div.fatura")
        if not secoes_faturas:
            print("Nenhuma seção de fatura encontrada")
            return False
            
        # Lista para armazenar tuplas de (data, botão XML)
        faturas_info = []
        
        # Processar cada seção
        for secao in secoes_faturas:
            try:
                texto_fatura = secao.find_element(By.CSS_SELECTOR, "h3#textoFaturas").text
                data_texto = texto_fatura.split('(')[1].strip(')')
                mes, ano = data_texto.split('/')
                data_completa = f"25/{mes}/{ano}"
                data_obj = datetime.strptime(data_completa, "%d/%m/%Y")
                
                # Verifica se a fatura é do mês de referência
                if (data_obj.year == mes_referencia.year and 
                    data_obj.month == mes_referencia.month):
                    botao_xml = secao.find_element(By.CSS_SELECTOR, 
                        "button.btn-imprimir.dropbtn-imprimir.float-left.btn-download-color.linkDownloadXml")
                    faturas_info.append((data_obj, botao_xml))
                    break  # Encontrou a fatura do mês de referência
            except Exception as e:
                print(f"Erro ao processar seção: {str(e)}")
                continue
        
        if not faturas_info:
            print(f"Não foi encontrada fatura para o mês {mes_referencia.month}/{mes_referencia.year}")
            return False
        
        # Clica no botão XML da fatura do mês de referência
        print(f"Baixando fatura de {faturas_info[0][0].strftime('%m/%Y')}...")
        faturas_info[0][1].click()
        
        # Extrai o arquivo ZIP
        extrair_zip(criar_pasta_ae())
        
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"Erro ao processar empresa {codigo_ons}: {str(e)}")
        return False

def acessar_dom_pedro():
    # Criar pasta AE e configurar Chrome para baixar nela
    pasta_ae = criar_pasta_ae()
    
    # Configurar opções do Chrome para download na pasta RE
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": pasta_ae,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        for codigo in CODIGOS_ONS:
            sucesso = processar_empresa(driver, codigo)
            
            if not sucesso:
                print(f"Falha ao processar empresa {codigo}, continuando com a próxima...")
            
            time.sleep(2)
            
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    acessar_dom_pedro()
