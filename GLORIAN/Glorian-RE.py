from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc  # Para sites com detecção de automação
from bs4 import BeautifulSoup  # Para análise do HTML
import time

def iniciar_navegador():
    try:
        # Tentativa 1: Chrome não detectável
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        driver = uc.Chrome(options=options)
        print("Navegador não detectável iniciado")
    except:
        # Tentativa 2: Chrome normal
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # Adicionar argumentos para evitar detecção
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # Modificar navigator.webdriver
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("Navegador padrão iniciado")
    return driver

def analisar_pagina(driver):
    # Analisar HTML com BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Procurar todos os botões na página
    botoes = soup.find_all('button')
    print("\nBotões encontrados na página:")
    for botao in botoes:
        print(f"Texto: {botao.text.strip()}")
        print(f"Classes: {botao.get('class', 'Sem classe')}")
        print(f"ID: {botao.get('id', 'Sem ID')}")
        print("---")

def analisar_tabela(driver, wait):
    try:
        print("\nIniciando análise detalhada da tabela Glorian...")
        time.sleep(5)  # Aguardar carregamento completo
        
        # Localizar o container principal como no C#
        container_selector = "div[style='position: absolute; overflow: hidden; width: 100%; height: 100%; left: 30px;'] > div"
        containers = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, container_selector))
        )
        
        if len(containers) > 1:
            # Pegando o segundo div como no código C#: elementsDiv[1]
            tabela_container = containers[1]
            
            # Localizar as linhas da tabela
            linhas = tabela_container.find_elements(By.CSS_SELECTOR, "table > tbody > tr")
            print(f"\nTotal de linhas encontradas: {len(linhas)}")
            
            for i, linha in enumerate(linhas[:3]):  # Analisando 3 primeiras linhas
                print(f"\nAnalisando linha {i+1}:")
                
                # Encontrar todas as colunas (similar ao columns no C#)
                colunas = linha.find_elements(By.TAG_NAME, "td")
                
                if len(colunas) >= 20:  # O C# acessa a coluna 19 para vencimento
                    dados = {
                        'Vencimento': colunas[19].text,
                        'Empresa': colunas[7].text if len(colunas) > 7 else 'N/A',
                        'Links': []
                    }
                    
                    # Procurar botões de download como no C#
                    try:
                        xml_btn = linha.find_element(By.CSS_SELECTOR, "div[title='Download do XML da NF-e.']")
                        dados['Links'].append('XML encontrado')
                    except:
                        pass
                        
                    try:
                        danfe_btn = linha.find_element(By.CSS_SELECTOR, "div[title='Download do Danfe da NFe.']")
                        dados['Links'].append('DANFE encontrado')
                    except:
                        pass
                        
                    try:
                        boleto_btn = linha.find_element(By.CSS_SELECTOR, "div[title='Download do boleto']")
                        dados['Links'].append('Boleto encontrado')
                    except:
                        pass
                    
                    print(f"Dados encontrados:")
                    print(f"  Vencimento: {dados['Vencimento']}")
                    print(f"  Empresa: {dados['Empresa']}")
                    print(f"  Links disponíveis: {', '.join(dados['Links'])}")
                    
            # Debug: Mostrar estrutura HTML da primeira linha
            if linhas:
                print("\nEstrutura HTML da primeira linha para debug:")
                html_linha = linhas[0].get_attribute('outerHTML')
                soup = BeautifulSoup(html_linha, 'html.parser')
                print(soup.prettify())
                
        else:
            print("Container da tabela não encontrado corretamente")
            
    except Exception as e:
        print(f"Erro durante análise: {str(e)}")
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            print("\nEstrutura atual da página:")
            print(soup.prettify()[:1000])
        except:
            print("Não foi possível mostrar a estrutura da página")

