# -*- coding: utf-8 -*-
import sys
import urllib.request as urllib
import numpy as np
import base64
import math
import requests
from PIL import Image, ImageFilter, ImageMath
from scipy import ndimage
from io import BytesIO
#import tensorflow as tf
#import styletransfer as st


# downloads the image, converts it to a NumPy array, and then reads
# it into OpenCV format
def url_to_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

#
# converts given Image into a black & white image
#
# @param Must be an Image, jpg/png
#
# @return Returns the converted black & white image
def blackwhite(image):
    return image.convert("L")

#
# upscales an image based on the given scale parameter
#
# @param image must be an image. jpg/png
# @param scake must be the size multiplier
#
# @return Returns the upscaled image
def upscale(image, scale):
    width, height = image.size[:2]
    return image.resize((width*scale, height*scale), Image.LANCZOS)
    
#
# Calculates the adaptive threshold of an image
# Source:
# https://stackoverflow.com/questions/33091755/bradley-roth-adaptive-thresholding-algorithm-how-do-i-get-better-performance
#
# @param image must be an image. jpg/png
# @param s is the window size
# @param t is the threshold
#
# @return  returns the Cartoon version of the iamge
#
def bradley_roth_numpy(image, s=None, t=None):
    # Convert image to numpy array
    img = np.array(image).astype(np.float)
    # Default window size is round(cols/8)
    if s is None:
        s = np.round(img.shape[1]/8)
    # Default threshold is 15% of the total
    # area in the window
    if t is None:
        t = 15.0
    # Compute integral image
    intImage = np.cumsum(np.cumsum(img, axis=1), axis=0)
    # Define grid of points
    (rows,cols) = img.shape[:2]
    (X,Y) = np.meshgrid(np.arange(cols), np.arange(rows))
    # Make into 1D grid of coordinates for easier access
    X = X.ravel()
    Y = Y.ravel()
    # Ensure s is even so that we are able to index into the image
    # properly
    s = s + np.mod(s,2)
    # Access the four corners of each neighbourhood
    x1 = X - s/2
    x2 = X + s/2
    y1 = Y - s/2
    y2 = Y + s/2
    # Ensure no coordinates are out of bounds
    x1[x1 < 0] = 0
    x2[x2 >= cols] = cols-1
    y1[y1 < 0] = 0
    y2[y2 >= rows] = rows-1
    # Ensures coordinates are integer
    x1 = x1.astype(np.int)
    x2 = x2.astype(np.int)
    y1 = y1.astype(np.int)
    y2 = y2.astype(np.int)
    # Count how many pixels are in each neighbourhood
    count = (x2 - x1) * (y2 - y1)
    # Compute the row and column coordinates to access
    # each corner of the neighbourhood for the integral image
    f1_x = x2
    f1_y = y2
    f2_x = x2
    f2_y = y1 - 1
    f2_y[f2_y < 0] = 0
    f3_x = x1-1
    f3_x[f3_x < 0] = 0
    f3_y = y2
    f4_x = f3_x
    f4_y = f2_y
    # Compute areas of each window
    sums = intImage[f1_y, f1_x] - intImage[f2_y, f2_x] - intImage[f3_y, f3_x] + intImage[f4_y, f4_x]
    # Compute thresholded image and reshape into a 2D grid
    out = np.ones(rows*cols, dtype=np.bool)
    out[img.ravel()*count <= sums*(100.0 - t)/100.0] = False
    # Also convert back to uint8
    out = 255*np.reshape(out, (rows, cols)).astype(np.uint8)
    return Image.fromarray(out)
#
# This method converts an Image into a Cartoon Version
#
# @param image is the image to be converted into a Cartoon Image
#
# @return Returns the Cartoon Image
#
def cartoonify(image):
    grayscale = blackwhite(image)
    grayscale = grayscale.filter(ImageFilter.MedianFilter(5))
    edges =  bradley_roth_numpy(grayscale, 16, 30)
    color = image.filter(ImageFilter.MedianFilter(23))
    try:
        red, green, blue, alpha = color.split()
        red = ImageMath.eval("convert(a&b, 'L')", a=red, b=edges)
        green = ImageMath.eval("convert(a&b, 'L')", a=green, b=edges)
        blue = ImageMath.eval("convert(a&b, 'L')", a=blue, b=edges)
        res = Image.merge("RGBA", (red, green, blue, alpha))    
    except ValueError:
        red, green, blue = color.split()
        red = ImageMath.eval("convert(a&b, 'L')", a=red, b=edges)
        green = ImageMath.eval("convert(a&b, 'L')", a=green, b=edges)
        blue = ImageMath.eval("convert(a&b, 'L')", a=blue, b=edges)
        res = Image.merge("RGB", (red, green, blue))
    return res
#
# checks if the given url is valid
#
# @param url is the url
#
# @return True is it's valid, False if it isn't
#
    
def url_valid(url):
    try:
        urllib.urlopen(url)
        return True
    except ValueError:
        return False

#
# checks if the link pointed to a correct image
#
# @param url is the url of the image
#
# @return True is it's avalid image, False if it isn't
#
def image_valid(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return (img.format == 'JPEG' or img.format == 'PNG')
    except OSError:
        return False

#
# Actual main method. The Service that decides which mode was selected and
# based upon that executes the wanted service.
#
# @param args The JSON that contains the url, selected Mode and the Scale 
#             modifier
#
# @return Either an Image as Byte64 with statusCode 200
#         or statusCode 405 with error message
#
def transformationService(args):
    if not url_valid(args.get("image_url")):
        response = {"body": {"statusCode": 405, "message" : "URL is not valid"}, "headers": {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*' , "Access-Control-Allow-Methods": ["POST", "GET", "OPTIONS"]}}
        return response
    if not image_valid(args.get("image_url")):
        response = {"body": {"statusCode": 405, "message" : "Image needs to be a jpg or png"}, "headers": {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*' , "Access-Control-Allow-Methods": ["POST", "GET", "OPTIONS"]}}
        return response
    img = url_to_image(args.get("image_url", 0))
    selected_mode = args.get("selected_mode", 0)
    if(selected_mode == 1):
        newimg = blackwhite(img)
    elif (selected_mode == 2):
        newimg = upscale(img, args.get("scale", 1))
    elif (selected_mode == 3):
        newimg = cartoonify(img)
    else:
        response = {"body": {"statusCode": 405, "message": "Not a valid mode selected"}, "headers": {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*' , "Access-Control-Allow-Methods": ["POST", "GET", "OPTIONS"]}}
        return response
    
    #returns image as byte64 inside the json
    output = BytesIO()
    newimg.save(output, format='PNG')
    im_data = output.getvalue()
    image_data = base64.b64encode(im_data)
    if not isinstance(image_data, str):
        # Python 3, decode from bytes to string
        image_data = image_data.decode()
    data_url = 'data:image/png;base64,' + image_data
    response = {"body": {"statusCode": 200, "image": data_url}, "headers": {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*' , "Access-Control-Allow-Methods": ["POST", "GET", "OPTIONS"]}}
    return response

# This main method will be invoked when this program is run
#
# @param Cloud Functions actions accept a single parameter,
#        which must be a JSON object.
#           
def main(args):
    return transformationService(args)