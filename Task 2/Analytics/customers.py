import pandas as pd
def gettop5customers(db_object):
    response=pd.read_sql(con=db_object,sql="Select * from top5customers")
    return response
