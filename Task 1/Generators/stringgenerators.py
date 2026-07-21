def get_db_url(username,password,host,port_no,db_name):
    return f"postgresql://{username}:{password}@{host}:{port_no}/{db_name}"  