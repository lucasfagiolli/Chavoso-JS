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
    epilog="Exemplo de uso: python script.py urls-js.txt -o resultado.txt -silent"
)

parser.add_argument("file_path", metavar="arquivo_urls.txt", type=str, help="Caminho para o arquivo contendo as URLs")
parser.add_argument("-o", dest="output_file", metavar="output.txt", type=str, help="Caminho para o arquivo de saída")
parser.add_argument("-silent", dest="silent", action="store_true", help="Executar em modo silencioso, sem exibir o banner")

# Analisar os argumentos da linha de comando
args = parser.parse_args()

# Exibir banner, a menos que -silent esteja definido
if not args.silent:
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

def search_keywords(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        result = response.text
    except requests.RequestException as e:
        print(f"\033[31mErro ao acessar {url}: {e}\033[0m")
        return

    matches = re.findall(r'access_key|access_token|api_key|api_secret|aws_access_key_id|aws_secret_access_key|password|secret|token|Secret_Key', result)

    grouped_matches = {
        "access_key": [],
        "access_token": [],
        "api_key": [],
        "api_secret": [],
        "aws_access_key_id": [],
        "aws_secret_access_key": [],
        "password": [],
        "secret": [],
        "token": [],
        "Secret_Key": [],
    }

    for match in set(matches):
        for keyword in grouped_matches:
            if keyword in match.lower():
                grouped_matches[keyword].append(f"\033[34m{keyword} ✅:\033[0m {url}")
                break

    return grouped_matches

# ...

file_path = args.file_path

all_results = {}

with open(file_path, 'r') as file:
    for line in file:
        results = search_keywords(line.strip())
        for keyword in results:
            all_results.setdefault(keyword, []).extend(results[keyword])

# Imprimir os resultados em ordem
for keyword in all_results:
    for result in all_results[keyword]:
        print(result)

# Salvar os resultados em um arquivo, se a opção -o estiver definida
if args.output_file:
    with open(args.output_file, 'w') as output_file:
        for keyword in all_results:
            for result in all_results[keyword]:
                output_file.write(result + "\n")
