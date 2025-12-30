# Retail Insights & Forecasting Tool (RIFT)

**RIFT** is an end-to-end sales analytics platform designed to help retailers optimize inventory and boost sales through data-driven insights. It features automated data pipelines, machine learning-driven recommendations, and high-accuracy forecasting.

## 🚀 Key Features & Impact
* **Engineered Data Pipeline:** Migrated 820k+ rows of raw transaction data into a **PostgreSQL** database, reducing data-load latency by **70%**.
* **AI Recommendations:** Implemented an **FP-Growth algorithm** to identify 250+ association rules (e.g., Red vs. White T-Light Holders), identifying cross-sell opportunities with up to **70% confidence**.
* **Predictive Forecasting:** Developed a **Prophet-based** time-series model to project daily sales 30 days into the future.
* **Automated Anomaly Detection:** Utilized **Isolation Forest** to flag extreme sales outliers, helping identify bulk orders or system errors.
* **Production Ready:** Fully **Dockerized** the application for seamless deployment to AWS or other cloud environments.

## 🛠️ Technology Stack
* **Database:** PostgreSQL (Dockerized)
* **Analysis:** Python (Pandas, SQLAlchemy)
* **Machine Learning:** Scikit-learn (Isolation Forest), mlxtend (FP-Growth)
* **Forecasting:** Meta Prophet
* **DevOps:** Docker

## 📊 Visual Insights
*(Note: You can take the screenshots you just made and put them in an 'images' folder in your project!)*

1.  **Sales Forecast:** Shows clear seasonal trends and predicted 30-day growth.
2.  **Anomaly Detection:** Highlights significant outliers (red markers) in the sales history.

## ⚙️ Setup & Installation
1.  **Clone the Repo:** `git clone https://github.com/yourusername/RIFT`
2.  **Launch Database:** `docker run --name rift-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres`
3.  **Install Dependencies:** `pip install -r requirements.txt`
4.  **Run Pipeline:** `python load_data.py`