import time
import requests


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

def download(method, url, params = None, data = None, headers = None, wait = 1, maxretries = 3):
    """
    This function 'download's the html from the input url
    """
    try:
        resp = requests.request(method, url, params=params, data=data, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if 500 <= e.response.status_code < 600 and maxretries > 0:
            time.sleep(wait)
            print("Error code:", e.response.status_code, "/// Retry num:", maxretries)
            resp = download(method, url, params, data, headers, timeout, maxretries-1)
        else:
            print(e.response.status_code)
            print(e.response.reason)
    return resp

def login(mainurl, addurl, data, maxretries = 2, wait = 1):
    """
    mainurl: The url where the login page is
    addurl: The additional url that will be added when logged in. It's the action's name.
    data: Dictionary of id, and password. Look for the name of inputs.

    This function makes a cookie first, and then log-in. However, some websites could be logged-in on the first try
    """
    session = requests.Session()
    url = requests.compat.urljoin(mainurl, addurl)
    try:
        for tries in range(maxretries):
            if tries == 0:
                html = session.post(url, data)
                print("First try... Creating cookies")
                # print(html.text)
            else:
                html = session.post(url, data)
                print(tries+1, "nd try...")
                # print(html.text)
            time.sleep(wait)
    except error as e:
        print(e)
    return html

print("Available functions: downlad, login",
      "\nAvailable objects: headers(dict with my user-agent info)")


