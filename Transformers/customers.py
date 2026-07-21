import string
import pandas as pd
def transformcustomers(cus_df):
    cus_df['city']=cus_df['city'].astype(str).str.strip()
    cus_df=cus_df[list(cus_df.columns)[:-1]]
    col_names_for_dropped_df=list(cus_df.columns)
    col_names_for_dropped_df.append('Reason')
    dropped_vals=pd.DataFrame(columns=col_names_for_dropped_df)
    columnstochecknullity=['email','username','password']
    for x in columnstochecknullity:
        null_mask=cus_df[x].isna()
        clean_df=cus_df[~null_mask].copy()
        dropped_vals=pd.concat([dropped_vals,cus_df[null_mask].copy()],ignore_index=True)
        reason_column=dropped_vals['Reason']
        dropped_vals.loc[dropped_vals['Reason'].isna(), 'Reason'] = f'{x} was null'
        cus_df=clean_df
    columnstocheckduplicates=['id','email','username']
    for x in columnstocheckduplicates:
        mask_col=cus_df[x].duplicated(keep='first')
        rowstodelete=cus_df[mask_col].copy()
        dropped_vals=pd.concat([dropped_vals,rowstodelete],ignore_index=True)
        null_mask=dropped_vals['Reason'].isna()
        dropped_vals.loc[null_mask,'Reason']=f'{x} was duplicated'
        cus_df=cus_df[~mask_col].copy() 
    return cus_df,dropped_vals