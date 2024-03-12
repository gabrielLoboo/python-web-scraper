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
properties = []
resposta_final = { "categories": categories,
                    "skus": skus,
                    "properties": properties
                   }


# Faz o request
response = requests.get(url, verify=False)


# Parse do responses
parsed_html = BeautifulSoup(response.content, 'html.parser')


# product_title
resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()


# brand
resposta_final['brand'] = parsed_html.find('div', class_='brand').get_text()


# reviews_average_score
resposta_final['reviews_average_score'] = parsed_html.select_one('div#comments h4').get_text().strip()


# url
resposta_final['url'] = url


# categories
strings_categories = parsed_html.find('nav', class_="current-category").find_all('a')

for string_categories in strings_categories:
    categories.append(string_categories.get_text())


# description
resposta_final['description'] = parsed_html.find('div', class_="proddet").get_text().strip()


# skus
cards_skus = parsed_html.find("div", class_="skus-area").find_all("div", class_="card-container")

for card in cards_skus:
    nome_element = card.find("div", class_="prod-nome")
    current_price_element = card.find("div", class_="prod-pnow")
    old_price_element = card.find("div", class_="prod-pold")
    available_element = card.find("div", class_="i")

    if nome_element:
        nome = nome_element.get_text().strip()
    else:
        nome = "nome não encontrado"

    if current_price_element:
        current_price = float(current_price_element.get_text().strip().replace("R$", "").replace(",", "."))
    else:
        current_price = None

    if old_price_element:
        old_price = float(old_price_element.get_text().strip().replace("R$", "").replace(",", "."))
    else:
        old_price = None

    skus.append({"name": nome, "current-price": current_price, "old-price": old_price})


# properties
tb_properties = parsed_html.find("table", class_="pure-table pure-table-bordered").find_all("tr")

for item in tb_properties:

    label = item.find("b").get_text()
    value = item.find_all("td")

    if len(value) > 1:

        value_element = value[1].get_text()
        properties.append({"label": label, "value": value_element})


# Gera string JSON com a resposta final
json_resposta_final = json.dumps(resposta_final, ensure_ascii=False)
# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_resposta_final)


