import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from Transformers.customers import transformcustomers
from Transformers.products import transformproducts




load_dotenv()




connection_string = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
db_object=create_engine(connection_string)

customers_df=pd.read_csv('dataset/customers.csv',header=0)
products_df=pd.read_csv('dataset/products.csv',header=0)
orders_df=pd.read_csv('dataset/orders.csv',header=0)
customers_df,dropped_customers_df=transformcustomers(customers_df)
products_df,dropped_products_df=transformproducts(products_df)
dropped_customers_df.to_csv('dataset/deleted_customer.csv',index=False)
dropped_products_df.to_csv('dataset/deleted_products.csv',index=False)

# customers_df.to_sql(
#     con=db_object,
#     index=False,
#     name='customers',
#     if_exists='append'
# )


# products_df.to_sql(
#     con=db_object,
#     index=False,
#     name='products',
#     if_exists='append'
# )

print('Program Executed Successfully')


