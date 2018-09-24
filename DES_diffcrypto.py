import numpy as np

box0 = np.array([
[1,0,3,2],
[3,2,1,0],
[0,2,1,3],
[3,1,3,2]
])


key = [1,0,1,0]
xor_val = [0,0,1,0]

def int_to_arr(i):
    return np.array([i/8, i%8 /4, i % 4 / 2, i % 2])

def arr_to_4int(i):
    return i[0]*8 + i[1] * 4 + i[2] * 2 + i[3]

def arr_to_2int(i):
    return i[0]*2 + i[1]

def s_box(input_bits, box):
    col = 2 * input_bits[1] + input_bits[2]
    row = 2* input_bits[0] + input_bits[3]
    return np.array([box[row,col] //2, box[row,col]%2])


#The simplified F function we're going to use to attempt differential cryptography against box S0
def f(input_bits, key):
    xor = input_bits ^ key
    # a ^ key, b ^ key
    # (a ^ key) ^ (b ^ key) = a ^ key ^ key ^ b = a ^ b = 2
    # a', b'
    # a' ^ b' = 2
    # (a',b') is one of the pairs we've already generated
    s0 = s_box(xor,box0) 
    return s0



for i in range(16):
    i_arr = int_to_arr(i)
    i_xor_arr = i_arr ^ xor_val

    sbox_1 = s_box(i_arr,box0)
    sbox_2 = s_box(i_xor_arr,box0)

    #f_1 = f(i_arr,key)
    #f_2 = f(i_xor_arr,key)
    #f_xor = f_1 ^ f_2
    print("A:{} B:{}  Out:{}".format(i, arr_to_4int(i_xor_arr), arr_to_2int(sbox_1 ^ sbox_2)))
#Numbers such that a ^ b = 2
#a ^ 2 = b
#iterate through the numbers, add (a, a^2)

# A:0 B:2  Out:1
# A:1 B:3  Out:1
# A:2 B:0  Out:1
# A:3 B:1  Out:1
# A:4 B:6  Out:1
# A:5 B:7  Out:1
# A:6 B:4  Out:1
# A:7 B:5  Out:1
# A:8 B:10  Out:2
# A:9 B:11  Out:2
# A:10 B:8  Out:2
# A:11 B:9  Out:2
# A:12 B:14  Out:2
# A:13 B:15  Out:1
# A:14 B:12  Out:2
# A:15 B:13  Out:1

#Distribution Table:
# 2 -> 1: 0,1,2,3,4,5,6,7,13,15 
# 2 -> 2: 8,9,10,11,12,14



f_1 = f(int_to_arr(1),key)
f_2 = f(int_to_arr(3),key)
f_xor = f_1 ^ f_2
print(arr_to_2int(f_xor))
#choosing a specific pair: 1, 3   (because 1 xor 3 = 2)
#Result is 2, meaning possible post-xor pairs are everything in the distribution table corresponding to 2
# since 1 ^ key = something in the dist table, 1 ^ something in the dist table = key
#possible keys now include:
#8 ^ 1 = 9
#9 ^ 1 = 8
#10 ^ 1 = 11
#11 ^ 1 = 10
#12 ^ 1 = 13
#14 ^ 1 = 12
#Possible Key set: (9,8,11,10,13,12)


f_1 = f(int_to_arr(4),key)
f_2 = f(int_to_arr(6),key)
f_xor = f_1 ^ f_2
print(arr_to_2int(f_xor))
#Second pair: 4,6, result 2

#8 ^ 4 = 12
#9 ^ 4 = 13
#10 ^ 4 = 14
#11 ^ 4 = 15
#12 ^ 4 = 8
#14 ^ 4 = 10
#repeating the same process, narrowing the key set down even further.
#Second possible key set: (12,13,14,15,8,10)
#Intersection: (8, 10, 12, 13)



f_1 = f(int_to_arr(0),key)
f_2 = f(int_to_arr(2),key)
f_xor = f_1 ^ f_2
print(arr_to_2int(f_xor))
#Third pair: 0,2, Result 2
#8 ^ 0 = 8
#9 ^ 0 = 9
#10 ^ 0  = 10
#11 ^ 0 = 11
#12 ^ 0 = 12
#14 ^ 0 = 14
#Intersection = (8,10,12)
#Continue this process until you get enough results to sufficiently narrow down the set, providing the answer: key = 10