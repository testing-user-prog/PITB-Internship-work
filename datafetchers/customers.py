import requests
def getcustomers(url):
    response=requests.get(url)
    return response.json().get('users',[])

