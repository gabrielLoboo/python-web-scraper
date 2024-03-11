# Bibliotecas que nós instalamos manualmente
from bs4 import BeautifulSoup

# Bibliotecas nativas do Python
import json
import requests

# URL do site
url = 'https://infosimples.com/vagas/desafio/commercia/product.html'

# Objeto contendo a resposta final
categories = []
skus = []
resposta_final = { "categories": categories,
                   "skus": skus
                   }

# Faz o request
response = requests.get(url, verify=False)

# Parse do responses
parsed_html = BeautifulSoup(response.content, 'html.parser')

# product_title
resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()

# brand
resposta_final['brand'] = parsed_html.find('div', class_='brand').get_text()

# categories
strings_categories = parsed_html.find('nav', class_="current-category").find_all('a')

for string_categories in strings_categories:
    categories.append(string_categories.get_text())

# description
resposta_final['description'] = parsed_html.find('div', class_="proddet").get_text()

# skus


# Gera string JSON com a resposta final
json_resposta_final = json.dumps(resposta_final, ensure_ascii=False)
# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_resposta_final)
