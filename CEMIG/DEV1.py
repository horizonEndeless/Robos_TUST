import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CEMIGDownloader:
    def __init__(self):
        self.download_path = r"C:\Users\Bruno\Downloads\TUST\CEMIG"
        
        # Garantir que o diretório de download exista
        os.makedirs(self.download_path, exist_ok=True)
        
        # Configurar o Chrome para baixar arquivos automaticamente para o diretório especificado
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        
        # Inicializar o driver do Chrome
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.base_url = "https://web.cemig.com.br/frbe"
        
    def iniciar_sessao(self):
        """Inicia a sessão no site da CEMIG"""
        try:
            self.driver.get(self.base_url)
            print("Sessão iniciada com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao iniciar sessão: {e}")
            return False
    
    def pesquisar_empresa(self, codigo_empresa):
        """Pesquisa a empresa pelo código ONS"""
        try:
            # Encontrar o campo de entrada e inserir o código
            input_ons = self.driver.find_element(By.ID, "ONS")
            input_ons.clear()
            input_ons.send_keys(codigo_empresa)
            
            print(f"Inserido código da empresa: {codigo_empresa}")
            
            # Mostrar o elemento de loading antes de clicar
            print("Verificando elemento de loading...")
            loading_element = self.driver.find_element(By.ID, "loading")
            print(f"Estado inicial do loading: {loading_element.get_attribute('style')}")
            
            # Clicar no botão de pesquisa
            botao_pesquisar = self.driver.find_element(By.ID, "btnPesquisar")
            botao_pesquisar.click()
            
            print("Botão de pesquisa clicado, aguardando carregamento...")
            
            # Aguardar que o elemento de loading apareça (display diferente de none)
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda driver: "display: none" not in driver.find_element(By.ID, "loading").get_attribute("style")
                )
                print("Loading visível, aguardando resultados...")
            except:
                print("Elemento de loading não ficou visível, mas continuando...")
            
            # Aguardar que o elemento de loading desapareça (display: none)
            try:
                WebDriverWait(self.driver, 30).until(
                    lambda driver: "display: none" in driver.find_element(By.ID, "loading").get_attribute("style")
                )
                print("Loading concluído!")
            except:
                print("Elemento de loading não desapareceu, mas continuando...")
            
            # Aguardar um tempo fixo para garantir
            print("Aguardando 5 segundos adicionais...")
            time.sleep(5)
            
            # Verificar se a div contentAjax foi preenchida
            content_ajax = self.driver.find_element(By.CLASS_NAME, "contentAjax")
            content_html = content_ajax.get_attribute("innerHTML").strip()
            
            print(f"Conteúdo da div contentAjax: {len(content_html)} caracteres")
            
            if len(content_html) < 10:  # Se estiver praticamente vazia
                print("A div contentAjax parece vazia. Tentando abordagem alternativa...")
                
                # Tentar executar o JavaScript diretamente
                try:
                    # Reenviar a requisição AJAX manualmente
                    ajax_result = self.driver.execute_script("""
                        var result;
                        $.ajax({
                            url: '/FRBE/Home/Pesquisar',
                            type: 'POST',
                            data: { ONS: arguments[0] },
                            async: false,
                            success: function(data) {
                                result = data;
                                $('.contentAjax').html(data);
                            }
                        });
                        return result;
                    """, codigo_empresa)
                    
                    print("Requisição AJAX executada manualmente")
                    
                    # Aguardar um pouco mais
                    time.sleep(3)
                    
                    # Verificar novamente o conteúdo
                    content_ajax = self.driver.find_element(By.CLASS_NAME, "contentAjax")
                    content_html = content_ajax.get_attribute("innerHTML").strip()
                    print(f"Novo conteúdo da div contentAjax: {len(content_html)} caracteres")
                except Exception as ajax_error:
                    print(f"Erro ao executar AJAX manualmente: {ajax_error}")
            
            # Verificar se há links de download
            links = self.driver.find_elements(By.TAG_NAME, "a")
            links_download = [link for link in links if "VisualizarArquivo" in (link.get_attribute("onclick") or "")]
            
            print(f"Encontrados {len(links_download)} links de download")
            
            if not links_download:
                print("Nenhum link de download encontrado. Salvando página atual...")
                
                # Salvar screenshot para diagnóstico
                screenshot_path = os.path.join(self.download_path, f"sem_links_{codigo_empresa}.png")
                self.driver.save_screenshot(screenshot_path)
                print(f"Screenshot salvo em: {screenshot_path}")
                
                # Salvar HTML para diagnóstico
                with open(os.path.join(self.download_path, f"pagina_sem_links_{codigo_empresa}.html"), "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                
                # Tentar uma última abordagem - recarregar a página e tentar novamente
                print("Tentando recarregar a página e pesquisar novamente...")
                self.driver.refresh()
                time.sleep(2)
                
                # Encontrar o campo de entrada e inserir o código novamente
                input_ons = self.driver.find_element(By.ID, "ONS")
                input_ons.clear()
                input_ons.send_keys(codigo_empresa)
                
                # Clicar no botão de pesquisa novamente
                botao_pesquisar = self.driver.find_element(By.ID, "btnPesquisar")
                botao_pesquisar.click()
                
                # Aguardar mais tempo
                print("Aguardando 10 segundos após segunda tentativa...")
                time.sleep(10)
                
                # Verificar novamente se há links
                links = self.driver.find_elements(By.TAG_NAME, "a")
                links_download = [link for link in links if "VisualizarArquivo" in (link.get_attribute("onclick") or "")]
                print(f"Segunda tentativa: Encontrados {len(links_download)} links de download")
                
                if not links_download:
                    return False
            
            # Salvar a página de resultados para análise
            with open(os.path.join(self.download_path, f"resultados_{codigo_empresa}.html"), "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            
            print(f"Pesquisa para empresa {codigo_empresa} realizada com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao pesquisar empresa: {e}")
            
            # Salvar screenshot para diagnóstico
            screenshot_path = os.path.join(self.download_path, f"erro_{codigo_empresa}.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot salvo em: {screenshot_path}")
            
            return False
    
    def baixar_arquivos(self, tipo_arquivo=None):
        """Baixa os arquivos encontrados na página de resultados"""
        try:
            # Aguardar um momento para garantir que a página está completamente carregada
            time.sleep(2)
            
            # Encontrar todos os links com VisualizarArquivo na página
            links = self.driver.find_elements(By.TAG_NAME, "a")
            links_download = [link for link in links if "VisualizarArquivo" in (link.get_attribute("onclick") or "")]
            
            print(f"Encontrados {len(links_download)} links de download")
            
            if not links_download:
                print("Nenhum link de download encontrado. Salvando página atual...")
                with open(os.path.join(self.download_path, "pagina_sem_links.html"), "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                return False
            
            # Contador para acompanhar os downloads
            downloads_realizados = 0
            
            for link in links_download:
                texto_link = link.text.strip().lower()
                onclick = link.get_attribute("onclick")
                
                # Verificar se o link corresponde ao tipo de arquivo desejado
                if tipo_arquivo:
                    if tipo_arquivo.lower() == "boleto" and "boleto" not in texto_link:
                        continue
                    elif tipo_arquivo.lower() == "xml" and "xml" not in texto_link:
                        continue
                    elif tipo_arquivo.lower() == "danfe" and "danfe" not in texto_link:
                        continue
                
                # Extrair o nome do arquivo do atributo onclick
                import re
                match = re.search(r'VisualizarArquivo\("([^"]+)"\)', onclick)
                if match:
                    nome_arquivo = match.group(1)
                    print(f"Tentando baixar: {nome_arquivo}")
                    
                    # Rolar até o link para garantir que está visível
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(0.5)  # Pequena pausa após rolagem
                    
                    # Clicar no link para iniciar o download
                    link.click()
                    
                    # Aguardar um tempo para o download iniciar
                    time.sleep(3)
                    
                    downloads_realizados += 1
            
            # Aguardar um tempo para os downloads concluírem
            if downloads_realizados > 0:
                print(f"Aguardando a conclusão de {downloads_realizados} downloads...")
                time.sleep(5 * downloads_realizados)  # 5 segundos por arquivo
                print("Downloads concluídos")
                return True
            else:
                print("Nenhum arquivo encontrado para download")
                return False
            
        except Exception as e:
            print(f"Erro ao baixar arquivos: {e}")
            
            # Salvar screenshot para diagnóstico
            screenshot_path = os.path.join(self.download_path, "erro_download.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot salvo em: {screenshot_path}")
            
            return False
    
    def baixar_boletos(self):
        """Baixa os boletos encontrados na página de resultados"""
        return self.baixar_arquivos("boleto")
    
    def baixar_xmls(self):
        """Baixa os XMLs encontrados na página de resultados"""
        return self.baixar_arquivos("xml")
    
    def baixar_danfes(self):
        """Baixa os DANFEs encontrados na página de resultados"""
        return self.baixar_arquivos("danfe")
    
    def fechar(self):
        """Fecha o navegador"""
        self.driver.quit()

    def verificar_javascript(self):
        """Verifica se o JavaScript está sendo executado corretamente"""
        try:
            # Tentar executar um JavaScript simples
            resultado = self.driver.execute_script("return document.readyState")
            print(f"Estado do documento: {resultado}")
            
            # Verificar se a função VisualizarArquivo existe
            existe_funcao = self.driver.execute_script("return typeof VisualizarArquivo !== 'undefined'")
            if existe_funcao:
                print("Função VisualizarArquivo encontrada!")
            else:
                print("Função VisualizarArquivo NÃO encontrada. Verificando scripts...")
                
                # Listar todos os scripts carregados
                scripts = self.driver.execute_script("""
                    var scripts = [];
                    var scriptElements = document.getElementsByTagName('script');
                    for (var i = 0; i < scriptElements.length; i++) {
                        scripts.push(scriptElements[i].src);
                    }
                    return scripts;
                """)
                
                print("Scripts carregados:")
                for script in scripts:
                    print(f"  - {script}")
            
            return True
        except Exception as e:
            print(f"Erro ao verificar JavaScript: {e}")
            return False

def main():
    # Exemplo de uso
    codigo_empresa = "3748"  # Código de exemplo mencionado
    
    downloader = CEMIGDownloader()
    
    try:
        # Iniciar sessão
        if downloader.iniciar_sessao():
            # Verificar JavaScript
            downloader.verificar_javascript()
            
            # Tentar até 3 vezes
            for tentativa in range(1, 4):
                print(f"\n=== Tentativa {tentativa} de 3 ===\n")
                
                # Pesquisar empresa
                if downloader.pesquisar_empresa(codigo_empresa):
                    # Verificar JavaScript novamente após a pesquisa
                    downloader.verificar_javascript()
                    
                    # Aguardar um momento para garantir que a página está completamente carregada
                    print("Aguardando 5 segundos para garantir carregamento completo...")
                    time.sleep(5)
                    
                    # Baixar todos os tipos de documentos
                    if downloader.baixar_arquivos():
                        print("Download concluído com sucesso!")
                        break
                    else:
                        print(f"Falha no download na tentativa {tentativa}")
                        
                        if tentativa < 3:
                            print("Tentando novamente...")
                            # Recarregar a página para nova tentativa
                            downloader.driver.get(downloader.base_url)
                            time.sleep(3)
                else:
                    print(f"Falha na pesquisa na tentativa {tentativa}")
                    
                    if tentativa < 3:
                        print("Tentando novamente...")
                        # Recarregar a página para nova tentativa
                        downloader.driver.get(downloader.base_url)
                        time.sleep(3)
    finally:
        # Garantir que o navegador seja fechado mesmo em caso de erro
        downloader.fechar()

if __name__ == "__main__":
    main()
