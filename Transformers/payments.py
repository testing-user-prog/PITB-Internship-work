import pandas as pd
def transformpayments(payments_data):
    df_payments = payments_data[['orderId', 'amount', 'method', 'status', 'createdAt']]
    df_payments['createdAt']=pd.to_datetime(df_payments['createdAt'])
    df_payments=df_payments.dropna()
    df_payments=df_payments.rename(columns={
        'orderId':'order_id',
        'method':'payment_method',
        'createdAt':'payment_date'



        }
    )
    return df_payments


