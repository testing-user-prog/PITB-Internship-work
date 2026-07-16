import json
import pandas as pd
from Generators.stringgenerators import get_db_url
from sqlalchemy import create_engine
from datafetchers.customers import getcustomers
from datafetchers.products import getproducts
from Transformers.customer import transformcustomer
from Transformers.products import transformproducts
from datafetchers.orders import getorders
from Transformers.orders import transformorders
with open('config.json', 'r') as f:
    config = json.load(f)


connection_string = get_db_url(
    username=config['db_user'],
    password=config['db_pass'],
    host=config['db_host'],
    port_no=config['db_port'],
    db_name=config['db_name']
)
db_obj=create_engine(connection_string)
# Storing the customer data
# customers_data = pd.DataFrame(getcustomers("https://dummyjson.com/users"))
# customers_data = transformcustomer(customers_data)

# customers_data.to_sql(
# name='customers',
# index=False,
# con=db_obj,
# if_exists='append')

# products_data=pd.DataFrame(getproducts("https://dummyjson.com/products"))
# products_data=pd.DataFrame(transformproducts(products_data))
# products_data.to_sql(
#     index=False,
#     con=db_obj,
#     if_exists='append',
#     name='products',


# )
orders_data=pd.DataFrame(getorders("https://fakestoreapi.com/carts"))
orders_data=transformorders(orders_data)
print(orders_data)
orders_data.to_sql(
    index=False,
    if_exists='append',
    con=db_obj,
    name='orders'
)





print('Successfully Executed')