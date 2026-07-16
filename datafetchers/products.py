import requests
def getproducts(url):
    response=requests.get(url)
    return response.json().get('products',[])

