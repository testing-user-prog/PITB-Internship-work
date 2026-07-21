import pandas as pd

def transformproducts(products_df):
    valid_cols_df = list(products_df.columns[:-1])
    products_df=products_df[valid_cols_df]
    products_df['price'] = products_df['price'].astype(str).str.replace('$', '', regex=False)
    
    columns_to_trim_spaces = ['title', 'price', 'description', 'category', 'image']
    for x in columns_to_trim_spaces:
        if x in products_df.columns:
            products_df[x] = products_df[x].astype(str).str.strip()

    deleted_dataframe_cols = valid_cols_df.copy()
    deleted_dataframe_cols.append('Reason')
    
    # Removal of the null values
    deleted_rows = pd.DataFrame(columns=deleted_dataframe_cols)
    null_cols = ['id', 'title', 'price']
    null_mask = products_df[null_cols].isna().any(axis=1)
    
    deleted_rows = pd.concat([products_df[null_mask].copy()], ignore_index=True)
    deleted_rows['Reason'] = 'Null value found'
    products_df = products_df[~null_mask].copy()
    
    dup_cols = ['id']
    dup_mask = products_df[dup_cols].duplicated(keep='first')
    
    dup_deleted = products_df[dup_mask].copy()
    dup_deleted['Reason'] = 'Duplicates occured'
    
    deleted_rows = pd.concat([deleted_rows, dup_deleted], ignore_index=True)
    products_df = products_df[~dup_mask].copy()
    
    return products_df, deleted_rows