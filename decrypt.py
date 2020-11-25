from cv2 import cv2
# from pip._vendor.distlib.compat import raw_input

input_image = input("input image: ")
img = cv2.imread(input_image, cv2.IMREAD_UNCHANGED)

key = input("input key: ")

bin_key = [bin(ord(x))[2:].zfill(8) for x in key]
des = [int(x, 2) for x in bin_key]


# abs_des = [abs(x) for x in des]


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


pi = pisah(des)
print(pi)

koordinat = min(pi, key=pi.get) if len(pi) > 0 else "Kunci Tidak Valid"

kolom = int(koordinat[0] if len(koordinat) < 3 else koordinat[:-1])
baris = int(koordinat[1] if len(koordinat) < 3 else koordinat[2:])
print(str(baris) + "," + str(kolom))


def get_len(image, x, y):
    i = 0
    panjangdata1 = ""
    panjangdata2 = ""
    datan = ""
    ke = 0
    tetapx = x
    tetapy = y
    itungx = 0
    itungy = 0
    while i < 8:
        if itungy == tetapy:
            ke = 1
            itungy = 0
            x += 1
        elif itungx == tetapx:
            ke = 0
            itungx = 0
            y +=1
        if ke == 0:
            gambar = image[x, y + itungy]
            panjangdata1 += str(bin(gambar[0])[-1])
            panjangdata2 += str(bin(gambar[1])[-1])
            datan += str(bin(gambar[2])[-1])
            itungy += 1
            i += 1
        elif ke == 1 :
            gambar = image[x + itungx, y]
            print(gambar)
            panjangdata1 += str(bin(gambar[0])[-1])
            panjangdata2 += str(bin(gambar[1])[-1])
            datan += str(bin(gambar[2])[-1])
            itungx += 1
            i += 1
    panjangdata = panjangdata1 + panjangdata2
    print(panjangdata1)
    print(panjangdata2)
    return [panjangdata, datan]


print("hasil: ")
sto = int(get_len(img, baris, kolom)[0], 2)
print(sto)
ton = get_len(img, baris, kolom)[1]
xors = int(ton, 2) ^ int(bin_key[0], 2)


def ambil_text(image, x, y, stop):
    global gambar
    print("stop", stop)
    i = 0
    pembatas = []
    data = ""
    kanan = y
    bawah = x
    height, width, dimension = image.shape
    ulangk = 1
    berhenti = False
    while i < stop:
        for kan in range(y, y + kanan):
            cek_kan = str(x % height) + ',' + str(kan % width)
            if cek_kan in pembatas:
                y = kanan + (bawah + kanan + 1) * ulangk
                x = bawah
                for k in range(kanan):
                    cekk = str(x % height) + ',' + str(y + k % width)
                    if cekk in pembatas:
                        berhenti = True
                        break
                ulangk += 1
                break
            pembatas.append(cek_kan)
            if i > stop:
                break
            gambar = image[x % height, kan % width]
            data += str(bin(gambar[2]))[-1]
            i += 1
        if berhenti:
            break
        x += 1
        for baw in range(x, x + bawah):
            cek_baw = str(baw % height) + ',' + str(y % width)
            if cek_baw in pembatas:
                y = kanan + (bawah + kanan + 1) * ulangk
                x = bawah
                gambar[0] = 255
                for k in range(kanan):
                    cekk = str(x % height) + ',' + str(y + k % width)
                    if cekk in pembatas:
                        berhenti = True
                        break
                ulangk += 1
                break
            pembatas.append(cek_baw)
            if i > stop:
                break
            gambar = image[baw % height, y % width]
            data += str(bin(gambar[2]))[-1]
            i += 1
        if berhenti:
            break
        y += 1
    print("looping ", i)
    return data


print("text: ")
hsil = ambil_text(img, baris, kolom, sto)
print('hasil', len(hsil) / 8)
text = ""
simpan = []
for s in hsil:
    if len(text) < 8:
        text += str(s)
    else:
        simpan.append(text)
        text = str(s)
if len(text) == 8:
    simpan.append(text)

new_key = ""
for x in range(len(simpan)):
    k = x % len(key)
    new_key += key[k]
print(new_key)
print(len(new_key))
keys = [bin(ord(x))[2:].zfill(8) for x in new_key]

isi = []
for text, kunci in zip(simpan, keys):
    isi.append("".join(str(ord(a) ^ ord(b)) for a, b in zip(text, kunci)))
print(" ")
print("".join(chr(int(k, 2)) for k in isi))
cv2.imshow('gambar', img)
cv2.waitKey(0)