# imgcurl

inspired by [this](https://twitter.com/thingskatedid/status/1280745824951996416) tweet.

See any image on the web with a single `curl`

![imgcurl in action](yoshi.gif)

### Quickstart:

Run this in the terminal: 

`curl -v 'imgcurl.samwheating.com?url=https://shortnur.pro/beeg'`

You'll need to have `curl` installed. 

### Usage:

`curl -v imgcurl.samwheating.com?url=<ANY_DIRECT_IMAGE_URL>`

You can also specify the width (in # of characters) with a `width=<number>` query param. The default is set to 150.

ex: `curl -v imgcurl.samwheating.com?url=<ANY_DIRECT_IMAGE_URL>&width=100`

works with most image formats (transparent PNG is ideal).

These headers get blocked by most production servers (gunicorn etc), and also broke Google Cloud Run. 

### How does this work?

Most modern terminals allow the use of [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code) to modify the colour of text. By breaking down an image into an array of pixels and converting each one into the nearest colour in the 216-colour ANSI palette. 

ANSI escape codes allow for 256 different colours:
```
  0-  7:  standard colours (as in ESC [ 30–37 m)
  8- 15:  high intensity colours (as in ESC [ 90–97 m)
 16-231:  6 × 6 × 6 cube (216 colours): 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)
232-255:  grayscale from black to white in 24 steps
```

So by converting each RGB colour values from a range of 0-255 to 0-5, we can get a reasonable approximation of the true colour to the pixel from the 216-colour ANSI colour cube.

Each "pixel" in the image is thus represented as `\u001b[48;5;<COLOR NUMBER FROM 16-231>m \u001b[0m`.

From here, each pixel in a row is converted into an ANSI control character and written into a string. Each row is then added to the response as a header. 
