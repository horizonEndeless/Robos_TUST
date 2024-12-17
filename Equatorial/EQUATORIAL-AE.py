from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def esperar_download(caminho, timeout=30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        if any(arquivo.endswith('.crdownload') for arquivo in os.listdir(caminho)):
            time.sleep(1)
        else:
            return True
    return False

def baixar_arquivo(driver, url, caminho, nome_arquivo):
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    
    response = s.get(url, allow_redirects=True)
    if response.status_code == 200:
        with open(os.path.join(caminho, nome_arquivo), 'wb') as f:
            f.write(response.content)
        print(f"Arquivo {nome_arquivo} baixado com sucesso em {caminho}.")
        return True
    else:
        print(f"Falha ao baixar {nome_arquivo}. Status code: {response.status_code}")
        return False

def processar_empresa_sp(empresa_info, sp_code, base_download_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options=chrome_options)

    try:
        empresa_path = os.path.join(base_download_path, empresa_info['empresa'])
        sp_path = os.path.join(empresa_path, sp_code)
        os.makedirs(sp_path, exist_ok=True)
        print(f"Processando {sp_code} para {empresa_info['empresa']}")

        driver.get("https://www.equatorial-t.com.br/segunda-via-transmissao/")
        wait = WebDriverWait(driver, 20)

        # Preencher campos e fazer login
        campo_cnpj = wait.until(EC.element_to_be_clickable((By.ID, "user_cnpj")))
        campo_cnpj.send_keys(empresa_info['cnpj'])
        campo_ons = wait.until(EC.element_to_be_clickable((By.ID, "user_ons")))
        campo_ons.send_keys(empresa_info['ons'])
        campo_spe = wait.until(EC.element_to_be_clickable((By.ID, "user_spe")))
        campo_spe.send_keys(sp_code)

        print(f"Campos preenchidos para {empresa_info['empresa']} - {sp_code}")

        # Rolar até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Esperar um pouco após a rolagem

        # Tentar fechar o aviso de cookies, se existir
        try:
            botao_cookies = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            botao_cookies.click()
            print("Aviso de cookies fechado.")
        except:
            print("Aviso de cookies não encontrado ou já fechado.")

        # Localizar e clicar no botão ENTRAR
        botao_entrar = wait.until(EC.element_to_be_clickable((By.ID, "wp-submit")))
        ActionChains(driver).move_to_element(botao_entrar).click().perform()

        print("Botão ENTRAR clicado com sucesso.")

        # Verificar se estamos na página correta após o login
        wait.until(EC.presence_of_element_located((By.XPATH, f"//h3[contains(text(), 'Faturas para ONS {empresa_info['ons']}')]")))
        print("Login bem-sucedido. Estamos na página de faturas.")

        # Processar boletos
        linhas_tabela = driver.find_elements(By.XPATH, "//table//tr")
        boletos_processados = 0
        boletos_em_aberto = []

        for linha in linhas_tabela[1:]:
            try:
                celulas = linha.find_elements(By.XPATH, ".//td")
                if len(celulas) < 6:  # Assumindo que há pelo menos 6 colunas na tabela
                    continue

                status_element = linha.find_element(By.XPATH, ".//td[1]//span[contains(@class, 'label-status')]")
                if "em aberto" in status_element.text.lower():
                    mes = celulas[3].text
                    ano = celulas[4].text
                    link_xml = celulas[5].find_element(By.XPATH, ".//a").get_attribute("href")
                    link_pdf = celulas[6].find_element(By.XPATH, ".//a").get_attribute("href")
                    
                    data = datetime.strptime(f"{mes}/{ano}", "%m/%Y")
                    boletos_em_aberto.append((data, link_xml, link_pdf))

            except Exception as e:
                print(f"Erro ao processar linha da tabela para {empresa_info['empresa']} - {sp_code}: {e}")

        if boletos_em_aberto:
            # Ordenar boletos pelo mês/ano mais recente
            boletos_em_aberto.sort(key=lambda x: x[0], reverse=True)
            data_mais_recente, link_xml, link_pdf = boletos_em_aberto[0]

            nome_arquivo_xml = f"{empresa_info['empresa']}_{sp_code}_fatura_{data_mais_recente.strftime('%m_%Y')}.xml"
            nome_arquivo_pdf = f"{empresa_info['empresa']}_{sp_code}_fatura_{data_mais_recente.strftime('%m_%Y')}.pdf"

            if baixar_arquivo(driver, link_xml, sp_path, nome_arquivo_xml):
                print(f"XML baixado para {empresa_info['empresa']} - {sp_code}: {nome_arquivo_xml}")
            if baixar_arquivo(driver, link_pdf, sp_path, nome_arquivo_pdf):
                print(f"PDF baixado para {empresa_info['empresa']} - {sp_code}: {nome_arquivo_pdf}")

            boletos_processados = 1

        print(f"Total de boletos processados para {empresa_info['empresa']} - {sp_code}: {boletos_processados}")

        # Encerrar sessão
        try:
            botao_encerrar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/section[2]/div/div/p[2]/a"))
            )
            botao_encerrar.click()
            print(f"Sessão encerrada para {empresa_info['empresa']} - {sp_code}.")
        except Exception as e:
            print(f"Erro ao encerrar sessão para {empresa_info['empresa']} - {sp_code}: {e}")

    except Exception as e:
        print(f"Erro ao processar {empresa_info['empresa']} - {sp_code}: {e}")
    finally:
        driver.quit()

def acessar_site_equatorial():
    base_download_path = r"C:\Users\Bruno\Downloads\EQUATORIAL"
    
    # Lista de empresas (mantida como estava)
    empresas = [
        {"cnpj": "30520122000170", "ons": "3859", "codigo": "", "empresa": "SJP1"},
        {"cnpj": "30432072000179", "ons": "3860", "codigo": "", "empresa": "SJP2"},
        {"cnpj": "30486042000145", "ons": "3861", "codigo": "", "empresa": "SJP3"},
        {"cnpj": "30425445000184", "ons": "3862", "codigo": "", "empresa": "SJP4"},
        {"cnpj": "30456405000108", "ons": "3863", "codigo": "", "empresa": "SJP5"},
        {"cnpj": "30421756000175", "ons": "3864", "codigo": "", "empresa": "SJP6"},
        {"cnpj": "14285232000148", "ons": "3740", "codigo": "", "empresa": "COR1"},
        {"cnpj": "14285242000183", "ons": "3741", "codigo": "", "empresa": "COR2"},
        {"cnpj": "24342513000149", "ons": "3750", "codigo": "", "empresa": "COR3"},
        {"cnpj": "10500221000182", "ons": "8011", "codigo": "", "empresa": "LIBRA"}
        
    ]

    max_workers = 4  # Número de navegadores simultâneos aumentado para 4

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for empresa_info in empresas:
            for sp in range(1, 9):  # SP01 até SP08
                sp_code = f"SP0{sp}"
                futures.append(executor.submit(processar_empresa_sp, empresa_info, sp_code, base_download_path))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Uma tarefa falhou: {e}")

if __name__ == "__main__":
    acessar_site_equatorial()
