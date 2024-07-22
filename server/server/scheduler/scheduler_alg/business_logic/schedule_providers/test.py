import numpy as np

matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

res = [[0,0,0]]

arr = [1,2,3]

for i in range(0,3):
    res = np.append(res, [matrix[i]], axis=0)
    arr = np.append(arr, [matrix[i][0]], axis=0)


d = {(0,0):[1,2,3], (1,1):[4,5,6]}
dk = np.array(list(d.keys()))

for i, di in d.items():
    dk = np.append(dk, [i],axis=0)

print(res)
print(np.append(arr,arr,axis=0))

print(dk)