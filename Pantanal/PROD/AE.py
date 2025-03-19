import requests
import os
from datetime import datetime
import time

def baixar_xml_pantanal():
    # Lista de empresas da RE com seus códigos ONS e nomes de pasta
    empresas = [
        ('3859', 'SJP1'),
        ('3860', 'SJP2'),
        ('3861', 'SJP3'),
        ('3862', 'SJP4'),
        ('3863', 'SJP5'),
        ('3864', 'SJP6'),
        ('3740', 'COR1'),
        ('3741', 'COR2'),
        ('3750', 'COR3'),
        ('8011', 'LIBRA')
    ]
    
    # Base directory for downloads
    base_dir = r'C:\Users\Bruno\Downloads\PANTANAL\AE'
    
    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/xml,text/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.pantanaltransmissao.com.br/pantanal.html'
    }

    for codigo_ons, pasta in empresas:
        try:
            # Criar pasta específica para cada empresa
            download_dir = os.path.join(base_dir, pasta)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            print(f"\nBaixando arquivo para {pasta} (Código ONS: {codigo_ons})...")
            
            # URL e parâmetros
            url = "https://www.pantanaltransmissao.com.br/download.php"
            params = {
                'tswcode': codigo_ons,
                'file': f'{codigo_ons}.xml'
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                # Nome do arquivo com timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'pantanal_{pasta}_{timestamp}.xml'
                filepath = os.path.join(download_dir, filename)
                
                # Salvar o arquivo
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ Arquivo baixado com sucesso: {filepath}")
            else:
                print(f"✗ Erro ao baixar arquivo para {pasta}. Status code: {response.status_code}")
                print(f"Resposta do servidor: {response.text}")
                
        except Exception as e:
            print(f"✗ Erro ao processar {pasta}: {e}")
        
        # Pequena pausa entre downloads para não sobrecarregar o servidor
        time.sleep(1)

if __name__ == "__main__":
    print("Iniciando o processo de download dos XMLs...")
    print("=" * 50)
    baixar_xml_pantanal()
    print("\nProcesso finalizado!")
