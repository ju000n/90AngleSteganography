from tkinter import *
from tkinter import filedialog, simpledialog
from pathlib import Path
from tkinter.scrolledtext import ScrolledText

from cv2 import cv2
from PIL import ImageTk, Image
import math

screen = Tk(screenName="Steganography")
screen.geometry("600x600")
title_txt = Label(text="Decrypt", bg="grey", width=600, height="2")
title_txt.pack()
imgcv = NONE


# find the coordinate
def pisah(data):
    kurang = {}
    pisahdes = []
    for x in data:
        # Mengubah data desimal menjadi string agar bisa di looping
        r = str(x)
        if len(r) == 3:
            # 2 karakter di depan disebut char awal
            char_awal = r[:-1]
            pisahdes.append(char_awal)
            # 1 Karakter di belakang
            char_akhir = r[2:]
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
            print(pisahdes)
            pisakhir = int(pisahdes[0])
            for d in range(len(pisahdes) - 1):
                pisakhir -= int(pisahdes[d + 1])
            kurang[r] = abs(pisakhir)
            print(pisakhir)
        pisahdes.clear()
    return kurang


# # new_key1 = []
# new_key = " "
#
# def newKey(key):
#     global new_key
#     new_key = ""
#     # key = input_key_box.get()
#     print(key)
#     for x in range(len(simpan)):
#         k = x % len(key)
#         new_key += key[k]
#     print(new_key)
#     print(len(new_key))
#     # return new_key
#     bin_key = [bin(ord(x))[2:].zfill(8) for x in new_key]
#     print(new_key)
#     # print(bin_key)
#     return bin_key


binary_key = ""
koordinat = IntVar()
x_axis = 0
y_axis = 0
d = ""


def cordinatKey():
    global binary_key
    global koordinat
    global imgcv
    global x_axis
    global y_axis
    global d
    input = input_key_box.get()
    # real_key = newKey(input_key_box.get())
    print(input)
    binary_key = [bin(ord(x))[2:].zfill(8) for x in input]
    print(binary_key)
    des = [int(x, 2) for x in binary_key]
    abs_des = [abs(x) for x in des]
    pi = pisah(abs_des)
    koordinat = min(pi, key=pi.get) if len(pi) > 0 else "Kunci Tidak Valid "
    x_axis = int(koordinat[0] if len(koordinat) < 3 else koordinat[:-1])
    y_axis = int(koordinat[1] if len(koordinat) < 3 else koordinat[2:])
    stop = length_txt(x_axis, y_axis)
    print(koordinat)
    print(str(x_axis) + "," + str(y_axis))
    data_txt = ambil_text(imgcv, x_axis, y_axis, stop)
    print(data_txt)
    print('hasil', len(data_txt) / 8)
    text = ""
    simpan = []
    for s in data_txt:
        if len(text) < 8:
            text += str(s)
        else:
            simpan.append(text)
            text = str(s)
    if len(text) == 8:
        simpan.append(text)
    new_key = ""
    for x in range(len(simpan)):
        k = x % len(input)
        new_key += input[k]
    print(new_key)
    print(len(new_key))
    keys = [bin(ord(x))[2:].zfill(8) for x in new_key]
    isi = []
    for text, kunci in zip(simpan, keys):
        isi.append("".join(str(ord(a) ^ ord(b)) for a, b in zip(text, kunci)))
    print(" ")
    d = "".join(chr(int(k, 2)) for k in isi)
    print(d)
    setText(str(d))


def openImage():
    fnImage = filedialog.askopenfilename(title="open")
    return fnImage


def displayImage():
    global img
    global imgcv
    x = openImage()
    imgcv = cv2.imread(x)
    img = Image.open(x)
    img = ImageTk.PhotoImage(img)
    image_canvas = Label(screen, width=200, height=200, image=img)
    dimensions = "%dx%d" % (img.width(), img.height())
    print(dimensions)
    # size
    image_canvas.image = img
    sizeLabel = Label(text=dimensions)
    sizeLabel.place(x=70, y=240)
    image_canvas.pack()
    image_canvas.place(x=205, y=50)


