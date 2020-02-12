import requests

def auth():
    URL = "http://pedidosya.sa.looker.com:19999/api/3.1/login?client_id=VwQwR3TXWS7RFb3K8ZQw&client_secret=2G8f8XYnnRsNkp68XgvMrmfx"
    PARAMS = {'client_id':'VwQwR3TXWS7RFb3K8ZQw', 'client_secret':'2G8f8XYnnRsNkp68XgvMrmfx'}
    r = requests.get(url = URL)

    print(r.json())



auth()