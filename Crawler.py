import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.ontopsicologia.com.br/livros?pagina=1",
    "https://www.ontopsicologia.com.br/livros?pagina=2",
    "https://www.ontopsicologia.com.br/livros?pagina=3"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

produtos = []

def extract_product_info(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_elements = soup.find_all('a', class_='nome-produto cor-secundaria')
        product_names = [item.get_text(strip=True) for item in product_elements]
        
        price_elements = soup.find_all('strong', class_='preco-promocional cor-principal')
        product_prices = [price.get_text(strip=True).replace('\xa0', ' ').strip() for price in price_elements]
        
        min_length = min(len(product_names), len(product_prices))
        for i in range(min_length):
            name, price = product_names[i], product_prices[i]

            if name and price and not name.startswith('--PRODUTO_NOME--') and not price.startswith('R$ --PRODUTO_PRECO_POR--'):
                produtos.append({'nome': name, 'preco': price})

for url in urls:
    extract_product_info(url)

for produto in produtos:
    print(produto)

with open('livros_ontopsicologia.csv', 'w') as file:
    file.write('Nome do Produto,Preço\n')
    for produto in produtos:
        file.write(f"{produto['nome']},{produto['preco']}\n")
