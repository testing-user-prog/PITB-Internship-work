from dateutil import relativedelta
from dateutil import relativedelta
from dateutil import relativedelta
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from Transformers.customers import transformcustomers
from Transformers.products import transformproducts
from Transformers.orders import transformorders
from Analytics.customers import gettop5customers
from Analytics.orders import ordercountperstatus
from Analytics.products import revenuepercategory
from Analytics.payments import month_over_month_revenue


load_dotenv()




connection_string = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
db_object=create_engine(connection_string)

customers_df=pd.read_csv('dataset/customers.csv',header=0)
products_df=pd.read_csv('dataset/products.csv',header=0)
orders_df=pd.read_csv('dataset/orders.csv',header=0)

customers_df,dropped_customers_df=transformcustomers(customers_df)
products_df,dropped_products_df=transformproducts(products_df)
orders_df,dropped_orders_df=transformorders(orders_df)

dropped_customers_df.to_csv('dataset/deleted_customer.csv',index=False)
dropped_products_df.to_csv('dataset/deleted_products.csv',index=False)
dropped_orders_df.to_csv('dataset/deleted_orders.csv',index=False)
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

# orders_df.to_sql(
#     con=db_object,
#     index=False,
#     name='orders',
#     if_exists='append'
# )

top_cus=gettop5customers(db_object)
order_status_df=ordercountperstatus(db_object)
revenue_category_df=revenuepercategory(db_object)
mom_revenue_df=month_over_month_revenue(db_object)

output_path='dataset/analytics.xlsx'

with pd.ExcelWriter(output_path,engine='openpyxl') as writer:
    top_cus.to_excel(writer,sheet_name='top5customers',index=False)

    order_status_df.to_excel(writer,sheet_name='ordercountperstatus',index=False)

    revenue_category_df.to_excel(writer,sheet_name='revenueincategories',index=False)

    mom_revenue_df.to_excel(writer,sheet_name='mom_revenue',index=False)






print('Program Executed Successfully')


