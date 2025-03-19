import os
import shutil

def consolidar_arquivos(pasta_origem):
    """Consolida arquivos XML e PDF com mesmo nome em pastas específicas"""
    print("Iniciando consolidação de arquivos...")
    
    # Lista todos os arquivos
    arquivos = os.listdir(pasta_origem)
    
    # Separa XMLs e PDFs
    xmls = [f for f in arquivos if f.endswith('.xml')]
    pdfs = [f for f in arquivos if f.endswith('.pdf')]
    
    # Remove as extensões para comparação
    empresas_xml = [os.path.splitext(f)[0] for f in xmls]
    empresas_pdf = [os.path.splitext(f)[0] for f in pdfs]
    
    # Encontra empresas que têm ambos os arquivos
    empresas_completas = set(empresas_xml) & set(empresas_pdf)
    
    print(f"\nEncontrados:")
    print(f"- {len(xmls)} arquivos XML")
    print(f"- {len(pdfs)} arquivos PDF")
    print(f"- {len(empresas_completas)} empresas com ambos os documentos")
    
    # Cria pastas e move arquivos
    for empresa in empresas_completas:
        print(f"\nProcessando empresa: {empresa}")
        
        # Cria pasta da empresa
        pasta_empresa = os.path.join(pasta_origem, empresa)
        if not os.path.exists(pasta_empresa):
            os.makedirs(pasta_empresa)
            print(f"Pasta criada: {pasta_empresa}")
        
        # Move XML
        xml_origem = os.path.join(pasta_origem, f"{empresa}.xml")
        xml_destino = os.path.join(pasta_empresa, f"{empresa}.xml")
        try:
            shutil.move(xml_origem, xml_destino)
            print(f"XML movido com sucesso")
        except Exception as e:
            print(f"Erro ao mover XML: {str(e)}")
        
        # Move PDF
        pdf_origem = os.path.join(pasta_origem, f"{empresa}.pdf")
        pdf_destino = os.path.join(pasta_empresa, f"{empresa}.pdf")
        try:
            shutil.move(pdf_origem, pdf_destino)
            print(f"PDF movido com sucesso")
        except Exception as e:
            print(f"Erro ao mover PDF: {str(e)}")
    
    print("\nProcesso de consolidação concluído!")
    
    # Lista arquivos que ficaram sem par
    xmls_restantes = set(empresas_xml) - empresas_completas
    pdfs_restantes = set(empresas_pdf) - empresas_completas
    
    if xmls_restantes:
        print("\nXMLs sem PDF correspondente:")
        for xml in xmls_restantes:
            print(f"- {xml}")
    
    if pdfs_restantes:
        print("\nPDFs sem XML correspondente:")
        for pdf in pdfs_restantes:
            print(f"- {pdf}")

def main():
    print("Iniciando programa de consolidação de arquivos")
    pasta_origem = input("Digite o caminho da pasta com os arquivos XML e PDF: ")
    
    if not os.path.exists(pasta_origem):
        print("Erro: Pasta não encontrada!")
        return
    
    consolidar_arquivos(pasta_origem)

if __name__ == "__main__":
    main()
