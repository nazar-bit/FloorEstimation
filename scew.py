import cv2
import numpy as np

#Real life Width(metres), Height(metres), metre/px ratio
W = 24.912
H = 29.804
s = 13.5

#In image facade coordinates
u1, v1 = 218, 421
u2, v2 = 641, 505
u3, v3 = 599, 853
u4, v4 = 181, 760

#Exprected facade corner coordinates
u1_, v1_ = 0, 0
u2_, v2_ = W*s, 0
u3_, v3_ = W*s, H*s 
u4_, v4_ = 0, H*s

#Calculation of skewing matrix
A = np.array(
    [
        [u1, v1, 1, 0, 0, 0, -u1*u1_, -v1*u1_],
        [0, 0, 0, u1, v1, 1, -u1*v1_, -v1*v1_],
        [u2, v2, 1, 0, 0, 0, -u2*u2_, -v2*u2_],
        [0, 0, 0, u2, v2, 1, -u2*v2_, -v2*v2_],
        [u3, v3, 1, 0, 0, 0, -u3*u3_, -v3*u3_],
        [0, 0, 0, u3, v3, 1, -u3*v3_, -v3*v3_],
        [u4, v4, 1, 0, 0, 0, -u4*u4_, -v4*u4_],
        [0, 0, 0, u4, v4, 1, -u4*v4_, -v4*v4_]
    ]
)

d = np.array(
    [u1_, v1_, u2_, v2_, u3_, v3_, u4_, v4_]
)

h = np.linalg.solve(A, d)
h = np.append(h, [1])
print(h)



#Application of skewing matrix
img = cv2.imread(r"D:\FloorEstimation\sikme_snimky\SLS\uzemi01\skupina01\test2.jpg")
rows, cols = img.shape[:2]

M = h.reshape(3, 3)
dst_width = int(W * s)
dst_height = int(H * s)

skewed_img = cv2.warpPerspective(img, M, (dst_width, dst_height))
cv2.imwrite("skewed_test2.jpg", skewed_img)


