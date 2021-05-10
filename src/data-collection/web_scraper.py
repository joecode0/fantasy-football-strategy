from proxy_requests import ProxyRequests
import requests
from bs4 import BeautifulSoup as soup

def get_raw_html(web_link):
    r = ProxyRequests(web_link)
    r.get()
    page = soup(r.get_raw(), "html.parser")
    return page