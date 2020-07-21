# imgcurl

inspired by [this](https://twitter.com/thingskatedid/status/1280745824951996416) tweet.

See any image on the web with a single `curl`

![imgcurl in action](yoshi.gif)

### Quickstart:

Run this in the terminal: 

`curl -v 'imgcurl.samwheating.com?url=shortnur.pro/beeg'`

You'll need to have `curl` installed. 

### Usage:

`curl -v imgcurl.samwheating.com?url=<ANY_DIRECT_IMAGE_URL>`

You can also specify the width (in # of characters) with a `width=<number>` query param.

ex: `curl -v imgcurl.samwheating.com?url=<ANY_DIRECT_IMAGE_URL>&width=100`

works with most image formats (transparent PNG is ideal).

These headers get blocked by most production servers (gunicorn etc), and also broke Google Cloud Run. 
