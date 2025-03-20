import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pdf_to_txt import converter_pdf_para_txt, converter_pdf_para_docx

class PDFHandler(FileSystemEventHandler):
    def __init__(self, pasta_saida, formato_saida='txt', usar_ocr=False):
        self.pasta_saida = pasta_saida
        self.formato_saida = formato_saida
        self.usar_ocr = usar_ocr

    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.src_path.lower().endswith('.pdf'):
            print(f'\nNovo arquivo PDF detectado: {event.src_path}')
            # Aguarda um momento para garantir que o arquivo foi completamente copiado
            time.sleep(1)
            self.processar_pdf(event.src_path)

    def processar_pdf(self, caminho_pdf):
        """Processa um arquivo PDF"""
        nome_arquivo = os.path.basename(caminho_pdf)
        caminho_saida = os.path.join(self.pasta_saida, os.path.splitext(nome_arquivo)[0] + '.' + self.formato_saida)
        
        if self.formato_saida == 'txt':
            converter_pdf_para_txt(caminho_pdf, caminho_saida, self.usar_ocr)
        else:  # docx
            converter_pdf_para_docx(caminho_pdf, caminho_saida, self.usar_ocr)

def processar_pdfs_existentes(pasta_entrada, pasta_saida, formato_saida, usar_ocr):
    """Processa todos os PDFs existentes na pasta de entrada"""
    print('\nProcessando PDFs existentes...')
    for arquivo in os.listdir(pasta_entrada):
        if arquivo.lower().endswith('.pdf'):
            caminho_pdf = os.path.join(pasta_entrada, arquivo)
            print(f'\nProcessando: {arquivo}')
            handler = PDFHandler(pasta_saida, formato_saida, usar_ocr)
            handler.processar_pdf(caminho_pdf)

def monitorar_pasta(pasta_entrada, pasta_saida, formato_saida='txt', usar_ocr=False):
    """
    Monitora uma pasta para converter PDFs automaticamente
    :param pasta_entrada: Pasta onde os PDFs serão colocados
    :param pasta_saida: Pasta onde os arquivos convertidos serão salvos
    :param formato_saida: Formato de saída ('txt' ou 'docx')
    :param usar_ocr: Se True, usa OCR para extrair texto de imagens
    """
    # Cria as pastas se não existirem
    os.makedirs(pasta_entrada, exist_ok=True)
    os.makedirs(pasta_saida, exist_ok=True)

    print(f'=== Monitor de PDF ===')
    print(f'Pasta de entrada: {pasta_entrada}')
    print(f'Pasta de saída: {pasta_saida}')
    print(f'Formato de saída: {formato_saida.upper()}')
    print(f'OCR: {"Ativado" if usar_ocr else "Desativado"}')
    print('\nColoque seus arquivos PDF na pasta de entrada.')
    print(f'Os arquivos {formato_saida.upper()} serão gerados automaticamente na pasta de saída.')
    print('Pressione Ctrl+C para encerrar o programa.\n')

    # Processa PDFs existentes
    processar_pdfs_existentes(pasta_entrada, pasta_saida, formato_saida, usar_ocr)

    # Configura o observador
    event_handler = PDFHandler(pasta_saida, formato_saida, usar_ocr)
    observer = Observer()
    observer.schedule(event_handler, pasta_entrada, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print('\nPrograma encerrado.')
    
    observer.join()

if __name__ == '__main__':
    # Define as pastas padrão
    pasta_entrada = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs_para_converter')
    pasta_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arquivos_convertidos')
    
    print('=== Monitor de PDF ===')
    print('1. Converter para TXT')
    print('2. Converter para DOCX')
    opcao = input('Escolha o formato de saída (1 ou 2): ').strip()
    
    if opcao == '1':
        formato_saida = 'txt'
    elif opcao == '2':
        formato_saida = 'docx'
    else:
        print('Opção inválida!')
        exit(1)
    
    # Pergunta se deseja usar OCR
    usar_ocr = input('Deseja usar OCR para extrair texto de imagens? (s/n): ').strip().lower() == 's'
    
    monitorar_pasta(pasta_entrada, pasta_saida, formato_saida, usar_ocr) 