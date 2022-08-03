from math import sqrt
from random import randint
import time


# build a grid to check if the key is valid
def grid_builder(l: int):
    if sqrt(l) % 2 != 0:
        print("Please enter perfect square number.")
        return None
    grid_list = [' ' for _ in range(l)]
    grid = ''
    for j in range(l):
        grid += grid_list[j]
    return grid


# a 90 degrees clockwise rotation
def turn(l, coord: int):
    x = coord // sqrt(l)
    y = coord % sqrt(l)
    a = y
    b = sqrt(l) - 1 - x
    return int(a*sqrt(l) + b)


# check if key is valid
def key_check(coord: int):
    global grid
    l = len(grid)
    temp = coord
    for _ in range(4):
        if grid[temp] == '*':
            return None
        temp = turn(l, temp)
    banned = []
    grid_temp = list(grid)
    for _ in range(4):
        grid_temp[temp] = '*'
        banned.append(temp)
        temp = turn(l, temp)
    print("Banned cells: ", banned)
    grid = "".join(grid_temp)
    return coord


# manual key generator
def key_gen(grid: str):
    key = []
    while len(key) < len(grid)/4:
        coordinate = choose(len(grid))
        temp = key_check(coordinate)
        if temp:
            key.append(temp)
        else:
            print("This cell is not available.")
    key.sort()
    return key


# automatic key generator
def auto_gen(grid: str):
    key = []
    start_time = time.perf_counter()
    while len(key) < len(grid) / 4:
        coordinate = randint(0, len(grid)-1)
        temp = key_check(coordinate)
        if temp is not None:
            key.append(temp)
    key.sort()
    print(f"Key was created for: {time.perf_counter() - start_time}")
    return key


# choose a cell from a grid
def choose(l):
    print(f'Choose a new cell from 0 to {l-1}:')
    coord = int(input())
    return coord


# encrypt a block
def encrypt(l, key, block: str):
    encrypted = []
    temp_key = []
    for i in range(len(key)):
        temp_key.append(key[i])
    res_list = ['' for _ in range(l)]
    res = ''
    temp_key_position = [0 for _ in range(l//4)]
    for i in range(l):
        temp_key_position[i % (l//4)] = temp_key[i % (l//4)]
        temp_key[i % (l//4)] = turn(l, temp_key[i % (l//4)])
        if (i + 1) % (l//4) == 0:
            temp_key_position.sort()
            for j in range(int(l/4)):
                encrypted.append(temp_key_position[j])
            temp_key_position = [0 for _ in range(l//4)]
    for i in range(l):
        try:
            res_list[encrypted[i]] = block[i]
        except IndexError:
            res_list[encrypted[i]] = ' '
    for i in range(l):
        res += res_list[i]
    return res


# encrypt text from a file by picking blocks
def encryption(input_file, key, lb):
    output_file = input_file.name[:-4] + '_encrypted.txt'
    file = open(output_file, 'w')
    while True:
        block = input_file.read(lb)
        if not block:
            break
        file.write(encrypt(lb, key, block))
    file.close()


# decrypt a block
def decrypt(l, key, block: str):
    decrypted = []
    res_list = ['' for _ in range(l)]
    res = ''
    temp_key = []
    for i in range(l//4):
        temp_key.append(key[i])
    temp_key_position = [0 for _ in range(l//4)]
    for i in range(l):
        temp_key_position[i % (l//4)] = temp_key[i % (l//4)]
        temp_key[i % (l//4)] = turn(l, temp_key[i % (l//4)])
        if (i + 1) % int(l/4) == 0:
            temp_key_position.sort()
            for j in range(int(l/4)):
                decrypted.append(temp_key_position[j])
            temp_key_position = [0 for _ in range(l//4)]
    for i in range(l):
        try:
            res_list[i] = block[decrypted[i]]
        except IndexError:
            break
    for i in range(l):
        res += res_list[i]
    return res


# decrypt text from a file by picking blocks
def decryption(input_file, key, lb):
    output_file = input_file.name[:-4] + '_decrypted.txt'
    file = open(output_file, 'w')
    while True:
        block = input_file.read(lb)
        if not block:
            break
        file.write(decrypt(lb, key, block))
    file.close()


while True:
    print("Enter path to the file to encrypt/decrypt(.txt): ")
    try:
        path = input()
        f = open(path)
        break
    except IOError:
        print("There is no such file/invalid extension.")
key = []
while True:
    print("1. Import key.")
    print("2. Create key.")
    print("3. Generate key(automatically).")
    print("4. Exit.")
    try:
        command = int(input())
        if command == 1:
            try:
                print("Enter a path to the key file:")
                key_path = input()
                key_file = open(key_path)
                try:
                    import_lb = int(key_file.readline())
                    import_key = key_file.readline()
                    numbers = import_key.split(' ')
                    if import_lb / (4*len(numbers)) != 1.:
                        raise ValueError
                    import_key = []
                    for i in range(len(numbers)):
                        import_key.append(int(numbers[i]))
                    lb = import_lb
                    key = import_key
                    break
                except ValueError:
                    print("Invalid type of file.")
            except IOError:
                print("There is no such file.")

        elif command == 2:
            print("Enter the length of block: ")
            lb = int(input())
            grid = grid_builder(lb)
            if grid:
                key = key_gen(grid)
                break

        elif command == 3:
            print("Enter the length of block: ")
            lb = int(input())
            grid = grid_builder(lb)
            if grid:
                key = auto_gen(grid)
                print(key)
                break

        elif command == 4:
            f.close()
            exit()
        else:
            print("Please enter a valid number.")
    except ValueError:
        print("Please enter a number.")

while True:
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    try:
        command = int(input())
        if command == 1:
            start_time = time.perf_counter()
            encryption(f, key, lb)
            print(f"Execution time: {time.perf_counter() - start_time}")
            print("A file with encrypted text was created.")
            f.close()
            break
        elif command == 2:
            start_time = time.perf_counter()
            decryption(f, key, lb)
            print(f"Execution time: {time.perf_counter() - start_time}")
            print("A file with decrypted text was created.")
            f.close()
            break
        elif command == 3:
            exit()
        else:
            print("Please enter a valid number.")
    except ValueError:
        print("Please enter a number.")
