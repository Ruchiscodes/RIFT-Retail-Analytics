import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import matplotlib.pyplot as plt

# Connect to your Docker Database
engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@host.docker.internal:5432/postgres')

def run_forecasting():
    print("Fetching time-series data...")
    # We pull Date and Quantity (or Price * Quantity for revenue)
    query = "SELECT \"InvoiceDate\", \"Quantity\" FROM raw_sales"
    df = pd.read_sql(query, engine)

    # 1. Prepare data for Prophet
    # Prophet requires two columns: 'ds' (datestamp) and 'y' (the value to predict)
    df['ds'] = pd.to_datetime(df['InvoiceDate']).dt.date
    df_daily = df.groupby('ds')['Quantity'].sum().reset_index()
    df_daily.columns = ['ds', 'y']

    print("Training the Prophet model...")
    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    model.fit(df_daily)

    # 2. Forecast the next 30 days
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # 3. Visualize the results
    print("Generating forecast plot...")
    fig = model.plot(forecast)
    plt.title("30-Day Sales Forecast")
    plt.xlabel("Date")
    plt.ylabel("Total Quantity Sold")
    plt.show()
    
    # Save the forecast data
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).to_csv('sales_forecast.csv', index=False)
    print("Forecast saved to 'sales_forecast.csv'")

if __name__ == "__main__":
    run_forecasting()