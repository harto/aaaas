ASCII Art As A Service
======================

An API for converting images to basic ASCII art, implemented in Python 3.


Endpoints
---------

 * `GET /` &mdash; basic healthcheck endpoint

 * `POST /images` &mdash; transform the (multipart-form-encoded) `image` file
   into ASCII "artwork". A non-empty `invert` querystring parameter inverts the
   color scheme. (See "Run locally" below.)


Notes
-----

 * There is an (arbitrarily selected) maximum upload size of 1MB.
 * There is no support for specifying output dimensions. The maximum output size
   is 128x128 chars.
 * Flask was chosen as the HTTP abstraction as it's a mature library with a
   simple API. For a system with a single endpoint it's probably fine, but for
   production systems there are probably better choices.
 * Pillow was chosen as the image manipulation library, as it's mature, easier
   to install/configure than e.g. OpenCV, and also has a simple API.


Setup
-----

Install packages using `pip`:
```
$ pip install -r requirements.txt
```

(Note: Pillow may require additional system-level dependencies &mdash; see
http://pillow.readthedocs.io/en/4.1.x/installation.html)


Run locally
-----------

```
$ bin/develop
```

Then, make requests against the API:
```
$ curl -H 'Accept: application/json' \
       -F image=@test/test.png \
       http://127.0.0.1:5000/images?invert=1
```

The image -> ASCII conversion can be run independently from the command line:
```
$ python -m aaaas.image test/test.png
```


Run test suite
--------------

```
$ bin/test
```
