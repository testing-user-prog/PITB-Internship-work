import pandas as pd
import copy

def transformorders(orders_df):
    orders_cols = copy.deepcopy(list(orders_df.columns))
    
    
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'], errors='coerce',dayfirst=True,format='mixed')
    
    
    deleted_dataframe_cols = orders_cols.copy()
    deleted_dataframe_cols.append('Reason')
    
    null_cols = ['id', 'customer_id', 'order_date', 'product_id', 'quantity']
    null_mask = orders_df[null_cols].isna().any(axis=1)
    
    deleted_rows = pd.DataFrame(columns=deleted_dataframe_cols)
    if null_mask.any():
        null_deleted = orders_df[null_mask].copy()
        null_deleted['Reason'] = 'Null value found'
        deleted_rows = pd.concat([deleted_rows, null_deleted], ignore_index=True)
        orders_df = orders_df[~null_mask].copy()
    
    dup_cols = ['id']
    dup_mask = orders_df[dup_cols].duplicated(keep='first')
    
    if dup_mask.any():
        dup_deleted = orders_df[dup_mask].copy()
        dup_deleted['Reason'] = 'Duplicates occured'
        deleted_rows = pd.concat([deleted_rows, dup_deleted], ignore_index=True)
        orders_df = orders_df[~dup_mask].copy()
        
    return orders_df, deleted_rows