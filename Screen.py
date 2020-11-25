from tkinter import *
from tkinter import filedialog, simpledialog
from pathlib import Path
from cv2 import cv2
from PIL import ImageTk, Image
import math

screen = Tk(screenName="Steganography")
screen.geometry("600x600")
title_txt = Label(text="Steganography", bg="grey", width=600, height="2")
title_txt.pack()
imgcv = NONE
content = StringVar()


def openfile():
    global content
    file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
    if file is not None:
        content = file.read()
        print(content)
        txtcounter = len(content)
        counterlabel = Label(text=txtcounter)
        counterlabel.place(x=140, y=90)
    setText(Path(file.name).name)


#find the coordinate
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


# new_key1 = []
new_key = " "

def newKey(key):
    global new_key
    new_key = ""
    # key = input_key_box.get()
    print(key)
    for x in range(len(content)):
        k = x % len(key)
        new_key += key[k]
    # return new_key
    bin_key = [bin(ord(x))[2:].zfill(8) for x in new_key]
    print(new_key)
    # print(bin_key)
    return bin_key


binary_key = StringVar()
koordinat = IntVar()

def cordinatKey(input):
    global binary_key
    global koordinat
    # real_key = newKey(input_key_box.get())
    print(input)
    binary_key = [bin(ord(x))[2:].zfill(8) for x in input]
    print(binary_key)
    des = [int(x, 2) for x in binary_key]
    abs_des = [abs(x) for x in des]
    pi = pisah(abs_des)
    koordinat = min(pi, key=pi.get) if len(pi) > 0 else "Kunci Tidak Valid "
    print(koordinat)
    return koordinat
    # print_kor = Label(text=koordinat)
    # print_kor.place(x=40, y=480)
    # print_kor.pack


#Label
input_file = Label(text="Input File")
char_counter = Label(text="Text Character: ")
input_image = Label(text="Input Cover Image")
max_char = Label(text="Max Character can be embeded: ")
size_img = Label(text="Size: ")
input_key = Label(text="Input Key ")

#Entry
input_file_box = Entry(screen, borderwidth=5, width=50)
input_file_box.pack()

input_key_box = Entry(screen, borderwidth=5, width=50)


def setText(text):
    input_file_box.delete(0, END)
    input_file_box.insert(0, text)


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
    #size
    image_canvas.image = img
    sizeLabel = Label(text=dimensions)
    sizeLabel.place(x=70, y=330)
    #max_char
    max_chara = (math.floor(((img.width() * img.height()) * 80 / 100) / 8))
    maxCharLabel = Label(text=max_chara)
    maxCharLabel.place(x=220, y=360)
    image_canvas.pack()
    image_canvas.place(x=205, y=125)


def process_enc(text, key):
    isi = []
    for text, kunci in zip(text, key):
        isi.append("".join(str(ord(a) ^ ord(b)) for a, b in zip(text, kunci)))
    return isi


encryptText = StringVar()
y_axis = IntVar()
x_axis = IntVar()


def encrypt():
    global encryptText
    global x_axis
    global y_axis
    global length_encryptText
    textValue = [bin(ord(x))[2:].zfill(8) for x in content]
    first_dot = cordinatKey(input_key_box.get())
    keyValue = (newKey(input_key_box.get()))
    Enc = process_enc(textValue, keyValue)
    # print(Enc)
    encryptText = "".join(Enc)
    length_encryptText = len(encryptText)
    l_text = bin(length_encryptText)[2:].zfill(16)
    # l_text_b = l_text[:8]
    # l_text_g = l_text[8:]
    #kordinat
    x_axis = int(koordinat[0] if len(koordinat) < 3 else koordinat[:-1])
    y_axis = int(koordinat[1] if len(koordinat) < 3 else koordinat[2:])
    print(x_axis)
    print(y_axis)
    embed(imgcv, encryptText, l_text, x_axis, y_axis, length_encryptText)


def rgb(image, r, g, b, lentxt):
    if lentxt:
        panjangdata1 = bin(image[0])[2:].zfill(8)
        panjangdata2 = bin(image[1])[2:].zfill(8)
        image[0] = int(str(panjangdata1[:-1]) + str(b), 2)
        image[1] = int(str(panjangdata2[:-1]) + str(g), 2)
        datas = bin(image[2])[2:].zfill(8)
        image[2] = int(datas[:-1] + r, 2)
    else:
        data = bin(image[2])[2:].zfill(8)
        image[2] = int(data[:-1] + r, 2)


def new_img():
    n_img = simpledialog.askstring("Stego Image", "Enter New stego Image Name: ")
    print(n_img)
    return n_img

