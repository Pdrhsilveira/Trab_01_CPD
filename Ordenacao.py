from Crawler import produtos

def insertion_sort_produtos(produtos):
    for i in range(1, len(produtos)):
        atual = produtos[i] 
        j = i - 1
        
        while j >= 0 and float(produtos[j]['preco'].replace('R$', '').replace(',', '.')) > float(atual['preco'].replace('R$', '').replace(',', '.')):
            produtos[j + 1] = produtos[j] 
            j -= 1
        
        produtos[j + 1] = atual  
    
    return produtos

produtos_ordenados = insertion_sort_produtos(produtos)

for produto in produtos_ordenados:
    print(produto['nome'], '-', produto['preco'])
