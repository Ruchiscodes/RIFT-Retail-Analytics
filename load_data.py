import pandas as pd
from sqlalchemy import create_engine

# 1. Connection settings (Matching your Docker command)
DB_TYPE = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_USER = 'postgres'
DB_PASS = 'mysecretpassword' # The password you set in the Docker command
DB_HOST = 'host.docker.internal'
DB_PORT = '5432'
DB_NAME = 'postgres'

# Create the connection string
connection_string = f"{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

def load_retail_data(file_path):
    print("Reading CSV... (this might take a minute)")
    # We use low_memory=False because the dataset is large
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    
    # 2. Basic Cleaning
    # Convert InvoiceDate to actual datetime objects
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Remove rows with no Customer ID (optional, but common in this project)
    df = df.dropna(subset=['Customer ID'])
    
    print(f"Uploading {len(df)} rows to PostgreSQL...")
    # 3. Upload to SQL
    df.to_sql('raw_sales', engine, if_exists='replace', index=False)
    print("Successfully loaded data into 'raw_sales' table!")

if __name__ == "__main__":
    # Update this path to where your Kaggle CSV is located
    load_retail_data('data/online_retail_II.csv')
    