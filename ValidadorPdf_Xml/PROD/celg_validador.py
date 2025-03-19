import os
import shutil
from pathlib import Path

def organizar_arquivos_por_nf(pasta_origem):
    # Criar um dicionário para agrupar os arquivos pelo número da NF
    arquivos_por_nf = {}
    
    # Listar todos os arquivos na pasta
    for arquivo in os.listdir(pasta_origem):
        # Encontrar o número da NF no nome do arquivo
        nf_numero = None
        
        if arquivo.startswith('NFe'):
            # Para arquivos XML e DANFE
            nf_numero = arquivo.split('-')[0].replace('NFe', '')
        elif arquivo.startswith('boleto-NFe'):
            # Para arquivos de boleto
            nf_numero = arquivo.replace('boleto-NFe', '').split('.')[0]
        
        if nf_numero:
            # Inicializar lista para esta NF se ainda não existir
            if nf_numero not in arquivos_por_nf:
                arquivos_por_nf[nf_numero] = []
            
            # Adicionar arquivo à lista desta NF
            arquivos_por_nf[nf_numero].append(arquivo)
    
    # Criar pastas e mover arquivos
    for nf_numero, arquivos in arquivos_por_nf.items():
        if len(arquivos) > 0:
            # Criar pasta para esta NF
            nova_pasta = os.path.join(pasta_origem, f'NF_{nf_numero}')
            Path(nova_pasta).mkdir(exist_ok=True)
            
            # Mover todos os arquivos relacionados para a nova pasta
            for arquivo in arquivos:
                origem = os.path.join(pasta_origem, arquivo)
                destino = os.path.join(nova_pasta, arquivo)
                shutil.move(origem, destino)
                print(f'Arquivo {arquivo} movido para {nova_pasta}')

if __name__ == "__main__":
    # Substitua pelo caminho da sua pasta
    pasta_origem = r"C:\Users\Bruno\Downloads\GLORIAN\RE\CELG_BACKUP"
    organizar_arquivos_por_nf(pasta_origem)
