import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Connect to your Docker Database
#engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres')
# Change localhost to host.docker.internal
engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@host.docker.internal:5432/postgres')

def find_anomalies():
    print("Fetching daily sales data...")
    query = "SELECT \"InvoiceDate\", \"Quantity\" FROM raw_sales"
    df = pd.read_sql(query, engine)
    
    # Prepare daily totals
    df['date'] = pd.to_datetime(df['InvoiceDate']).dt.date
    daily_sales = df.groupby('date')['Quantity'].sum().reset_index()
    
    print("Running Isolation Forest (Anomaly Detection)...")
    # contamination=0.01 means we expect about 1% of data to be 'weird'
    model = IsolationForest(contamination=0.01, random_state=42)
    
    # We reshape the data for the model
    daily_sales['anomaly_score'] = model.fit_predict(daily_sales[['Quantity']])
    
    # -1 means it's an anomaly, 1 means it's normal
    anomalies = daily_sales[daily_sales['anomaly_score'] == -1]
    
    print(f"Found {len(anomalies)} suspicious sales days.")
    
    # Visualize
    plt.figure(figsize=(12,6))
    plt.plot(daily_sales['date'], daily_sales['Quantity'], color='blue', label='Normal Sales', alpha=0.5)
    plt.scatter(anomalies['date'], anomalies['Quantity'], color='red', label='ANOMALY', edgecolors='black')
    plt.title("Detected Sales Anomalies (RIFT Engine)")
    plt.legend()
    plt.show()

    # Save to CSV
    anomalies.to_csv('detected_anomalies.csv', index=False)
    print("Anomalies saved to 'detected_anomalies.csv'")

if __name__ == "__main__":
    find_anomalies()