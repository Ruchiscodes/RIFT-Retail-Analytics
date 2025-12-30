import pandas as pd
from sqlalchemy import create_engine
from mlxtend.frequent_patterns import fpgrowth, association_rules

# 1. Connect to your Docker Database
engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres')

def run_recommendations():
    print("Fetching data from PostgreSQL...")
    # We only need Invoice and Description for this part
    query = "SELECT \"Invoice\", \"Description\" FROM raw_sales"
    df = pd.read_sql(query, engine)

    print("Preparing 'baskets' (this may take a moment)...")
    # Clean up descriptions
    df['Description'] = df['Description'].str.strip()
    
    # Create the 'Basket' format: Each row is an invoice, each column is a product
    basket = (df.groupby(['Invoice', 'Description'])['Description']
              .count().unstack().reset_index().fillna(0)
              .set_index('Invoice'))

    # Convert counts to 1 (bought) or 0 (not bought)
    def encode_units(x):
        return 1 if x >= 1 else 0
    basket_sets = basket.map(encode_units)

    print("Running FP-Growth algorithm...")
    # Find items that appear in at least 2% of all transactions
    frequent_itemsets = fpgrowth(basket_sets, min_support=0.005, use_colnames=True)

    # Generate the rules (The 'Insights')
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    # Sort by 'confidence' to find the strongest relationships
    rules = rules.sort_values('confidence', ascending=False)

    print("\n--- TOP 10 PRODUCT RECOMMENDATIONS ---")
    print(rules[['antecedents', 'consequents', 'support', 'confidence']].head(10))
    
    # Save to CSV so you can show it in your project portfolio
    rules.to_csv('product_recommendations.csv', index=False)
    print("\nResults saved to 'product_recommendations.csv'")

if __name__ == "__main__":
    run_recommendations()