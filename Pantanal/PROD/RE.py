import requests
import os
from datetime import datetime
import time

def baixar_xml_pantanal():
    # Lista de empresas da RE com seus códigos ONS e nomes de pasta
    empresas = [
        ('4313', 'BRJA'),
        ('4314', 'BRJB'),
        ('3430', 'CECA'),
        ('3431', 'CECB'),
        ('3432', 'CECC'),
        ('4415', 'CECD'),
        ('4315', 'CECE'),
        ('4316', 'CECF'),
        ('3502', 'ITA1'),
        ('3497', 'ITA2'),
        ('3503', 'ITA3'),
        ('3530', 'ITA4'),
        ('3498', 'ITA5'),
        ('3531', 'ITA6'),
        ('3532', 'ITA7'),
        ('3537', 'ITA8'),
        ('3538', 'ITA9'),
        ('3947', 'SDBA'),
        ('3948', 'SDBB'),
        ('3969', 'SDBC'),
        ('3970', 'SDBD'),
        ('3976', 'SDBE'),
        ('3972', 'SDBF')
    ]
    
    # Base directory for downloads
    base_dir = r'C:\Users\Bruno\Downloads\TUST\PANTANAL\RE'
    
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
