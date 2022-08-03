import math
from random import randint
import numpy as np
from sympy import Matrix
import time


# encryption process by picking blocks
def encryption(a, s):
    while True:
        print("Enter path to a file: ")
        path = input()
        try:
            f = open(path, 'r', encoding='utf-8')
            open(f"{path[:-4]}_encrypted.txt", 'w').close()
            break
        except IOError:
            print("Please enter the correct path.")
    while True:
        output = ''
        text = f.read(len(a[0]))
        if text == '':
            print("File was successfully encrypted.")
            f.close()
            break
        text = translate(text)
        encrypted = encrypt(a, s, text)
        for i in encrypted:
            output += chr(i % 95 + 32)
        with open(f"{path[:-4]}_encrypted.txt", 'a', encoding='utf-8') as g:
            g.write(output)


# decryption process by picking blocks
def decryption(a, s):
    while True:
        print("Enter path to a file: ")
        path = input()
        try:
            f = open(path, 'r', encoding='utf-8')
            open(f"{path[:-4]}_decrypted.txt", 'w').close()
            break
        except IOError:
            print("Please enter the correct path.")
    while True:
        output = ''
        text = f.read(len(a[0]))
        if text == '':
            print("File was successfully decrypted.")
            f.close()
            break
        text = translate(text)
        decrypted = decrypt(a, s, text)
        for i in decrypted:
            output += chr(i % 95 + 32)
        with open(f"{path[:-4]}_decrypted.txt", 'a', encoding='utf-8') as g:
            g.write(output)


# renumerate a character in order we to use a scope that starts from 0 for modular division
def translate(text):
    res = []
    for i in text:
        res.append(ord(i) - 32)
    return np.array(res)


# check if the key is valid
def key_check(a, s):
    for i in s:
        if i < 0 or i > 94:
            return False
    for i in a:
        for j in i:
            if j < 0 or j > 94:
                return False
    ka = np.array(a)
    detka = np.linalg.det(ka)
    if math.gcd(int(detka), 95) == 1:
        return True
    else:
        return False


# create a key manually
def key_create():
    while True:
        print("X -> AX + S\n")
        while True:
            try:
                print("Enter A: ")
                temp = input()
                temp = temp.split()
                root = math.sqrt(len(temp))
                if int(root + 0.5)**2 != len(temp):
                    print("Please enter the correct number of elements.")
                else:
                    a = [[0 for _ in range(int(math.sqrt(len(temp))))] for _ in range(int(math.sqrt(len(temp))))]
                    for i in range(int(math.sqrt(len(temp)))):
                        for j in range(int(math.sqrt(len(temp)))):
                            a[i][j] = int(temp[i*int(math.sqrt(len(temp)))+j])
                    break
            except ValueError:
                print("Please enter a matrix of numbers.")
        print("Enter S: ")
        while True:
            try:
                temp = input().split(' ')
                if len(temp) != len(a[0]):
                    print("Please enter the correct number of elements.")
                else:
                    s = [int(i) for i in temp]
                    break
            except ValueError:
                print("Please enter a vector of numbers.")
        if key_check(a, s):
            return a, s
        print("Key is not correct.")


# generate a key automatically
def key_gen():
    print("Enter the length of the block.")
    while True:
        try:
            k = int(input())
            break
        except ValueError:
            print("Please enter a number.")
    while True:
        a = [[randint(0, 94) for _ in range(k)] for _ in range(k)]
        s = [randint(0, 94) for _ in range(k)]
        if key_check(a, s):
            break
    return a, s


# save the key in .txt extension
def key_save(a, s):
    output = ''
    for i in a:
        for j in i:
            output += f"{j} "
    output = output[:-1] + "\n"
    for i in s:
        output += f"{i} "
    output = output[:-1]
    try:
        print("Enter the name of the file:")
        path = input() + ".txt"
        with open(path, 'w') as f:
            f.write(output)
        print("Key was saved successfully.")
    except IOError:
        print("Please enter the correct file name.")


# import .txt key
def key_load():
    while True:
        print("Enter the name of the file: ")
        path = input()
        try:
            with open(path, 'r') as f:
                output = f.readlines()
            break
        except IOError:
            print("Please enter the correct file name.")
            continue
    first = output[0].split()
    second = output[1].split()
    a = [[0 for _ in range(int(math.sqrt(len(first))))] for _ in range(int(math.sqrt(len(first))))]
    for i in range(int(math.sqrt(len(first)))):
        for j in range(int(math.sqrt(len(first)))):
            a[i][j] = int(first[i*int(math.sqrt(len(first))) + j])
    s = [int(i) for i in second]
    if not key_check(a, s):
        print("The key is incorrect.")
        return
    print("The key was successfully loaded.")
    return a, s


# calculate inverse matrix which is a decryption key
def key_inverse(a):
    a_inv = Matrix(a)
    a_inv = a_inv.inv_mod(95)
    a_inv = a_inv.tolist()
    a_inv = np.array(a_inv)
    return a_inv


# encrypt a block
def encrypt(a, s, x):
    while len(x) != len(s):
        x += 0
    return np.add(np.array(s), np.dot(a, x))


# decrypt a block
def decrypt(a, s, x):
    return np.add(np.dot(key_inverse(a), x), np.dot(-1*key_inverse(a), s))


while True:
    print("1. Create key")
    print("2. Import key")
    print("3. Generate key")
    print("4. Exit")
    try:
        com = int(input())
        if com == 1:
            A, S = key_create()
            break
        if com == 2:
            A, S = key_load()
            break
        if com == 3:
            start_time = time.perf_counter()
            A, S = key_gen()
            print(f"Key was created for {time.perf_counter() - start_time}")
            break
        if com == 4:
            exit()
        else:
            print("Please enter a number from 1 to 4.")
    except ValueError:
        print("Please enter a number.")


print("Do you want to save a key?[y/n]")
while True:
    com = input()
    if com == 'y':
        key_save(A, S)
        break
    if com == 'n':
        break
    else:
        print("Please enter y or n.")

while True:
    print("1. Encryption")
    print("2. Decryption")
    print("3. Exit")
    try:
        com = int(input())
    except ValueError:
        print("Please enter a number.")
        continue
    if com == 1:
        start_time = time.perf_counter()
        encryption(A, S)
        print(f"Execution time: {time.perf_counter() - start_time}")
    if com == 2:
        start_time = time.perf_counter()
        decryption(A, S)
        print(f"Execution time: {time.perf_counter() - start_time}")
    if com == 3:
        exit()
    else:
        print("Please enter a number from 1 to 3.")
