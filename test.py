import requests

url = "http://www.zeyun021.com"

req = requests.get(url)
if req.encoding == "ISO-8859-1":
    encodings = requests.utils.get_encodings_from_content(req.text)
    if encodings:
        encoding = encodings[0]
    else:
        encoding = req.apparent_encoding

    encode_content = req.content.decode(encoding)
