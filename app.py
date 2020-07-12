from PIL import Image
from flask import Flask, make_response, redirect

import os
import math

PIXEL = " "

# Takes a 4-element (r,g,b,opacity) tuple and returns the required characters to print it to terminal.
def pixelchar(color):
    if color[3] == 0:
        return "\u001b[0m" + PIXEL
    
    r,g,b = color[0:3]
    r = math.floor(r/51)
    g = math.floor(g/51)
    b = math.floor(b/51)

    color = 16 + 36 * r + 6 * g + b

    ccode = "\u001b[48;5;{}m".format(color)
    return ccode + PIXEL

def generate_headers(imgpath):
    headers = []
    img = Image.open(imgpath)
    for row in range(img.size[1]):
        rstring = ""
        for column in range(img.size[0]):
            rstring += pixelchar(img.getpixel((column, row)))
        rstring += "\u001b[0m"
        headers.append(rstring)

    return headers

app = Flask(__name__)

@app.route('/')
def hello():
    resp = redirect("https://samwheating.com", 302)
    headers = generate_headers('raccoon.png')
    for i in range(len(headers)):
        resp.headers['r{}'.format(i).ljust(5, '-')] = headers[i]
    return resp

if __name__ == '__main__':
    port = os.getenv("PORT", 5000)
    app.run(host='0.0.0.0', port=port)
