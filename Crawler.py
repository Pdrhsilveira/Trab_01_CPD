import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página a ser raspada
url = "https://www.ontopsicologia.com.br/lancamentos"

# Cabeçalhos para simular um navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Fazendo a requisição para obter o conteúdo da página com os cabeçalhos
response = requests.get(url, headers=headers)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parsing do conteúdo da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar os elementos que contêm os nomes dos produtos
    product_elements = soup.find_all('a', class_='nome-produto cor-secundaria')
    product_names = [item.get_text(strip=True) for item in product_elements]

    # Encontrar os elementos que contêm os preços dos produtos
    price_elements = soup.find_all('strong', class_='preco-promocional cor-principal')
    product_prices = [price.get_text(strip=True).replace('\xa0', ' ').strip() for price in price_elements]

    # Criar listas para armazenar produtos e preços que têm correspondência
    valid_product_names = []
    valid_product_prices = []

    # Garantir que a quantidade de preços e nomes é a mesma
    min_length = min(len(product_names), len(product_prices))

    for i in range(min_length):
        # Filtrar produtos e preços inválidos
        if product_names[i] and product_prices[i] and not product_names[i].startswith('--PRODUTO_') and not product_prices[i].startswith('R$ --PRODUTO_'):
            valid_product_names.append(product_names[i])
            valid_product_prices.append(product_prices[i])

    # Criando um DataFrame para organizar os dados válidos
    df = pd.DataFrame({
        'Nome do Produto': valid_product_names,
        'Preço': valid_product_prices
    })

    # Exibindo o DataFrame
    print(df)

    # Salvando os dados em um arquivo CSV
    df.to_csv('produtos_ontopsicologia.csv', index=False)
else:
    print(f"Erro ao acessar a página: {response.status_code}")
