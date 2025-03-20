import os
import shutil
import subprocess
import sys

def build_executable():
    print("Iniciando processo de build...")
    
    # Limpa diretórios de build anteriores
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Instala dependências
    print("Instalando dependências...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Compila o executável
    print("Compilando executável...")
    subprocess.run([
        "pyinstaller",
        "--name=conversor_pdf",
        "--windowed",
        "--onefile",
        "--add-data=resources;resources",
        "--icon=resources/icon.ico",
        "src/main.py"
    ])
    
    print("Build concluído!")
    print("O executável está em: dist/conversor_pdf.exe")

if __name__ == "__main__":
    build_executable() 