from pandas import DataFrame
import pandas as pd
def transformorders(orders):
    db_columns=['id','customer_id','order_date','product_id','quantity']
    orders=orders.dropna()
    df=pd.DataFrame(columns=db_columns)
    flattened_data=[]
    for index,x in orders.iterrows():
        id=x.loc['id']
        customer_id=x.loc['userId']
        order_date=pd.to_datetime(x.loc['date'])
        for y in x.loc['products']:
            prod_id=y['productId']
            quantity=y['quantity']
            flattened_data.append([id,customer_id,order_date,prod_id,quantity])
    return pd.DataFrame(flattened_data,columns=db_columns)
        






