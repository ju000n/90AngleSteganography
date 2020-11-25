from cv2 import cv2
import sys

txt = input("txt = ")
key = input("key = ")

# convert string to binary
bint = [bin(ord(x))[2:].zfill(8) for x in txt]
bins = [bin(ord(x))[2:].zfill(8) for x in key]

# fungsi xor
def prosesXor(texts, knci):
    isi = []
    for text, kunci in zip(texts, knci):
        isi.append("".join(str(ord(a) ^ ord(b)) for a, b in zip(text, kunci)))
    return isi

# kembalian dari fungsi xor
data = prosesXor(bint, bins)
# membuat binary menjadi desimal
des = [int(x, 2) for x in bins]
print("txt bin = ")
print(bint)
print("key bin = ")
print(bins)
print("hasil = ")
print(data)
print("desimal key= ")
print(des)

def pisah(data):
    kurang = {}
    pisahdes = []
    for x in data:
        #Mengubah data desimal menjadi string agar bisa di looping
        r = str(x)
        if len(r) == 3:
            #2 karakter di depan disebut char awal
            char_awal = r[:-1]
            # print("awal= "+ char_awal)
            pisahdes.append(char_awal)
            #1 Karakter di belakang
            char_akhir = r[2:]
            # print("akhir =" + char_akhir)
            #Cek jika nilai dari char_akhir lebih dari 1
            if int(char_akhir) >= 2:
                pisahdes.append(char_akhir)
            else:
                pisahdes.clear()

                #cek ukuran String jika berjumlah 2
        elif len(r) == 2:
            #looping string untuk dijadikan array
            for y in r:
                #cek jika lebih dari 1
                if int(y) >= 2:
                    pisahdes.append(y)
                else:
                    pisahdes.clear()
                    break
        #cek jika array lebih dari 0
        if len(pisahdes) > 0:
            pisahsel = iter(pisahdes)
            next(pisahsel)
            pisakhir = int(pisahdes[0])
            for d in pisahdes:
                pisakhir -= int(next(pisahsel, 0))
            kurang[r] = abs(pisakhir)
        pisahdes.clear()
    return kurang
pi = pisah(des)
koordinat = min(pi, key= pi.get) if len(pi) > 0 else "Kunci Tidak Valid"

print(koordinat)

if koordinat == "Kunci Tidak Valid":
    sys.exit("Kunci Tidak Valid")

cc = cv2.imread("kucing.jpg")


def tobinnary(data):
    return [bin(int(data))[2:].zfill(8)]

x = koordinat[0] if len(koordinat) < 3 else koordinat[:-1]
y = koordinat[1] if len(koordinat) < 3 else koordinat[2:]

print("x : " + x)
print("y : " + y)

x = int(x)
y = int(y)

h = x
v = y

print("h =" + str(h))
print("v =" + str(v))

heigth = cc.shape[0]
widht = cc.shape[1]

text = "".join(str(x) for x in data)

print(heigth, widht)

i = 0
j = 0
f = 0

o = x
p = y

# untuk menentukan ke kanan atau ke kiri
ke = 0

lengt_text = tobinnary(len(text))[0]
print(len(text))
u = 0
z = 0
ada = []
cek = False

def awal():
    adss = []
    for b in range(0, x):
        adss.append(str((x-1) + b+1) + ',' + str(y-1))
        ssa = cc[y - 1 , (x-1) + b+1]
        ssa[0] = 255
        ssa[1] = 255
        ssa[2] = 255
    for n in range(0, y+1):
        adss.append(str(x-1) + ',' + str(y+n))
        ssa = cc[y + n, x - 1]
        ssa[0] = 255
        ssa[1] = 255
        ssa[2] = 255
    print(adss)
    return adss

berhenti = awal()
# fdsawe
# fdsaew
while i < len(text):
    print(i)
    lond = text[i]
    # if u == 255:
    #     u = 0
    # if z == 255:
    #     z = 0x
    cari = str((x+f) % widht) + ',' + str(y % heigth)
    if cari in berhenti:
        break
    if cari in ada:
        cek = True
    if j == h and ke == 0 or f == h and ke == 0 or cek == True and ke == 0:
        ada.append(str((x + f) % widht) + ',' + str(y % heigth))
        ss = cc[y % heigth, (x+f) % widht]
        ss[0] = 255
        ss[1] = 255
        ss[2] = 255
        p = p + 1
        y = p
        ke = 1
        f = 0
        j = 0
        cek = False
    elif j == v and ke == 1 or f == v and ke == 1 or cek == True and ke == 1:
        ada.append(str(x % widht) + ',' + str((y+f) % heigth))
        ss = cc[(y+f) % heigth, x % widht]
        ss[0] = 255
        ss[1] = 255
        ss[2] = 255
        o = o + 1
        x = o
        ke = 0
        f = 0
        j = 0
        cek = False
    if ke == 0:
        if f == widht:
            x = 0
            f = 0
        data = cc[y % heigth, (x+f) % widht]
        # data = cc[y, x+f]
        # data[0] = int(str(tobinnary(str(data[0]))[0][:-1]) + str(text[i]), 2)
        data[0] = 0
        data[1] = 0
        data[2] = 0
        if i < 8:
            # data[2] = int(str(tobinnary(str(data[2]))[0][:-1]) + str(lengt_text[i]), 2)
            data[2] = 255
    if ke == 1:
        if f == heigth:
            y = 0
            f = 0
        data = cc[(y+f) % heigth, x % widht]
        # data = cc[y+f, x]
        # data[0] =
        # int(str(tobinnary(str(data[0]))[0][:-1]) + str(text[i]), 2)
        data[0] = 0
        data[1] = 0
        data[2] = 0
        if i < 8:
            # data[2] = int(str(tobinnary(str(data[2]))[0][:-1]) + str(lengt_tzext[i]), 2)
            data[2] = 255
    u += 25
    z += 25
    f += 1
    j += 1
    i += 1

print(ada)

cv2.imshow("percobaan", cc)
cv2.waitKey(0)

