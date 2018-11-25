## File Api

### Requirements

*   python 3
*   flask (`pip install flask`)

### Usage

Execute `$ python app.py` to run the daemon (and server).

Then make requests to `http://127.0.0.1:5000/api/files`.

* POST request with file (file in form like `-F` parameter of `curl`) will upload file to storage and send you back md5 hash of this file.
* GET request with 'hash' parameter will send you file back if it exists (`http://127.0.0.1:5000/api/files?hash=4291d9011323bc51ecb3db1204f57979` for example).
* DELETE request with 'hash' parameter will delete your file if it exists.

If you make request to `http://127.0.0.1:5000/` or `http://127.0.0.1:5000/api/`, you will have api html home page (the same as readme).
