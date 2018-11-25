## File Api

### Requrements

*   python 3
*   flask (`pip install flask`)

### Usage

Execute `$ python app.py` to run the daemon (and server).

Then make requests to `http://127.0.0.1:5000/api/files`.

* POST request with file (file in form like `-F` parameter of `curl`) will upload file to storage and send you back md5 hash of this file.
* GET request with 'hash' parameter will send you file back if it exists.
* DELETE request with 'hash' parameter will delete your file if it exists.