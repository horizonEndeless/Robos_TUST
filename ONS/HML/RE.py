from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações do ChromeDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Descomente para executar em modo headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Iniciar o navegador usando o WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Acessar a página de login
    driver.get("https://sintegre.ons.org.br/sites/1/18/paginas/servicos/historico-de-produtos.aspx")

    # Esperar até que o campo de nome de usuário esteja presente
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("tust@rioenergy.com.br")

    # Esperar até que o campo de senha esteja presente
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("Ca2003@#")

    # Simular um pequeno atraso antes de clicar no botão de login
    time.sleep(2)

    # Submeter o formulário
    login_button = driver.find_element(By.ID, "kc-login")
    login_button.click()

    # Esperar um pouco para garantir que o login foi processado
    time.sleep(5)

    # Verificar se o login foi bem-sucedido
    if "alguma_palavra_chave_que_indica_sucesso" in driver.page_source:
        print("Login bem-sucedido!")
    else:
        print("Falha no login.")

finally:
    # Fechar o navegador
    driver.quit()
