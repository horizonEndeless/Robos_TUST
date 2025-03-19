import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup
import traceback
import re

class TBEPortalClient:
    def __init__(self):
        self.base_url = "https://portalcliente.tbenergia.com.br"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.empresas = []
    
    def login(self, username: str, password: str) -> bool:
        """Realiza login no portal"""
        self.last_username = username  # Guarda credenciais para possível re-login
        self.last_password = password
        
        login_url = f"{self.base_url}/Login/Index"
        payload = {
            "Login": username,
            "Senha": password
        }
        
        try:
            response = self.session.post(
                login_url,
                data=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            # Verifica se o login foi bem sucedido
            if "Fechamento" in response.text:
                print("Login realizado com sucesso!")
                # Após login bem sucedido, já busca as empresas
                self.get_empresas()
                return True
            else:
                print("Login falhou - redirecionamento não encontrado")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Erro no login: {str(e)}")
            return False

    def get_notas_recentes(self, cnpj: str = "") -> Optional[Dict[str, Any]]:
        """Obtém notas fiscais recentes"""
        url = f"{self.base_url}/Fechamento/NotasRecentes"
        params = {
            "CNPJ": cnpj,  # Usa o ID/CNPJ como está
            "_": str(int(datetime.now().timestamp() * 1000))
        }
        
        try:
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'table'})
            
            if not table:
                print("Tabela de notas não encontrada")
                return None
            
            notas = []
            for row in table.find_all('tr')[1:]:  # Pula o cabeçalho
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Inicializa real_cnpj com o CNPJ padrão
                    real_cnpj = "26.643.937/0003-30"  # CNPJ padrão
                    
                    # Verifica se a coluna tem um link
                    link = cols[1].find('a')
                    if link:
                        href = link.get('href', '')
                        # Extrai o CNPJ do link se possível
                        cnpj_match = re.search(r'cnpj=([^&]+)', href)
                        if cnpj_match:
                            real_cnpj = cnpj_match.group(1)
                    
                    nota = {
                        'numero': cols[1].text.strip(),
                        'data': cols[0].text.strip(),
                        'valor': cols[2].text.strip(),
                        'cnpj': real_cnpj
                    }
                    if nota['numero'].strip():
                        notas.append(nota)
                        print(f"Nota encontrada: {nota}")
            
            return {'notas': notas} if notas else None
            
        except Exception as e:
            print(f"Erro ao processar notas: {str(e)}")
            traceback.print_exc()  # Imprime o traceback completo
            return None

    def get_faturas_recentes(self, cnpj: str = "") -> Optional[Dict[str, Any]]:
        """Obtém faturas recentes"""
        url = f"{self.base_url}/Faturas/FaturasRecentes"
        params = {
            "CNPJ": cnpj,
            "_": str(int(datetime.now().timestamp() * 1000))
        }
        
        try:
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar faturas recentes: {str(e)}")
            return None

    def download_xml(self, nfe: str, cnpj: str, tipo: int = 1) -> Optional[bytes]:
        """Download do XML da nota fiscal"""
        url = f"{self.base_url}/Downloads/DownloadXml"
        
        # Usa o CNPJ padrão se não for fornecido um válido
        if len(cnpj.replace(".", "").replace("/", "").replace("-", "")) != 14:
            cnpj = "26.643.937/0003-30"  # CNPJ padrão
        
        params = {
            "Nfe": nfe,
            "cnpj": cnpj.replace(".", "").replace("/", "").replace("-", ""),  # Remove formatação
            "tp": tipo
        }
        
        try:
            print(f"Tentando baixar XML: {url} com params: {params}")
            response = self.session.get(url, params=params, headers=self.headers)
            
            # Adiciona mais informações de debug
            print(f"Status code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Tamanho da resposta: {len(response.content)} bytes")
            
            response.raise_for_status()
            
            if response.content and len(response.content) > 0:
                return response.content
            else:
                print(f"Resposta vazia para nota {nfe}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar XML: {str(e)}")
            traceback.print_exc()  # Imprime o traceback completo
            return None

    def get_empresas(self) -> List[Dict[str, str]]:
        """Obtém lista de empresas/CNPJs disponíveis"""
        url = f"{self.base_url}/Fechamento/Index"
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca o select que contém os CNPJs
            select = soup.find('select', {'id': 'CNPJ'})
            empresas = []
            
            if select:
                print("Select encontrado")  # Debug
                for option in select.find_all('option'):
                    if option.get('value'):
                        texto_completo = option.text.strip()
                        print(f"Processando opção: {texto_completo}")
                        
                        # Mesmo sem o CNPJ, vamos adicionar a empresa usando o ID
                        empresas.append({
                            'cnpj': option['value'],  # Usa o ID como identificador
                            'nome': texto_completo,
                            'id': option['value']
                        })
                        print(f"Empresa encontrada: {texto_completo} - ID: {option['value']}")
            
            # Se não encontrou empresas mas está na página correta, continua
            if not empresas and "login" not in response.text.lower():
                print("Nenhuma empresa encontrada, mas página parece estar correta")
                empresas = [{
                    'cnpj': '3748',  # ID conhecido
                    'nome': 'DIAMANTE GERACAO DE ENERGIA LTDA',
                    'id': '3748'
                }]
            
            # Só tenta re-login se realmente estiver na página de login
            if not empresas and "login" in response.text.lower() and "senha" in response.text.lower():
                print("Página de login detectada, tentando fazer login novamente")
                if self.login(self.last_username, self.last_password):
                    return self.get_empresas()
            
            self.empresas = empresas
            return empresas
            
        except Exception as e:
            print(f"Erro ao obter empresas: {str(e)}")
            return []

    def download_xml_all(self, periodo: str = None) -> Dict[str, Any]:
        """
        Baixa XMLs de todas as empresas disponíveis
        :param periodo: Período opcional no formato MM/YYYY
        :return: Dicionário com resultados por empresa
        """
        resultados = {}
        
        if not self.empresas:
            print("Buscando lista de empresas...")
            self.get_empresas()
        
        if not self.empresas:
            print("Nenhuma empresa encontrada!")
            return resultados
        
        for empresa in self.empresas:
            print(f"\nProcessando empresa: {empresa['nome']}")
            print(f"CNPJ: {empresa['cnpj']}")
            
            notas = self.get_notas_recentes(empresa['cnpj'])
            
            if not notas or not notas.get('notas'):
                print(f"Nenhuma nota encontrada para {empresa['nome']}")
                continue
            
            xmls_baixados = []
            for nota in notas['notas']:
                print(f"Processando nota {nota['numero']}")
                
                # Tenta baixar o XML independente da data
                xml = self.download_xml(
                    nfe=nota['numero'],
                    cnpj=empresa['cnpj']
                )
                if xml:
                    filename = f"xmls/{nota['numero']}_{empresa['cnpj']}.xml"
                    with open(filename, "wb") as f:
                        f.write(xml)
                    xmls_baixados.append(nota['numero'])
                    print(f"XML {filename} baixado com sucesso!")
                else:
                    print(f"Erro ao baixar XML da nota {nota['numero']}")
            
            resultados[empresa['cnpj']] = {
                'nome': empresa['nome'],
                'xmls_baixados': xmls_baixados
            }
        
        return resultados

# Exemplo de uso
if __name__ == "__main__":
    cliente = TBEPortalClient()
    
    if cliente.login("najla1447", "n@jl@1447"):
        print("\nTentando buscar empresas após login...")
        empresas = cliente.get_empresas()
        
        if not empresas:
            print("\nTentando acessar diretamente a página de fechamento...")
            response = cliente.session.get(f"{cliente.base_url}/Fechamento/Index")
            print(f"Status: {response.status_code}")
            print(f"Conteúdo: {response.text[:500]}...")
        
        print("\nEmpresas disponíveis:")
        for empresa in empresas:
            print(f"CNPJ: {empresa['cnpj']} - Nome: {empresa['nome']}")
        
        # Baixa XMLs de todas as empresas
        print("\nBaixando XMLs...")
        resultados = cliente.download_xml_all(periodo="02/2025")  # Opcional: especifica período
        
        # Mostra resultados
        print("\nResultados do download:")
        for cnpj, resultado in resultados.items():
            print(f"\nEmpresa: {resultado['nome']}")
            print(f"CNPJ: {cnpj}")
            print(f"XMLs baixados: {len(resultado['xmls_baixados'])}")
            print("Números das notas:", resultado['xmls_baixados'])
