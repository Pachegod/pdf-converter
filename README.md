# Conversor de PDF

Este é um sistema para converter arquivos PDF em arquivos de texto (TXT) ou documentos Word (DOCX). O sistema oferece uma interface gráfica moderna e intuitiva para facilitar a conversão de arquivos.

## Características

- Interface gráfica moderna e intuitiva
- Suporte a temas claro e escuro
- Arraste e solte de arquivos
- Conversão em lote de múltiplos arquivos
- Suporte a OCR para extrair texto de imagens
- Conversão para TXT e DOCX
- Barra de progresso
- Tratamento de erros
- Instalador completo

## Requisitos do Sistema

- Windows 10 ou superior
- Python 3.6 ou superior (apenas para desenvolvimento)
- Tesseract OCR
- Poppler

## Instalação

### Para Usuários Finais

1. Baixe o instalador `ConversorPDF_Setup.exe` da última versão
2. Execute o instalador
3. Siga as instruções do assistente de instalação
4. O programa será instalado com todas as dependências necessárias

### Para Desenvolvedores

1. Clone ou baixe este repositório:
```bash
git clone https://github.com/seu-usuario/pdf-converter.git
cd pdf-converter
```

2. Instale o Tesseract OCR:
   - Windows: 
     1. Baixe e instale de https://github.com/UB-Mannheim/tesseract/wiki
     2. Durante a instalação, marque a opção "Add to system PATH"
     3. Baixe o arquivo `por.traineddata` de https://github.com/tesseract-ocr/tessdata
     4. Copie o arquivo para `C:\Program Files\Tesseract-OCR\tessdata`

3. Instale o Poppler:
   - Windows:
     1. Baixe de https://github.com/oschwartz10612/poppler-windows/releases/
     2. Extraia o arquivo ZIP
     3. Copie a pasta para `C:\Program Files\poppler`
     4. Adicione `C:\Program Files\poppler\Library\bin` ao PATH do sistema

4. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

5. Para compilar o executável:
```bash
python build.py
```

6. Para criar o instalador:
   - Instale o Inno Setup de https://jrsoftware.org/isdl.php
   - Abra o arquivo `installer/installer.iss`
   - Clique em "Build > Compile"

## Como Usar

1. Inicie o programa pelo menu Iniciar ou pelo ícone na área de trabalho
2. Arraste e solte seus arquivos PDF na área principal ou clique para selecionar
3. Escolha o formato de saída (TXT ou DOCX)
4. Marque a opção "Usar OCR" se necessário
5. Clique em "Converter"
6. Aguarde a conclusão da conversão
7. Os arquivos convertidos serão salvos na pasta "arquivos_convertidos"

## Funcionalidades

- Converte PDFs para TXT ou DOCX
- Mantém a formatação básica do texto
- Suporta caracteres especiais (UTF-8)
- Tratamento de erros para arquivos corrompidos ou inválidos
- Interface gráfica moderna e intuitiva
- Suporte a temas claro e escuro
- Arraste e solte de arquivos
- Conversão em lote de múltiplos arquivos
- Suporte a OCR para extrair texto de PDFs com imagens
- Detecção automática de PDFs que precisam de OCR
- Suporte ao idioma português
- Formatação automática em DOCX (fonte Arial, tamanho 11)

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para:
1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 