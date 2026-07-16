import requests
def getorders(url):
    response=requests.get(url)
    return response.json()

