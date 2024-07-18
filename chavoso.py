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

parser.add_argument("inputs", nargs="+", help="URLs ou palavras-chave diretamente na linha de comando ou caminho para arquivo de texto")
parser.add_argument("-o", metavar="output.txt", type=str, help="Caminho para o arquivo de saída")
parser.add_argument("-silent", action="store_true", help="Executar em modo silencioso, sem exibir o banner")

# Analisar os argumentos da linha de comando
args = parser.parse_args()

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
        "ADMINBAR_ACCESS_TOKEN": [],
        "AWS_SECRET_ACCESS_KEY": [],
        "AWS_ACCESS_KEY_ID": [],
        "Secret_Key": [],
    }

    for match in set(matches):
        for keyword in grouped_matches:
            if keyword in match.lower():
                grouped_matches[keyword].append(f"\033[34m{keyword} ✅:\033[0m {url}")
                break

    return grouped_matches

# Se foram fornecidas URLs diretamente na linha de comando ou via arquivo, use-as; caso contrário, leia a partir do arquivo padrão
inputs = args.inputs if args.inputs else sys.stdin.read().splitlines()

all_results = {}

for input_data in inputs:
    if input_data.startswith("http://") or input_data.startswith("https://"):
        # Se a entrada é uma URL, use-a diretamente
        results = search_keywords(input_data)
    else:
        # Caso contrário, assume-se que é um caminho para um arquivo de texto e lê as entradas do arquivo
        try:
            with open(input_data, 'r') as file:
                for line in file:
                    results = search_keywords(line.strip())
                    for keyword in results:
                        all_results.setdefault(keyword, []).extend(results[keyword])
        except FileNotFoundError:
            print(f"\033[31mArquivo não encontrado: {input_data}\033[0m")
            sys.exit(1)

# Imprimir os resultados em ordem
for keyword in all_results:
    for result in all_results[keyword]:
        print(result)

# Se foi especificado um arquivo de saída, gravar os resultados nele
if args.o:
    with open(args.o, 'w') as output_file:
        for keyword in all_results:
            for result in all_results[keyword]:
                output_file.write(result + "\n")
