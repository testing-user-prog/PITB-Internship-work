from datafetchers import products
import pandas as pd
def transformproducts(products):
    products=products.dropna(subset=['title','price'])
    products=products.drop_duplicates(subset=['id'])
    products['title']=products['title'].astype(str).str.slice(0,255)
    products['category']=products['category'].astype(str).str.slice(0,100)
    columnstokeep=['id','title','price','description','category','images','rating']
    res = []
    for x in products['images']:
        # Grab the first image URL from the list, slice it to 255 chars
        first_image = x[0][:255]
        res.append(first_image)

    products['images'] = res
    products=products[columnstokeep]
    products=products.rename(columns={
        'images':'image',
        'rating':'rating_rate'
    })
    return products
    



    

