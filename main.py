from fuzzywuzzy import fuzz
from PIL import Image
import pytesseract
import cv2
import os, os.path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
 

productSet = []
unitSet = []


def processImage(filename, threshold = None, process = None):
    # load the example image and convert it to grayscale

    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    '''# show the output images
    cv2.imshow("Image", image)
    cv2.imshow("Output", gray)
    cv2.waitKey(0)'''

    # check to see if we should apply thresholding to preprocess the
    # image
    if threshold:
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # make a check to see if median blurring should be done to remove
    # noise
    elif process:
        gray = cv2.medianBlur(gray, 3)
    
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, image) # try rgb

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text

def fileRead():
    data = {}

    for f in os.listdir("flyer_images"):
        # process all images in directory
        print(f)

        data[f] = processImage("flyer_images/" + f)
        print("Done")

    with open("outputTemp.txt", "w") as t:
        for f in data:
            t.write(("File: {}\nData:\n{}".format(f, data[f])))

def popMax(arr):
    if arr != []:
        k = max(arr)
        arr.remove(k)
    else:
        k = 0
    return k

def interpreter(filename):

    l = []

    with open(filename, "r") as f:
        s = f.read()

        i = 0 # i to check for "File: " pointer

        while s.find("week", i) != -1:
            

            i = s.find("week", i)
            print(i)
            iNext = s.find("week", i+5)
            # find the next instance of "find to denote the end of the data stream"
            fName = s[i:s.find("\n", i)]

            dStart = s.find("Data:", i) + 6

            data = s[dStart:iNext] # TODO PROCESS THIS DATA STRING

            num = [int(s) for s in data.split() if s.isdigit()]
            print(num)

            for p in productSet:
                if fuzz.partial_ratio(p, data) > 75:
                    print(p)
                    d = {}
                    d["product_name"] = p

                    d["unit_promo_price"] = popMax(num)

                    d["flyer_name"] = fName.replace(".jpg", "")

                
                    d["uom"] = ":)"
                    d["least_unit_for_promo"] = popMax(num)
                    d["save_per_unit"] = popMax(num)

                    d["discount"] = popMax(num)
                    d["organic"] = 0

                    l.append(d)

            i = iNext
            
    return l

if __name__ == "__main__":

    with open("product_dictionary.csv", "r") as p:
        productSet += (p.read().split("\n"))

    data = interpreter("outputTemp.txt")
    
    with open("output.csv", "w") as csv:
        csv.write("flyer_name, product_name, unit_promo_price, uom, least_unit_for_promo, save_per_unit, discount, organic")

        for e in data:
            csv.write("\n")
            csv.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(e["flyer_name"], e["product_name"], e["unit_promo_price"], e["uom"], e["least_unit_for_promo"], e["save_per_unit"], e["discount"], e["organic"]))
    
