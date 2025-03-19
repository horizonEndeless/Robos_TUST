import os
import shutil
from pathlib import Path

def organize_ons_files(source_dir):
    # Criar o diretório base onde as pastas serão organizadas
    base_dir = Path(source_dir)
    
    # Verificar se o diretório existe
    if not base_dir.exists():
        print(f"O diretório {source_dir} não existe!")
        return
    
    # Listar todos os arquivos PDF
    pdf_files = list(base_dir.glob("*.pdf"))
    
    # Para cada arquivo PDF
    for pdf_file in pdf_files:
        # Extrair o nome da empresa do arquivo
        file_name = pdf_file.name
        
        # Identificar o nome da empresa
        if "EOLICA" in file_name.upper():
            # Extrair o nome específico da eólica
            parts = file_name.split('_')[0].split()
            company_name = ' '.join(parts[1:])  # Pegar tudo depois de "EOLICA"
        else:
            company_name = "OUTROS"
        
        # Criar diretório para a empresa se não existir
        company_dir = base_dir / company_name
        company_dir.mkdir(exist_ok=True)
        
        # Definir o caminho de destino
        destination = company_dir / pdf_file.name
        
        try:
            # Mover o arquivo
            shutil.move(str(pdf_file), str(destination))
            print(f"Arquivo {pdf_file.name} movido para {company_name}/")
        except Exception as e:
            print(f"Erro ao mover {pdf_file.name}: {str(e)}")

if __name__ == "__main__":
    # Caminho para a pasta com os arquivos
    source_directory = r"C:\Users\Bruno\Downloads\faturas-ONS"
    
    # Executar a organização
    organize_ons_files(source_directory)