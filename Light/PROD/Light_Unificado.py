from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
import requests

class LightRobot:
    def __init__(self, tipo_empresa="RE"):
        # Adicionar configuração do mês de competência
        self.mes_competencia = 3  #(fácil de alterar)
        self.ano = 2025
        self.tipo_empresa = tipo_empresa.upper()  # RE, AE ou DE
        
        # Configurar opções do Firefox
        firefox_options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=firefox_options)
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        
        # Selecionar a lista de empresas com base no tipo
        self.empresas = self.obter_lista_empresas()

    def obter_lista_empresas(self):
        if self.tipo_empresa == "RE":
            return [
                # BRJA e BRJB
                {"cnpj": "33485728/0001-00", "ons": "4313", "pasta": "BRJA", "cliente": "1108376"},
                {"cnpj": "33485874/000135", "ons": "4314", "pasta": "BRJB", "cliente": "1108377"},
                
                # CECA até CECE
                {"cnpj": "19233858000205", "ons": "3430", "pasta": "CECA", "cliente": "1101532"},
                {"cnpj": "19.235.607/0002-60", "ons": "3431", "pasta": "CECB", "cliente": "1101533"},
                {"cnpj": "19.560.109/0002-92", "ons": "3432", "pasta": "CECC", "cliente": "1101534"},
                {"cnpj": "33.457.932/0001-17", "ons": "4415", "pasta": "CECD", "cliente": "1108935"},
                {"cnpj": "33471379000177", "ons": "4315", "pasta": "CECE", "cliente": "1108378"},
                {"cnpj": "33468809000100", "ons": "4316", "pasta": "CECF", "cliente": "1108379"},
                
                # ITA1 até ITA9
                {"cnpj": "19.560.032/0002-50", "ons": "3502", "pasta": "ITA1", "cliente": "1101690"},
                {"cnpj": "19.560.074/0002-91", "ons": "3497", "pasta": "ITA2", "cliente": "1101632"},
                {"cnpj": "19.560.839/0002-93", "ons": "3503", "pasta": "ITA3", "cliente": "1101691"},
                {"cnpj": "20.553.751/0002-23", "ons": "3530", "pasta": "ITA4", "cliente": "1101738"},
                {"cnpj": "19.560.868/0002-55", "ons": "3498", "pasta": "ITA5", "cliente": "1101633"},
                {"cnpj": "20.533.879/0002-25", "ons": "3531", "pasta": "ITA6", "cliente": "1101739"},
                {"cnpj": "20.533.473/0002-42", "ons": "3532", "pasta": "ITA7", "cliente": "1101753"},
                {"cnpj": "20.533.310/0002-60", "ons": "3537", "pasta": "ITA8", "cliente": "1101754"},
                {"cnpj": "20.533.377/0002-02", "ons": "3538", "pasta": "ITA9", "cliente": "1101755"},
                
                # SDBA até SDBE
                {"cnpj": "30.063.842/0002-34", "ons": "3947", "pasta": "SDBA", "cliente": "1105036"},
                {"cnpj": "29.527.877/0002-06", "ons": "3948", "pasta": "SDBB", "cliente": "1105047"},
                {"cnpj": "29.591.504/0002-96", "ons": "3969", "pasta": "SDBC", "cliente": "1105267"},
                {"cnpj": "30.062.725/0002-56", "ons": "3970", "pasta": "SDBD", "cliente": "1105268"},
                {"cnpj": "30.062.736/0002-36", "ons": "3976", "pasta": "SDBE", "cliente": "1105116"},
                {"cnpj": "30.234.798/0002-88", "ons": "3972", "pasta": "SDBF", "cliente": "1105385"},
            ]
        elif self.tipo_empresa == "AE":
            return [
                # CELEO
                {"cnpj": "30.520.122/0001-70", "ons": "3859", "pasta": "SJP_I", "cliente": "1103697"},
                {"cnpj": "30.432.072/0001-79", "ons": "3860", "pasta": "SJP_II", "cliente": "1103698"},
                {"cnpj": "30.486.042/0001-45", "ons": "3861", "pasta": "SJP_III", "cliente": "1103699"},
                {"cnpj": "30.425.445/0001-84", "ons": "3862", "pasta": "SJP_IV", "cliente": "1103700"},
                {"cnpj": "30.456.405/0001-08", "ons": "3863", "pasta": "SJP_V", "cliente": "1103701"},
                {"cnpj": "30.421.756/0001-75", "ons": "3864", "pasta": "SJP_VI", "cliente": "1103702"},
                
                # COREMAS
                {"cnpj": "14.285.232/0001-48", "ons": "3740", "pasta": "COREMAS_I", "cliente": "1102652"},
                {"cnpj": "14.285.242/0001-83", "ons": "3741", "pasta": "COREMAS_II", "cliente": "1102653"},
                {"cnpj": "24.342.513/0001-49", "ons": "3750", "pasta": "COREMAS_III", "cliente": "1102829"},
                
                # LIBRA
                {"cnpj": "10.500.221/0001-82", "ons": "9011", "pasta": "LIBRA", "cliente": "1100243"},
            ]
        elif self.tipo_empresa == "DE":
            return [
                # DIAMANTE
                {"cnpj": "27093977000238", "ons": "3748", "pasta": "DIAMANTE", "cliente": "1103697"},
            ]
        else:
            print(f"Tipo de empresa '{self.tipo_empresa}' não reconhecido. Usando RE como padrão.")
            return self.obter_lista_empresas("RE")

    def processar_empresa(self, empresa):
        max_tentativas_processo = 2  # Número de tentativas para o processo completo
        tentativa = 0
        
        while tentativa < max_tentativas_processo:
            tentativa += 1
            print(f"\nProcessando empresa: CNPJ {empresa['cnpj']} - ONS {empresa['ons']} (Tentativa {tentativa})")
            
            try:
                # Configurar pasta de download
                pasta_base = os.path.join(f"C:\\Users\\Bruno\\Downloads\\TUST\\LIGHT\\{self.tipo_empresa}", empresa["pasta"])
                os.makedirs(pasta_base, exist_ok=True)
                
                self.driver.get("about:config")
                self.driver.find_element(By.ID, "warningButton").click()
                self.driver.execute_script("""
                    Services.prefs.setStringPref("browser.download.dir", arguments[0]);
                    Services.prefs.setIntPref("browser.download.folderList", 2);
                    Services.prefs.setBoolPref("browser.download.useDownloadDir", true);
                """, pasta_base)
                
                # Se o acesso ao site for bem-sucedido, sair do loop
                if self.acessar_site(empresa):
                    break
                
                print(f"Falha na tentativa {tentativa}. {'Tentando novamente...' if tentativa < max_tentativas_processo else 'Número máximo de tentativas atingido.'}")
                
            except Exception as e:
                print(f"Erro ao processar empresa {empresa['cnpj']}: {str(e)}")
                if tentativa < max_tentativas_processo:
                    print("Tentando novamente...")
                    time.sleep(2)
                else:
                    print("Número máximo de tentativas atingido.")

    def executar(self):
        try:
            print(f"\n=== Iniciando processamento para {self.tipo_empresa} ===")
            print(f"Total de empresas a processar: {len(self.empresas)}")
            
            for i, empresa in enumerate(self.empresas):
                print(f"\nEmpresa {i+1}/{len(self.empresas)}")
                self.processar_empresa(empresa)
                time.sleep(5)  # Aguardar entre empresas
                
            print(f"\n=== Processamento para {self.tipo_empresa} concluído ===")
                
        except Exception as e:
            print(f"Erro na execução: {str(e)}")
        finally:
            input("\nPressione ENTER para fechar o navegador...")
            self.driver.quit()

    def acessar_site(self, empresa):
        try:
            print("\n1. Acessando o site...")
            self.driver.get("https://nfe.light.com.br/Web/wfmAutenticar.aspx")
            wait = WebDriverWait(self.driver, 10)
            
            print("2. Preenchendo CNPJ...")
            campo_cnpj = wait.until(EC.presence_of_element_located((By.ID, "tbxCnpj")))
            campo_cnpj.clear()
            campo_cnpj.send_keys(empresa["cnpj"])
            
            print("3. Preenchendo ONS...")
            campo_ons = wait.until(EC.presence_of_element_located((By.ID, "tbxOns")))
            campo_ons.clear()
            campo_ons.send_keys(empresa["ons"])
            
            # Número máximo de tentativas para o CAPTCHA
            max_tentativas = 3
            tentativa = 0
            sucesso = False
            
            while tentativa < max_tentativas and not sucesso:
                tentativa += 1
                print(f"\n4. Tentativa {tentativa} de {max_tentativas} para o CAPTCHA...")
                
                caminho_captcha = self.capturar_captcha()
                if caminho_captcha:
                    print("\n5. Processando imagem do CAPTCHA...")
                    texto_captcha = self.processar_imagem_captcha(caminho_captcha)
                    
                    if texto_captcha:
                        print(f"\n6. Preenchendo campo do CAPTCHA com o texto: {texto_captcha}")
                        campo_captcha = wait.until(EC.presence_of_element_located((By.ID, "tbxCodigoCaptcha")))
                        campo_captcha.clear()  # Limpar campo antes de nova tentativa
                        campo_captcha.send_keys(texto_captcha)
                        
                        print("\n7. Clicando no botão Autenticar...")
                        botao_autenticar = wait.until(EC.element_to_be_clickable((By.ID, "btnAutenticar")))
                        botao_autenticar.click()
                        
                        # Verificar se houve erro no CAPTCHA
                        try:
                            erro_element = wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//span[contains(text(), 'Código de segurança não confere')]")))
                            print("\nCAPTCHA incorreto. Tentando novamente...")
                            
                            # Clicar no botão refresh para nova imagem
                            refresh_button = wait.until(EC.presence_of_element_located((By.ID, "ibnRefresh")))
                            refresh_button.click()
                            time.sleep(1)  # Aguardar nova imagem carregar
                            continue
                            
                        except:
                            # Se não encontrou mensagem de erro, CAPTCHA está correto
                            print("\nCAPTCHA aceito com sucesso!")
                            sucesso = True
                            
                            print("\n8. Aguardando carregamento da página de faturas...")
                            wait.until(EC.url_contains("wfmBuscaNotas.aspx"))
                            time.sleep(3)
                            
                            # Continuar com o resto do processo...
                            print("\n9. Selecionando filtros...")
                            # Selecionar ano
                            select_ano = wait.until(EC.presence_of_element_located((By.ID, "ddlAno")))
                            select_ano.click()
                            opcao_ano = wait.until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, f"option[value='{self.ano}']")))
                            opcao_ano.click()
                            
                            # Selecionar competência
                            select_competencia = wait.until(EC.presence_of_element_located((By.ID, "ddlCompetencia")))
                            select_competencia.click()
                            opcao_mes = wait.until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, f"option[value='{self.mes_competencia}']")))
                            opcao_mes.click()
                            
                            print("\n10. Clicando no botão Buscar...")
                            botao_buscar = wait.until(EC.element_to_be_clickable((By.ID, "btnBuscar")))
                            botao_buscar.click()
                            
                            print("\n11. Aguardando resultados...")
                            time.sleep(1)  # Aguardar carregamento da tabela
                            
                            print("\n12. Iniciando downloads...")
                            self.baixar_arquivos()
            
            if not sucesso:
                print(f"\nTentativa {tentativa} falhou. {'Tentando novamente...' if tentativa < max_tentativas else 'Número máximo de tentativas atingido.'}")
            
            if not sucesso:
                print(f"\nNão foi possível completar o processo para a empresa {empresa['cnpj']} após {max_tentativas} tentativas.")
                return False
                
            return True
            
        except Exception as e:
            print(f"\nERRO: {str(e)}")
            return False

    def processar_imagem_captcha(self, caminho_imagem):
        try:
            image = cv2.imread(caminho_imagem)
            image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            cv2.imwrite(caminho_imagem.replace('.png', '_processada.png'), binary)
            
            resultado = self.ocr.ocr(binary, cls=True)
            
            if resultado:
                texto = ''
                for line in resultado:
                    for word_info in line:
                        texto += word_info[1][0]
                
                texto = ''.join(c for c in texto if c.isalnum())
                print(f"Texto detectado no CAPTCHA: {texto}")
                return texto
            else:
                print("Nenhum texto detectado")
                return None
            
        except Exception as e:
            print(f"Erro ao processar CAPTCHA: {str(e)}")
            return None

    def capturar_captcha(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            captcha_element = wait.until(EC.presence_of_element_located((By.ID, "imgCaptcha")))
            
            pasta_captchas = r'C:\Users\Bruno\Desktop\Workspace\Robos\Light\captchas'
            os.makedirs(pasta_captchas, exist_ok=True)
            
            nome_arquivo = f'captcha_{time.strftime("%Y%m%d-%H%M%S")}.png'
            caminho_completo = os.path.join(pasta_captchas, nome_arquivo)
            
            time.sleep(0.5)
            captcha_element.screenshot(caminho_completo)
            print(f"CAPTCHA salvo em: {caminho_completo}")
            
            return caminho_completo
            
        except Exception as e:
            print(f"Erro ao capturar CAPTCHA: {str(e)}")
            return None

    def baixar_arquivos(self):
        try:
            print("\n1. Localizando links de download...")
            wait = WebDriverWait(self.driver, 10)
            
            # Aguardar a tabela carregar
            wait.until(EC.presence_of_element_located((By.ID, "gvwResultado")))
            
            downloads = self.driver.find_elements(By.LINK_TEXT, "Download")
            
            for i, download_link in enumerate(downloads):
                row = download_link.find_element(By.XPATH, "./ancestor::tr")
                tipo = row.find_element(By.XPATH, ".//td[3]").text
                data_emissao = row.find_element(By.XPATH, ".//td[1]").text
                
                # Baixar XML, BOL e NFE
                if tipo in ["XML", "BOL", "NFE"]:
                    print(f"\n2. Baixando arquivo {tipo} - Data: {data_emissao}...")
                    nome_arquivo = row.find_element(By.XPATH, ".//td[4]").text
                    print(f"Nome do arquivo: {nome_arquivo}")
                    
                    self.driver.execute_script("arguments[0].click();", download_link)
                    time.sleep(3)
                    
                    # Tratamento especial para XML
                    if tipo == "XML":
                        try:
                            erro_element = wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//div[contains(text(), 'Download não verificado')]")
                            ))
                            
                            print(f"Erro no download do XML. Tentando novamente...")
                            fechar_btn = self.driver.find_element(By.CLASS_NAME, "close-button")
                            if fechar_btn:
                                fechar_btn.click()
                                time.sleep(1)
                                self.driver.execute_script("arguments[0].click();", download_link)
                                time.sleep(3)
                                
                        except:
                            print(f"Download do {tipo} parece ter sido bem sucedido")
            
            print("\n3. Downloads concluídos!")
            
        except Exception as e:
            print(f"\nERRO ao baixar arquivos: {str(e)}")


def executar_todos():
    """Executa o processamento para todos os tipos de empresas em sequência"""
    tipos = ["RE", "AE", "DE"]
    
    for tipo in tipos:
        print(f"\n\n{'='*50}")
        print(f"INICIANDO PROCESSAMENTO PARA {tipo}")
        print(f"{'='*50}\n")
        
        robo = LightRobot(tipo)
        robo.executar()
        
        print(f"\n{'='*50}")
        print(f"PROCESSAMENTO PARA {tipo} CONCLUÍDO")
        print(f"{'='*50}\n")


if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1 - Processar apenas RE")
    print("2 - Processar apenas AE")
    print("3 - Processar apenas DE")
    print("4 - Processar todos (RE, AE e DE)")
    
    opcao = input("\nDigite o número da opção desejada: ")
    
    if opcao == "1":
        robo = LightRobot("RE")
        robo.executar()
    elif opcao == "2":
        robo = LightRobot("AE")
        robo.executar()
    elif opcao == "3":
        robo = LightRobot("DE")
        robo.executar()
    elif opcao == "4":
        executar_todos()
    else:
        print("Opção inválida. Executando RE como padrão.")
        robo = LightRobot("RE")
        robo.executar() 