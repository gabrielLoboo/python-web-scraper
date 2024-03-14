from bs4 import BeautifulSoup

import json
import requests

# URL do site
url = 'https://infosimples.com/vagas/desafio/commercia/product.html'

# Objeto contendo a resposta final
categories = []
skus = []
properties = []
userreviews = []
resposta_final = { "categories": categories,
                    "skus": skus,
                    "properties": properties,
                    "reviews": userreviews
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

for item in strings_categories:
    categories.append(item.get_text())


# description
resposta_final['description'] = parsed_html.find('div', class_="proddet").get_text().strip()


# skus
cards_skus = parsed_html.find("div", class_="skus-area").find_all("div", class_="card-container")

for card in cards_skus:
    nome = card.find("div", class_="prod-nome").get_text().strip()
    current_price = card.find("div", class_="prod-pnow")
    old_price = card.find("div", class_="prod-pold")
    available = card.find("i")

    if current_price:
        current_price = float(current_price.get_text().strip().replace("R$", "").replace(",", "."))
    else:
        current_price = None

    if old_price:
        old_price = float(old_price.get_text().strip().replace("R$", "").replace(",", "."))
    else:
        old_price = None

    if available:
        available = False
    else:
        available = True

    skus.append({"name": nome, "current-price": current_price, "old-price": old_price, "available": available})


# properties
tb_properties = parsed_html.find("table", class_="pure-table pure-table-bordered").find_all("tr")

for item in tb_properties:

    label = item.find("b").get_text()
    value = item.find_all("td")

    if len(value) > 1:

        value_element = value[1].get_text()
        properties.append({"label": label, "value": value_element})


# reviews
comments_section = parsed_html.find("div", id="comments").find_all("div", class_="analisebox")

for item in comments_section:
    name = item.find("span", class_="analiseusername").get_text()
    date = item.find("span", class_="analisedate").get_text()
    text = item.find("p").get_text()
    score = item.find("span", class_="analisestars").get_text()
    stars_count = score.count("★")

    userreviews.append({"name": name, "date": date, "text": text, "score": stars_count})

# Gera string JSON com a resposta final
json_resposta_final = json.dumps(resposta_final, ensure_ascii=False)
# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_resposta_final)


