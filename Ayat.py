from cv2 import cv2
from pip._vendor.distlib.compat import raw_input
import sys
from PIL import Image
import PIL


txt_input = raw_input("Text Filename: ")
with open(txt_input, encoding='utf8') as t:
    line = t.read()

key = input("key = ")
new_key = ""
for x in range(len(line)):
    k = x % len(key)
    new_key += key[k]

print(line)
print(new_key)
bin_txt = [bin(ord(x))[2:].zfill(8) for x in line]
bin_key = [bin(ord(x))[2:].zfill(8) for x in new_key]


# fungsi mencari nilai terkecil


def pisah(data):
    kurang = {}
    pisahdes = []
    for x in data:
        # Mengubah data desimal menjadi string agar bisa di looping
        r = str(x)
        if len(r) == 3:
            # 2 karakter di depan disebut char awal
            char_awal = r[:-1]
            # print("awal= "+ char_awal)
            pisahdes.append(char_awal)
            # 1 Karakter di belakang
            char_akhir = r[2:]
            # print("akhir =" + char_akhir)
            # Cek jika nilai dari char_akhir lebih dari 1
            if int(char_akhir) >= 2:
                pisahdes.append(char_akhir)
            else:
                pisahdes.clear()
                # cek ukuran String jika berjumlah 2
        elif len(r) == 2:
            # looping string untuk dijadikan array
            for y in r:
                # cek jika lebih dari 1
                if int(y) >= 2:
                    pisahdes.append(y)
                else:
                    pisahdes.clear()
                    break
        # cek jika array lebih dari 0
        if len(pisahdes) > 0:
            # pisahsel = iter(pisahdes)
            # next(pisahsel)
            # pisakhir = int(pisahdes[0])
            # for d in pisahdes:
            #     pisakhir -= int(next(pisahsel, 0))
            print(pisahdes)
            pisakhir = int(pisahdes[0])
            for d in range(len(pisahdes) - 1):
                pisakhir -= int(pisahdes[d + 1])
            kurang[r] = abs(pisakhir)
            print(pisakhir)
        pisahdes.clear()
    return kurang


# fungsi xor
def prosesXor(texts, knci):
    isi = []
    for text, kunci in zip(texts, knci):
        isi.append("".join(str(ord(a) ^ ord(b)) for a, b in zip(text, kunci)))
    return isi


data = prosesXor(bin_txt, bin_key)
# membuat binary menjadi desimal

# print("txt bin = ")
# print(bin_txt)
# print("key bin = ")
# print(bin_key)
print("hasil = ")
print(data)

# ---------------
# mencari koordinat
des = [int(x, 2) for x in bin_key]
abs_des = [abs(x) for x in des]
# print("desimal key= ")
# print(des)

# ---------------------
gambar = Image.open("kucing.png")

# ---------------
# input text dan key

pi = pisah(abs_des)
print(pi)
koordinat = min(pi, key=pi.get) if len(pi) > 0 else "Kunci Tidak Valid"
# koordinat = input("masukan kordinat: ")  # testing input kordinat manual
# ---------------
# ukuran text binary
txt = "".join(data)
# print(txt)
l_txt = len(data)
print(l_txt)
panjang_txt = bin(l_txt)[2:].zfill(16)
print(panjang_txt)

print("ukuran text binary = " + str(l_txt))
# ---------------
# menaruh koordinat
baris = int(koordinat[0] if len(koordinat) < 3 else koordinat[:-1])
kolom = int(koordinat[1] if len(koordinat) < 3 else koordinat[2:])

h = kolom
v = baris

height, width, dimension = gambar.shape

print(str(baris) + "," + str(kolom))


# ----------------
# fungso
# penyisipan
def rgb(image, r, b, lentxt):
    if lentxt:
        panjangdata = bin(image[0])[2:].zfill(8)
        print("awal " +str(image[0]))
        image[0] = int(str(panjangdata[:-1]) + str(b), 2)
        print(image[0])
        datas = bin(image[2])[2:].zfill(8)
        image[2] = int(datas[:-1] + r, 2)
    else:
        data = bin(image[2])[2:].zfill(8)
        image[2] = int(data[:-1] + r, 2)
    # if lentxt:
    #     image[0] = b
    #     image[2] = r
    # else:
    #     image[2] = r


# untuk membuat helm

# ----------------
# menyisipkan ke gambar
# pembatas_helm = helm(kolom, baris, h, v)
pembatas = []
i = 0
ulang_k = 1
ulang_b = 1
berhenti = False
while i < l_txt:
    # perulangan untuk menyisipkan kekanan
    for kanan in range(kolom, kolom + h):
        # variabel untuk pengecekan helm
        cek_kanan = str(baris % height) + "," + str(kanan % width)

        # cek jika looping lebih dari perulangan text
        if i > l_txt:
            break

        # cek jika menabrak helm
        if cek_kanan in pembatas:
            kolom = h + (h + v + 1) * ulang_k
            baris = v
            for k in range(h):
                cekk = str(baris % height) + "," + str(kolom + k % width)
                if cekk in pembatas:
                    berhenti = True
                    print("Text anda melebihi kapasitas maksimal!")
                    break
            ulang_k += 1
            # pembatas_helm = helm(kolom, baris, h, v)
            break

        pembatas.append(cek_kanan)
        # menyisipkan data
        if i < 16:
            rgb((gambar[baris % height, kanan % width]), txt[i], panjang_txt[i], True)
        else:
            rgb((gambar[baris % height, kanan % width]), txt[i], " ", False)
        i += 1
    # untuk menurunikan baris ke bawah
    baris = baris + 1

    # mengecek jika perlu berhenti
    if berhenti:
        break

    # pengecekan untuk menyisipkan ke bawah
    for bawah in range(baris, baris + v):
        # variabel untuk pengecekan helm
        cek_bawah = str(bawah % height) + "," + str(kolom % width)

        # cek jika looping lebih dari perulangan text
        if i > l_txt:
            break

        # # cek jika menabrak helm
        # if cek_bawah in pembatas_helm:
        #     kolom = h
        #     baris = v + (v + 2 + h) * ulang_b
        #     ulang_b += 1
        #     # pembatas_helm = helm(kolom, baris, h, v)
        #     break

        if cek_bawah in pembatas:
            kolom = h + (h + v + 1) * ulang_k
            baris = v
            for k in range(h):
                cekk = str(baris % height) + "," + str(kolom + k % width)
                if cekk in pembatas:
                    berhenti = True
                    print("Text anda melebihi kapasitas maksimal!")
                    break
            ulang_k += 1
            # pembatas_helm = helm(kolom, baris, h, v)
            break

        pembatas.append(cek_bawah)
        # menyisipkan data
        if i < 16:
            rgb((gambar[bawah % height, kolom % width]), txt[i], panjang_txt[i], True)
        else:
            rgb((gambar[bawah % height, kolom % width]), txt[i], " ", False)
        i += 1
    # untuk mengenyampingkan kolom ke kanan
    kolom = kolom + 1

    # mengecek jika perlu berhenti
    if berhenti:
        break

print("jumlah perulangan = " + str(i))
# ----------------
if not berhenti:
    stega_gambar = input("Nama gambar baru: ")
    Image.SAVE(stega_gambar, gambar)
    gambar.show()