def decrypt(image, x, y):
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
            y += 1
        if ke == 0:
            gambar = image[x, y + itungy]
            panjangdata1 += str(bin(gambar[0])[-1])
            panjangdata2 += str(bin(gambar[1])[-1])
            datan += str(bin(gambar[2])[-1])
            itungy += 1
            i += 1
        elif ke == 1:
            gambar = image[x + itungx, y]
            print(gambar)
            panjangdata1 += str(bin(gambar[0])[-1])
            panjangdata2 += str(bin(gambar[1])[-1])
            datan += str(bin(gambar[2])[-1])
            itungx += 1
            i += 1
    panjangdata = panjangdata1 + panjangdata2
    return panjangdata


def length_txt(x_axis, y_axis):
    global binary_key
    print(x_axis, y_axis)
    panjag_data = int(decrypt(imgcv, y_axis, x_axis), 2)
    return panjag_data


def ambil_text(image, x, y, stop):
    global gambar
    print("stop", stop)
    i = 0
    pembatas = []
    data = ""
    kanan = x
    bawah = y
    height, width, dimension = image.shape
    ulangk = 1
    berhenti = False
    while i < stop:
        for kan in range(x, x + kanan):
            cek_kan = str(y % height) + ',' + str(kan % width)
            if cek_kan in pembatas:
                x = kanan + (bawah + kanan + 1) * ulangk
                y = bawah
                for k in range(kanan):
                    cekk = str(y % height) + ',' + str(x + k % width)
                    if cekk in pembatas:
                        berhenti = True
                        break
                ulangk += 1
                break
            pembatas.append(cek_kan)
            if i > stop:
                break
            gambar = image[y % height, kan % width]
            data += str(bin(gambar[2]))[-1]
            i += 1
        if berhenti:
            break
        y += 1
        for baw in range(y, y + bawah):
            cek_baw = str(baw % height) + ',' + str(x % width)
            if cek_baw in pembatas:
                x = kanan + (bawah + kanan + 1) * ulangk
                y = bawah
                gambar[0] = 255
                for k in range(kanan):
                    cekk = str(y % height) + ',' + str(x + k % width)
                    if cekk in pembatas:
                        berhenti = True
                        break
                ulangk += 1
                break
            pembatas.append(cek_baw)
            if i > stop:
                break
            gambar = image[baw % height, x % width]
            data += str(bin(gambar[2]))[-1]
            i += 1
        if berhenti:
            break
        x += 1
    print("looping ", i)
    return data


def setText(text):
    text_area.insert(END, text)
    text_area.update_idletasks()

# Label
input_image = Label(text="Input Stego Image: ")
size_img = Label(text="Size: ")
input_key = Label(text="Input Key ")

# Entry
input_key_box = Entry(screen, borderwidth=5, width=50)
text_area = ScrolledText(screen, width=40, height=10, fg="green")
# text_area.config(state=DISABLED)
# text_area.delete(0.0, END)
# text_area.insert(1.0, d)
text_area.pack()
# Button
icon_img = PhotoImage(file=r"browseImgMini.png")
btnOpenImg = Button(image=icon_img, command=lambda: displayImage())
btnOpenImg.pack()

btnDecrypt = Button(text="Decrypt", font="Helvetica 12", width=16, height=2, bg="blue", command=lambda: cordinatKey())
btnDecrypt.pack()

# Place
size_img.place(x=40, y=240)
input_image.place(x=40, y=40)
btnOpenImg.place(x=460, y=40)
input_key.place(x=40, y=270)
input_key_box.place(x=140, y=300)
btnDecrypt.place(x=225, y=340)
text_area.place(x=135, y=400)
screen.mainloop()
