import pandas as pd
def transformcustomer(customers_data):
    mapped_rows = []
    for idx, row in customers_data.iterrows():
        address = row.get('address')
        address = address if isinstance(address, dict) else {}
        mapped_rows.append({
            'id': row.get('id'),
            'email': row.get('email'),
            'username': row.get('username'),
            'password': row.get('password'),
            'first_name': row.get('firstName'),
            'last_name': row.get('lastName'),
            'phone': row.get('phone'),
            'city': address.get('city'),
            'street': address.get('address'),
            'zipcode': address.get('postalCode')
        })

    customer_db_columns = [
        'id', 
        'email', 
        'username', 
        'password', 
        'first_name', 
        'last_name', 
        'phone', 
        'city', 
        'street', 
        'zipcode'
    ]
    df_clean = pd.DataFrame(mapped_rows, columns=customer_db_columns)
    df_clean = df_clean.drop_duplicates(subset=['email','username'])
    df_clean['username'] = df_clean['username'].astype(str).str.slice(0, 50)
    df_clean['phone'] = df_clean['phone'].astype(str).str.slice(0, 20)
    df_clean['city'] = df_clean['city'].astype(str).str.slice(0, 100)
    df_clean['street'] = df_clean['street'].astype(str).str.slice(0, 150)
    df_clean['zipcode'] = df_clean['zipcode'].astype(str).str.slice(0, 20)
    df_clean = df_clean.dropna(subset=['id', 'email', 'username'])
    return df_clean
