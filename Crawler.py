import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista com as URLs das páginas a serem raspadas
urls = [
    "https://www.ontopsicologia.com.br/livros?pagina=1",
    "https://www.ontopsicologia.com.br/livros?pagina=2",
    "https://www.ontopsicologia.com.br/livros?pagina=3"
]

# Cabeçalhos para simular um navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Listas para armazenar todos os nomes e preços dos produtos
all_product_names = []
all_product_prices = []

# Função para extrair informações de uma página
def extract_product_info(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraindo nomes dos produtos
        product_elements = soup.find_all('a', class_='nome-produto cor-secundaria')
        product_names = [item.get_text(strip=True) for item in product_elements]
        
        # Extraindo preços dos produtos
        price_elements = soup.find_all('strong', class_='preco-promocional cor-principal')
        product_prices = [price.get_text(strip=True).replace('\xa0', ' ').strip() for price in price_elements]
        
        # Garantindo que a quantidade de preços e nomes é a mesma
        min_length = min(len(product_names), len(product_prices))
        for i in range(min_length):
            name, price = product_names[i], product_prices[i]
            # Verificando se o nome e o preço são válidos
            if name and price and not name.startswith('--PRODUTO_NOME--') and not price.startswith('R$ --PRODUTO_PRECO_POR--'):
                all_product_names.append(name)
                all_product_prices.append(price)

# Iterar sobre todas as URLs e extrair informações de cada uma
for url in urls:
    extract_product_info(url)

# Criando um DataFrame para organizar todos os dados coletados
df = pd.DataFrame({
    'Nome do Produto': all_product_names,
    'Preço': all_product_prices
})

# Exibindo o DataFrame final
print(df)

# Salvando os dados em um arquivo CSV
df.to_csv('todos_produtos_filtrados.csv', index=False)

    # Salvando os dados em um arquivo CSV
    df.to_csv('produtos_ontopsicologia.csv', index=False)
else:
    print(f"Erro ao acessar a página: {response.status_code}")
