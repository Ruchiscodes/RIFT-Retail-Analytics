# import time
# import pandas as pd
# from sqlalchemy import create_engine

# # CSV Path
# csv_path = 'data/online_retail_II.csv'
# # SQL Engine
# engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres')

# # 1. Test CSV Latency
# start_csv = time.time()
# df_csv = pd.read_csv(csv_path)
# filtered_csv = df_csv[df_csv['Price'] > 10] # Example filter
# end_csv = time.time()
# csv_time = end_csv - start_csv

# # 2. Test SQL Latency (Real-time Analytics)
# # Change the SQL query to only pull what you need for a specific chart
# start_sql = time.time()
# df_sql = pd.read_sql("SELECT \"InvoiceDate\", \"Quantity\" FROM raw_sales WHERE \"Price\" > 10", engine)
# end_sql = time.time()
# sql_time = end_sql - start_sql

# reduction = ((csv_time - sql_time) / csv_time) * 100

# print(f"CSV Load Time: {csv_time:.4f}s")
# print(f"SQL Load Time: {sql_time:.4f}s")
# print(f"✅ Data-load Latency Reduction: {reduction:.1f}%")

import time
import pandas as pd
from sqlalchemy import create_engine

csv_path = 'data/online_retail_II.csv'
engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres')

# 1. CSV Latency (Searching through the whole file)
start_csv = time.time()
df_csv = pd.read_csv(csv_path)
# Complex filter mimics a real dashboard query
res_csv = df_csv[(df_csv['Price'] > 5) & (df_csv['Quantity'] > 10)]
end_csv = time.time()
csv_time = end_csv - start_csv

# 2. SQL Latency (Database Optimization)
start_sql = time.time()
# Real-world optimization: Only pull the columns needed for the chart
query = "SELECT \"InvoiceDate\", \"Quantity\" FROM raw_sales WHERE \"Price\" > 5 AND \"Quantity\" > 10"
df_sql = pd.read_sql(query, engine)
end_sql = time.time()
sql_time = end_sql - start_sql

reduction = ((csv_time - sql_time) / csv_time) * 100
print(f"✅ Latency Reduction: {reduction:.1f}%")