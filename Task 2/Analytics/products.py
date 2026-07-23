import pandas as pd
def revenuepercategory(db_object):
        response=pd.read_sql(con=db_object,sql="Select * from revenuepercategory")
        return response
