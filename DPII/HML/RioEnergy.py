from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

# Lista de códigos ONS
CODIGOS_ONS = [
    "4314", "3430", "3431", "3432", "4415", "4315", 
    "3502", "3497", "3505", "3530", "3498", "3531", 
    "3534", "3537", "3538", "3947", "3948", "3969", 
    "3970", "3976", "4316" , "4313" , "3503"
    
]

def criar_pasta_re():
    pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    pasta_re = os.path.join(pasta_downloads, "RE")
    
    if not os.path.exists(pasta_re):
        os.makedirs(pasta_re)
        print("Pasta RE criada com sucesso!")
    
    return pasta_re

def processar_empresa(driver, codigo_ons):
    try:
        print(f"\nProcessando empresa código: {codigo_ons}")
        
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
                # Encontrar o texto da fatura que contém a data
                texto_fatura = secao.find_element(By.CSS_SELECTOR, "h3#textoFaturas").text
                # Extrair a data do texto (formato: "Fatura XXXXX (MM/YYYY)")
                data_texto = texto_fatura.split('(')[1].strip(')')
                mes, ano = data_texto.split('/')
                # Construir a data completa (assumindo dia 25 conforme exemplo)
                data_completa = f"25/{mes}/{ano}"
                data_obj = datetime.strptime(data_completa, "%d/%m/%Y")
                
                # Encontrar o botão XML na mesma seção
                botao_xml = secao.find_element(By.CSS_SELECTOR, 
                    "button.btn-imprimir.dropbtn-imprimir.float-left.btn-download-color.linkDownloadXml")
                
                faturas_info.append((data_obj, botao_xml))
            except Exception as e:
                print(f"Erro ao processar seção: {str(e)}")
                continue
        
        if not faturas_info:
            print("Não foi possível encontrar faturas válidas")
            return False
            
        # Encontrar a fatura mais recente
        fatura_mais_recente = max(faturas_info, key=lambda x: x[0])
        print(f"Data de vencimento mais recente: {fatura_mais_recente[0].strftime('%d/%m/%Y')}")
        
        # Clicar no botão XML da fatura mais recente
        print("Botão XML encontrado, iniciando download...")
        fatura_mais_recente[1].click()
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"Erro ao processar empresa {codigo_ons}: {str(e)}")
        return False

def acessar_dom_pedro():
    # Criar pasta RE e configurar Chrome para baixar nela
    pasta_re = criar_pasta_re()
    
    # Configurar opções do Chrome para download na pasta RE
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": pasta_re,
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
