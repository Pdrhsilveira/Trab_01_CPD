import os
import heapq
import tempfile
import random

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
                
                temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
                temp_files.append(temp_file.name)
                
                with open(temp_file.name, 'w') as temp:
                    temp.write('\n'.join(str(x) for x in block))
    
    with open(output_file, 'w') as output:
        min_heap = []
        file_pointers = [open(temp_file, 'r') for temp_file in temp_files]
        
        for i, fp in enumerate(file_pointers):
            line = fp.readline().strip()
            if line:
                heapq.heappush(min_heap, (int(line), i))
        
        while min_heap:
            min_value, min_index = heapq.heappop(min_heap)
            output.write(str(min_value) + '\n')
            
            line = file_pointers[min_index].readline().strip()
            if line:
                heapq.heappush(min_heap, (int(line), min_index))
            else:
                file_pointers[min_index].close()
    
    for temp_file in temp_files:
        os.remove(temp_file)

def create_random_file(filename, num_numbers):
    with open(filename, 'w') as file:
        for _ in range(num_numbers):
            file.write(f"{random.randint(1, 1000)}\n")

def split_file(input_file, num_parts):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    part_size = len(lines) // num_parts
    for i in range(num_parts):
        part_filename = f"{input_file.split('.')[0]}_part{i+1}.txt"
        with open(part_filename, 'w') as part_file:
            part_file.writelines(lines[i * part_size:(i + 1) * part_size])


create_random_file('Numeros_Aleatorios.txt', 1000)


split_file('Numeros_Aleatorios.txt', 5)


input_files = ['Numeros_Aleatorios_part1.txt', 'Numeros_Aleatorios_part2.txt', 'Numeros_Aleatorios_part3.txt', 'Numeros_Aleatorios_part4.txt', 'Numeros_Aleatorios_part5.txt']
output_file = 'arquivo_final.txt'

for i, input_file in enumerate(input_files):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        lines = [int(line.strip()) for line in lines]
        sorted_lines = merge_sort(lines)
        
        with open(f"Ordenados_part{i+1}.txt", 'w') as sorted_file:
            sorted_file.write('\n'.join(str(line) for line in sorted_lines))
block_size = 10000


external_sort(input_files, output_file, block_size)
print('Finalizado, verifique o processo nos arquivos txt!')
