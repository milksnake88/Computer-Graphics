import numpy as np

#A
M = np.arange(5,21,1)
print(M,end = "\n\n")

#B
M = M.reshape(4,4)
print(M,end = "\n\n")

#C
M[1:3,1:3] = 0
print(M,end = "\n\n")

#D
M = M@M
print(M,end = "\n\n")

#E
v = M[0,:]
v_square = np.square(v)
v_squareSum = v_square[0]+v_square[1]+v_square[2]+v_square[3]
v_magnitude = np.sqrt(v_squareSum)
print(v_magnitude)
