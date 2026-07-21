import requests
def getpayments(url):
    response=requests.get(url)
    return response.json().get('data',[])

