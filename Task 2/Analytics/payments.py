import pandas as pd
def month_over_month_revenue(db_object):
    response = pd.read_sql(con=db_object, sql="Select * from month_over_month_revenue")
    if 'revenue_month' in response.columns:
        response['revenue_month'] = pd.to_datetime(response['revenue_month']).dt.tz_localize(None)
    return response
