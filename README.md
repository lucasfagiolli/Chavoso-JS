# Chavoso JS
![image](https://github.com/lucasfagiolli/Drake/assets/85661349/facc2da7-e6f4-49a4-8c3d-49935fbc306d)



Este é um script simples em Python para procurar palavras-chave sensíveis em URLs JavaScript.

## Pré-requisitos

- Python 3.x
- Bibliotecas Python: `requests`

Você pode instalar as dependências executando:

```bash
pip install requests
```

Para criar uma lista de arquivos .js usando ferramentas como Gauplus e Subjs, você pode seguir as etapas abaixo:
``` bash
# Enumere arquivos .js conforme suas técnicas
cat sub.txt | gauplus | subjs | anew js
```
Filtre apenas os status codes 200:
``` bash
cat js | httpx -status-code -mc 200 | anew js200
```
Sua lista deve estar assim:
``` bash
https://exemplo.com/jquery/3.5.1/jquery.min.js
https://exemmplo.com/runtime.523794ee3f93b507.js
https://exemplo.com/runtime.0455abbda6964ac2.js
```

## Como usar
``` bash
python3 chavoso.py urls_js.txt [-o output.txt] [-silent]
```
## Argumentos

urls_js.txt: Caminho para o arquivo contendo as URLs JavaScript.

-o output.txt: Caminho opcional para o arquivo de saída.

-silent: Executar em modo silencioso, sem exibir o banner.

Lembre-se de personalizar a lista de palavras conforme necessário. Este script é fornecido "como está", sem garantias de qualquer tipo. Use-o com responsabilidade e sempre respeite as leis e regulamentações locais.


