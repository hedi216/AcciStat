from db_utils import get_connection
import pandas as pd

engine = get_connection()
query = "SELECT * FROM caracteristiques LIMIT 10"
df = pd.read_sql_query(query, con=engine)

print("Shape:", df.shape)
print(df.head())
