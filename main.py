import fuzzywuzzy
from PIL import Image
import pytesseract
import cv2
import os, os.path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
 


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

if __name__ == "__main__":
    data = {}

    for f in os.listdir("flyer_images"):
        # process all images in directory
        print(f)

        data[f] = processImage("flyer_images/" + f)

        

        print("Done")

    with open("outputTemp.text", "w") as t:
        for f in data:
            t.write(("File: {}\nData:\n{}".format(f, data[f])))

    
