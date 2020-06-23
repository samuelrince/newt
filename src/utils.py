import tldextract
import urllib.parse


def get_domain(url: str) -> str:
    extracted = tldextract.extract(url)
    return f'{extracted.domain}.{extracted.suffix}'


def decode_url(url: str) -> str:
    return urllib.parse.unquote_plus(url)


def encode_url(url: str) -> str:
    return urllib.parse.quote_plus(url)
