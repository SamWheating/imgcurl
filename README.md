# imgcurl

See any image on the web with a single `curl`

![imgcurl in action](yoshi.gif)

inspired by [this](https://twitter.com/thingskatedid/status/1280745824951996416) tweet.

### Usage:

`curl -v imgcurl.samwheating.com?url=<ANY_DIRECT_IMAGE_URL>`

You can also specify the width (in # of characters) with a `width=<number>` query param.

ex: `curl -v imgcurl.samwheating.com?url=<ANY_DIRECT_IMAGE_URL>&width=100`

works with most image formats (transparent PNG is ideal).

These headers get blocked by most production servers (gunicorn etc) so I had to run a flask development server in production - there's probably a better way of doing this. Google Cloud Run also can't handle this, but I'm not sure why
