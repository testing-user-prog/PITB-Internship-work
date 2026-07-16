import requests
import pandas as pd
def getcustomers(url):
    response=requests.get(url)
    return response.json().get('users',[])