def acessar_site():
    try:
        driver = iniciar_navegador()
        print("Navegador iniciado com sucesso")
        
        url = "https://bp.glorian.com.br/bpglportal/"
        driver.get(url)
        print("Site acessado com sucesso")

        # Espera explícita
        wait = WebDriverWait(driver, 15)

        # Inserir email
        email_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @type='email']"))
        )
        email_field.clear()
        email_field.send_keys("carolina.ferreira@pontalenergy.com")
        print("Email inserido com sucesso")

        # Analisar a página para debug
        print("\nAnalisando estrutura da página...")
        analisar_pagina(driver)

        # Tentar diferentes métodos para encontrar e clicar no botão
        metodos_botao = [
            (By.XPATH, "//button[normalize-space()='Próximo']"),
            (By.XPATH, "//button[contains(., 'Próximo')]"),
            (By.XPATH, "//*[text()='Próximo']"),
            (By.CSS_SELECTOR, "button"),
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//button[contains(@class, 'proximo')]")
        ]

        for locator in metodos_botao:
            try:
                print(f"\nTentando localizar botão com: {locator}")
                botao = wait.until(EC.element_to_be_clickable(locator))
                print("Botão encontrado, tentando clicar...")
                
                # Tentativa 1: Clique direto
                try:
                    botao.click()
                    print("Clique direto successful")
                    break
                except:
                    # Tentativa 2: JavaScript
                    try:
                        driver.execute_script("arguments[0].click();", botao)
                        print("Clique JavaScript successful")
                        break
                    except:
                        # Tentativa 3: Action Chains
                        try:
                            ActionChains(driver).move_to_element(botao).click().perform()
                            print("Clique Action Chains successful")
                            break
                        except:
                            # Tentativa 4: Enter
                            try:
                                botao.send_keys(Keys.RETURN)
                                print("Clique via Enter successful")
                                break
                            except Exception as e:
                                print(f"Falha em todas as tentativas de clique: {str(e)}")
                                continue
            except:
                continue

        # Verificar resultado e inserir senha
        try:
            campo_senha = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            print("\nSucesso! Campo de senha encontrado!")
            
            # Inserir a senha
            campo_senha.clear()
            campo_senha.send_keys("Pontal@2024")  # Substitua pela senha correta
            print("Senha inserida com sucesso")

            # Procurar e clicar no botão de login
            metodos_botao_login = [
                (By.XPATH, "//button[normalize-space()='Login']"),
                (By.XPATH, "//button[contains(., 'Login')]"),
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//*[text()='Login']"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]

            for locator in metodos_botao_login:
                try:
                    print(f"\nTentando localizar botão de login com: {locator}")
                    botao_login = wait.until(EC.element_to_be_clickable(locator))
                    print("Botão de login encontrado, tentando clicar...")
                    
                    # Tentativas de clique
                    try:
                        # Clique direto
                        botao_login.click()
                        print("Clique no botão login realizado com sucesso")
                        break
                    except:
                        try:
                            # JavaScript click
                            driver.execute_script("arguments[0].click();", botao_login)
                            print("Clique via JavaScript no botão login realizado")
                            break
                        except:
                            try:
                                # Action Chains
                                ActionChains(driver).move_to_element(botao_login).click().perform()
                                print("Clique via Action Chains no botão login realizado")
                                break
                            except Exception as e:
                                print(f"Falha ao clicar no botão login: {str(e)}")
                                continue
                except:
                    continue

        except TimeoutException:
            print("\nNão foi possível encontrar o campo de senha após as tentativas")

        # Aguardar carregamento da página principal
        time.sleep(5)  # Aguardar carregamento inicial
        print("\nProcurando link 'Notas Fiscais'...")

        # Diferentes tentativas de localizar o elemento Notas Fiscais
        metodos_notas_fiscais = [
            (By.XPATH, "//p[text()='Notas Fiscais']"),
            (By.XPATH, "//p[@tabindex='0'][contains(text(),'Notas Fiscais')]"),
            (By.CSS_SELECTOR, "p[tabindex='0'][style*='cursor: pointer']"),
            (By.XPATH, "//*[contains(text(),'Notas Fiscais')]")
        ]

        for locator in metodos_notas_fiscais:
            try:
                print(f"Tentando localizar Notas Fiscais com: {locator}")
                notas_fiscais = wait.until(EC.element_to_be_clickable(locator))
                print("Elemento 'Notas Fiscais' encontrado, tentando clicar...")

                # Tentativas de clique
                try:
                    # Clique direto
                    notas_fiscais.click()
                    print("Clique em Notas Fiscais realizado com sucesso")
                    
                    # Verificar se a tabela de faturas carregou
                    try:
                        tabela = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                        print("Tabela de faturas encontrada!")
                        # Adicionar análise da tabela
                        analisar_tabela(driver, wait)
                        break
                    except TimeoutException:
                        print("Tabela de faturas não encontrada após o clique")
                        
                except:
                    try:
                        # JavaScript click
                        driver.execute_script("arguments[0].click();", notas_fiscais)
                        print("Clique via JavaScript realizado")
                        time.sleep(3)
                        break
                    except:
                        try:
                            # Action Chains
                            ActionChains(driver).move_to_element(notas_fiscais).click().perform()
                            print("Clique via Action Chains realizado")
                            time.sleep(3)
                            break
                        except Exception as e:
                            print(f"Falha ao clicar em Notas Fiscais: {str(e)}")
                            continue
            except:
                continue

        # Analisar estrutura da página após clique
        print("\nAnalisando estrutura da página após clique em Notas Fiscais...")
        analisar_pagina(driver)

        # Manter navegador aberto
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"Erro geral: {str(e)}")

if __name__ == "__main__":
    acessar_site()
