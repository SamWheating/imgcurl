import requests

from PIL import Image, ImageColor
from flask import Flask, make_response, redirect, request
from io import BytesIO

import os
import math

PIXEL = " "
MAX_WIDTH = 150
ASPECT_RATIO = 2.3  # characters in a terminal aren't square so we have to stretch the image to compensate.

# Takes a tuple and returns the required characters to print it to terminal.
# 4 element: (r,g,b,opacity)
# 3 element: (r,g,b)
def pixelchar(color):
    
    if type(color) == int:
        color = ImageColor.getrgb(color)
        # color -= 16
        # r = int(color/36)
        # color -= r*36
        # g = int(color/6)
        # b = color - g*6

    else:
        if len(color) == 4:
            if color[3] == 0:
                return "\u001b[0m" + PIXEL
        # normalize color from 24-bit 3*(0-255) to 8-bit 3*(0-5)
        r,g,b = color[0:3]
        r = math.floor(r/51)
        g = math.floor(g/51)
        b = math.floor(b/51)

    # create the appropriate ansi control character.
    color = 16 + 36 * r + 6 * g + b
    ccode = "\u001b[48;5;{}m".format(color)
    return ccode + PIXEL

def image_to_characters(img):
    rows = []
    for row in range(img.size[1]):
        rstring = ""
        for column in range(img.size[0]):
            rstring += pixelchar(img.getpixel((column, row)))
        rstring += "\u001b[0m"
        rows.append(rstring)

    return rows

app = Flask(__name__)

# Resize to a max width of 70px
def get_new_size(size, width):
    if size[0] <= width:
        return size
    return (width, int(size[1]/(size[0]/width)))


@app.route('/')
def base_route():
    url = request.args.get('url', None)
    if url is None:
        img = Image.open('raccoon.png')
    else:
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            if img.mode == 'P':
                img = img.convert('RGBA')
        except Exception as ex:
            return make_response("Error: {}".format(type(ex).__name__), 400)

    width = min(int(request.args.get('width', MAX_WIDTH)), 200)
    img = img.resize((int(img.size[0]*ASPECT_RATIO), img.size[1]))
    img = img.resize(get_new_size(img.size, width))

    resp = redirect("https://samwheating.com", 302)
    lines = image_to_characters(img)
    for i in range(len(lines)):
        resp.headers['{}'.format(i).ljust(3, '-')] = lines[i]
    return resp

if __name__ == '__main__':
    port = os.getenv("PORT", 5000)
    app.run(host='0.0.0.0', port=port)
