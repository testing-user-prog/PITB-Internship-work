import json
import pandas as pd
from Generators.stringgenerators import get_db_url
from sqlalchemy import create_engine
from datafetchers.customers import getcustomers
from Transformers.customer import transformcustomer
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
print('Successfully Executed')
customers_data = pd.DataFrame(getcustomers("https://dummyjson.com/users"))
customers_data = transformcustomer(customers_data)
with db_obj.connect() as connection:
    customers_data.to_sql(
    name='customers',
    index=False,
    con=db_obj,
    if_exists='append')
    connection.commit()
