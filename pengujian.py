from cv2 import cv2
import glob
import numpy as np

original = cv2.imread("train.png")
stego = cv2.imread("20%.png")

bOri, gOri, rOri = cv2.split(original)
bStego, gStego, rStego = cv2.split(stego)

row, column = rStego.shape

total = 0
for i in range(row):
    for j in range(column):
        power = (np.float(rOri[i, j])-np.float(rStego[i,j]))**2
        total = total + power

MSE = total/(row*column)
print("MSE: ",MSE)

PSNR = 10 * np.log10(255**2)/MSE
print("PSNR :", PSNR)





