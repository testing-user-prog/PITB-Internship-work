import pandas as pd
def ordercountperstatus(db_object):
        response=pd.read_sql(con=db_object,sql="Select * from ordercountsbystatus")
        return response
