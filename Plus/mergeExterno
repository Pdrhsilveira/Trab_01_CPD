import os

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    left = merge_sort(left)
    right = merge_sort(right)
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    while i < len(left):
        result.append(left[i])
        i += 1
    
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result

def external_sort(input_files, output_file, block_size):
    temp_files = []
    
    for input_file in input_files:
        with open(input_file, 'r') as file:
            while True:
                block = file.read(block_size)
                if not block:
                    break
                
                block = block.split('\n')
                block = [int(x) for x in block if x]
                block = merge_sort(block)
                
                temp_file = f'temp_{len(temp_files)}.txt'
                temp_files.append(temp_file)
                
                with open(temp_file, 'w') as temp:
                    temp.write('\n'.join(str(x) for x in block))
    
    with open(output_file, 'w') as output:
        blocks = [open(temp_file, 'r') for temp_file in temp_files]
        current_values = [int(block.readline()) for block in blocks]
        
        while any(current_values):
            min_value = min(current_values)
            min_index = current_values.index(min_value)
            
            output.write(str(min_value) + '\n')
            
            line = blocks[min_index].readline().strip()
            if line:
                current_values[min_index] = int(line)
            else:
                current_values[min_index] = float('inf')
                blocks[min_index].close()
    
    for temp_file in temp_files:
        os.remove(temp_file)

# Exemplo de uso
input_files = ['aleatorios1.txt', 'aleatorios2.txt']
output_file = 'output.txt'

input_files = ['aleatorios1.txt', 'aleatorios2.txt']
block_size = 10000

external_sort(input_files, output_file, block_size)
block_size = 10000

external_sort(input_files, output_file, block_size)
