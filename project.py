import cv2
import numpy as np
from PIL import Image

#it convert data in binary formate


def data2binary(data):
    p = ''
    if type(data) == str:
        p = ''.join([format(ord(i), '08b')for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b')for i in data]   # Returns array of bin values of pix
    return p


# hide data in given img

def hidedata(img, data):    #img(opened with cv2)
    data += "$$"                                   #'$$'--> End Delimeters
    d_index = 0
    b_data = data2binary(data)
    len_data = len(b_data)
    #iterate pixels from image and update pixel values
    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index])
                d_index += 1
            if d_index >= len_data:
                break
    return img


def encode():
    img_name = input("\nEnter image name:")
    image = cv2.imread(img_name)#gives pixels format
    img = Image.open(img_name, 'r')#gives width height
    w, h = img.size
    data = input("\nEnter Message:")
    if len(data) == 0:
        return print("Encrypting failed because the message is empty")
    enc_img = input("\nEnter Encoded Image Name:")
    enc_data = hidedata(image, data)
    cv2.imwrite(enc_img, enc_data)
    img1 = Image.open(enc_img, 'r')
    img1 = img1.resize((w, h),Image.Resampling.LANCZOS)
    # optimize with 65% quality
    if w != h:
        img1.save(enc_img, optimize=True, quality=65)
        return print("Image Encrypted Successfully...")
    else:
        img1.save(enc_img)
        return print("Image Encrypted Successfully...")

# decoding

def extract_data(img):
    bin_data = ""
    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]
    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$$":
            break
    return readable_data[:-2]


def decode():
    img_name = input("\nEnter Encoded Image Name : ")
    image = cv2.imread(img_name)
    msg = extract_data(image)
    return msg

if __name__ == '__main__':
    x = 0
    while x != 3:
        print('''
           1.Encrypt
           2.Decrypt
           3.Exit''')
        x = int(input("\n Enter your choice: "))
        if x == 1:
            encode()
        elif x == 2:
            ans = decode()
            print("\nEncoded message is :" + ans)
    print("Exited Succesfully......")
    print("Thank you for using our image steganography program")