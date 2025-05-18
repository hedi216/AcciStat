# streamlit/db_utils.py
import pandas as pd
from sqlalchemy import create_engine

def get_connection():
    return create_engine("mysql+pymysql://root:@localhost/accidents")

def load_table(name):
    engine = get_connection()
    return pd.read_sql_table(name, con=engine)