def embed(gambar, txt, panjang_txt, x_axis, y_axis, l_txt):
    edge = []
    panjang_txt1 = panjang_txt[:8]
    panjang_txt2 = panjang_txt[8:]
    horizontal = x_axis
    vertical = y_axis
    height, width, dimension = gambar.shape
    i = 0
    ulang_k = 1
    berhenti = False
    while i < length_encryptText:
        # perulangan untuk menyisipkan kekanan
        for kanan in range(x_axis, x_axis + horizontal):
            # variabel untuk pengecekan helm
            cek_kanan = str(y_axis % height) + "," + str(kanan % width)

            # cek jika looping lebih dari perulangan text
            if i > l_txt - 1:
                break

            # cek jika menabrak helm
            if cek_kanan in edge:
                x_axis = horizontal + (horizontal + vertical + 1) * ulang_k
                y_axis = vertical
                for k in range(horizontal):
                    cekk = str(y_axis % height) + "," + str(x_axis + k % width)
                    if cekk in edge:
                        berhenti = True
                        print("Text anda melebihi kapasitas maksimal!")
                        break
                ulang_k += 1
                # pembatas_helm = helm(kolom, baris, h, v)
                break

            edge.append(cek_kanan)
            # menyisipkan data
            if i < 8:
                rgb((gambar[y_axis % height, kanan % width]), txt[i], panjang_txt2[i], panjang_txt1[i], True)
            else:
                rgb((gambar[y_axis % height, kanan % width]), txt[i], " ", " ", False)
            i += 1
        # untuk menurun kan baris ke bawah
        y_axis = y_axis + 1

        # mengecek jika perlu berhenti
        if berhenti:
            break

        # pengecekan untuk menyisipkan ke bawah
        for bawah in range(y_axis, y_axis + vertical):
            # variabel untuk pengecekan helm
            cek_bawah = str(bawah % height) + "," + str(x_axis % width)

            # cek jika looping lebih dari perulangan text
            if i > l_txt - 1:
                break

            if cek_bawah in edge:
                x_axis = horizontal + (horizontal + vertical + 1) * ulang_k
                y_axis = vertical
                for k in range(horizontal):
                    cekk = str(y_axis % height) + "," + str(x_axis + k % width)
                    if cekk in edge:
                        berhenti = True
                        print("Text anda melebihi kapasitas maksimal!")
                        break
                ulang_k += 1
                # pembatas_helm = helm(kolom, baris, h, v)
                break

            edge.append(cek_bawah)
            # menyisipkan data
            if i < 8:
                rgb((gambar[bawah % height, x_axis % width]), txt[i], panjang_txt2[i], panjang_txt1[i], True)
            else:
                rgb((gambar[bawah % height, x_axis % width]), txt[i], " ", " ", False)
            i += 1
        # untuk mengenyampingkan kolom ke kanan
        x_axis = x_axis + 1

        # mengecek jika perlu berhenti
        if berhenti:
            break
    if not berhenti:
        stega = simpledialog.askstring("Stego Image", "enter new name: ")
        cv2.imwrite(stega, gambar)
        # cv2.imshow('gambar', gambar)
        # cv2.waitKey(0)
        success = Label(text="Encrypt Success!", fg="green")
        success.place(x=90, y=560)
        success.pack()





#Button
icon = PhotoImage(file=r"Open.png")
btnOpen = Button(image=icon, command=lambda: openfile())
btnOpen.pack()

icon_img = PhotoImage(file=r"browseImgMini.png")
btnOpenImg = Button(image=icon_img, command=lambda : displayImage())
btnOpenImg.pack()

btnEncrypt = Button(text="Encrypt", font="Helvetica 12", width=16, height=2, bg="green", command=lambda: encrypt())
btnEncrypt.pack()




#place
size_img.place(x=40, y=330)
input_image.place(x=40, y=125)
char_counter.place(x=40, y=90)
input_file.place(x=40, y=50)
input_file_box.place(x=140, y=48)
btnOpen.place(x=460, y=50)
btnOpenImg.place(x=460, y=125)
max_char.place(x=40, y=360)
input_key.place(x=40, y=400)
input_key_box.place(x=140, y=400)
btnEncrypt.place(x=210, y=440)
screen.mainloop()


# Resize
# import cv2
#
# image = cv2.imread("snowpiercer.jpg")
# resiz = cv2.resize(image, (220, 180))
# cv2.imwrite("percob.gif", resiz)
#
# cv2.imshow("window", resiz)
# cv2.imshow("ori", image)
# cv2.waitKey(0)
