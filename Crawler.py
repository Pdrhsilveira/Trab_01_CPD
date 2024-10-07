import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.ontopsicologia.com.br/livros?pagina=1",
    "https://www.ontopsicologia.com.br/livros?pagina=2",
    "https://www.ontopsicologia.com.br/livros?pagina=3"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"  # spell-checker: disable
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


valid_produtos = []
for produto in produtos:  
    try:
        produto['preco'] = float(produto['preco'].replace('R$', '').replace(',', '.'))  
        valid_produtos.append(produto)
    except ValueError:
        continue

for i in range(1, len(valid_produtos)):  
    key = valid_produtos[i]  
    j = i - 1
    while j >= 0 and key['preco'] < valid_produtos[j]['preco']:  
        valid_produtos[j + 1] = valid_produtos[j]  
        j -= 1
    valid_produtos[j + 1] = key  


for produto in valid_produtos:  
    produto['preco'] = f"R$ {produto['preco']:.2f}".replace('.', ',')  

for produto in valid_produtos:  
    print(produto)  

with open('livros_ontopsicologia.csv', 'w') as file:  
    file.write('Nome do Produto,preco\n')  
    for produto in valid_produtos: 
        file.write(f"{produto['nome']},{produto['preco']}\n")  
