import hashlib
import re
import uuid

def uuid4():
    return str(uuid.uuid4())

def sha3_256(data: bytes) -> bytes:
    h = hashlib.sha3_256()
    h.update(data)
    return h.digest()

def md5(text: str):
    md = hashlib.md5(text.encode('utf-8'))
    return md.hexdigest()


def is_empty_str(s: str) -> bool:
    return s is None or len(s.strip()) == 0


def is_valid_url(url):
    pattern = re.match(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',
                       url, re.IGNORECASE)
    if pattern:
        return True
    else:
        return False
