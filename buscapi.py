import requests
import re
import sys
import urllib3
import argparse

# Desativar avisos relacionados à verificação de certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurar o parser de argumentos
parser = argparse.ArgumentParser(
    description="Script para procurar palavras-chave sensíveis em URLs.",
    epilog="Exemplo de uso: python script.py urls-js.txt -o resultado.txt -s"
)

parser.add_argument("-o", metavar="output.txt", type=str, help="Caminho para o arquivo de saída")
parser.add_argument("-s", "--silent", action="store_true", help="Executar em modo silencioso, sem exibir o banner")

# Analisar os argumentos da linha de comando
args, _ = parser.parse_known_args()

# Exibir banner, a menos que -silent esteja definido
if not args.silent:
    # Assinatura do autor
    print("\033[34m")
    print("""                               
                                                          
                  ____        ____        ____    
                /  _  |      / ___)      |  _ \   
                | |_| |  _   | |     _   | | | |   
                \__   | (_)  |_|    (_)  |_| |_|  🔑
                    |_|                                      
                                                            
                Autor: Q.R.N 💙 ♿
    """)
    print("\033[0m")

def search_keywords(url, keywords):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        result = response.text
    except requests.RequestException as e:
        print(f"\033[31mErro ao acessar {url}: {e}\033[0m")
        return

    matches = re.findall(keywords, result)

    if matches:
        print(f"\033[33m{keyword} ✅:\033[0m {url}")

if len(sys.argv) != 2:
    print("Uso: python script.py urls-js.txt")
    sys.exit(1)

file_path = sys.argv[1]

# Lista de palavras-chave na ordem desejada
keywords_order = ["access_key", "access_token", "api_key", "api_secret", "aws_access_key_id", "aws_secret_access_key", "password", "secret", "token", "Secret_Key"]

with open(file_path, 'r') as file:
    for line in file:
        for keyword in keywords_order:
            # Procurar pela palavra-chave na URL atual
            search_keywords(line.strip(), keyword)
